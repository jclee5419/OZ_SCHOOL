import requests
import time
import random
import pymysql
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# MySQL 연결 설정
def connect_to_database():
    connection = pymysql.connect(
        host='localhost',          # MySQL 서버 주소
        user='root',               # MySQL 사용자 이름
        password='0000',       # MySQL 비밀번호
        database='KREAM-DB',       # 데이터베이스 이름
        charset='utf8mb4'
    )
    return connection

# 데이터베이스 및 테이블 생성
def setup_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='0000',
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # 데이터베이스 생성
            cursor.execute("CREATE DATABASE IF NOT EXISTS kream_db")
            cursor.execute("USE kream_db")
            
            # 상품 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id VARCHAR(50) UNIQUE,
                    brand VARCHAR(255),
                    name VARCHAR(255),
                    model_number VARCHAR(100),
                    release_date DATE,
                    original_price INT,
                    scrape_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 가격 정보 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id VARCHAR(50),
                    size VARCHAR(50),
                    price INT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)
            
            # 거래 내역 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id VARCHAR(50),
                    size VARCHAR(50),
                    price INT,
                    transaction_date DATETIME,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)
            
        connection.commit()
        print("데이터베이스와 테이블이 성공적으로 생성되었습니다.")
    
    except Exception as e:
        print(f"데이터베이스 설정 중 오류 발생: {e}")
    
    finally:
        connection.close()

# Selenium 웹드라이버 설정
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 백그라운드 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# KREAM 상품 목록 페이지 스크레이핑
def scrape_product_list(driver, category_url, page_limit=5):
    product_links = []
    
    for page in range(1, page_limit + 1):
        url = f"{category_url}?page={page}"
        driver.get(url)
        
        # 페이지 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_card"))
        )
        
        # 상품 카드 링크 추출
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div.product_card a")
        
        for element in product_elements:
            link = element.get_attribute("href")
            if link and "products/" in link:
                product_links.append(link)
        
        # 중복 제거
        product_links = list(set(product_links))
        
        print(f"페이지 {page} 스크레이핑 완료: {len(product_links)}개 상품 발견")
        
        # 요청 간격 조정
        time.sleep(random.uniform(1.5, 3.0))
    
    return product_links

# 상품 상세 페이지 스크레이핑
def scrape_product_detail(driver, product_url):
    driver.get(product_url)
    
    # 페이지 완전 로딩 대기
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_detail"))
    )
    
    time.sleep(2)  # 추가 대기
    
    try:
        # 제품 ID 추출
        product_id = product_url.split("/")[-1]
        
        # 상품 기본 정보 추출
        brand = driver.find_element(By.CSS_SELECTOR, "a.brand").text.strip()
        name = driver.find_element(By.CSS_SELECTOR, "p.title").text.strip()
        
        # 모델 번호 및 출시일
        product_info = driver.find_elements(By.CSS_SELECTOR, "div.detail_box")
        model_number = None
        release_date = None
        original_price = None
        
        for info in product_info:
            title_element = info.find_element(By.CSS_SELECTOR, "h3.title")
            if "모델번호" in title_element.text:
                model_number = info.find_element(By.CSS_SELECTOR, "div.detail_product_info").text.strip()
            elif "발매일" in title_element.text:
                date_text = info.find_element(By.CSS_SELECTOR, "div.detail_product_info").text.strip()
                if date_text:
                    # 날짜 포맷 변환 (YYYY/MM/DD 형식 가정)
                    release_date = date_text
            elif "발매가" in title_element.text:
                price_text = info.find_element(By.CSS_SELECTOR, "div.detail_product_info").text.strip()
                original_price = price_text.replace(",", "").replace("원", "").strip()
                if original_price:
                    try:
                        original_price = int(original_price)
                    except ValueError:
                        original_price = 0
        
        # 사이즈별 가격 정보 추출
        size_price_data = []
        
        # 사이즈 선택 클릭
        size_button = driver.find_element(By.CSS_SELECTOR, "div.size")
        size_button.click()
        
        time.sleep(1)
        
        # 사이즈 목록 추출
        size_list = driver.find_elements(By.CSS_SELECTOR, "ul.option_list li.item")
        
        for size_item in size_list:
            try:
                size = size_item.find_element(By.CSS_SELECTOR, "button.btn").text.strip()
                price_element = size_item.find_element(By.CSS_SELECTOR, "div.price")
                price_text = price_element.text.strip().replace(",", "").replace("원", "")
                
                if price_text and price_text != "-":
                    price = int(price_text)
                    size_price_data.append({"size": size, "price": price})
            except Exception as e:
                print(f"사이즈 가격 추출 오류: {e}")
        
        # ESC 키를 눌러 사이즈 선택 팝업 닫기
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        
        # 거래 내역 추출을 위해 "체결 내역" 탭 클릭
        try:
            tabs = driver.find_elements(By.CSS_SELECTOR, "div.tab_list a.tab_link")
            for tab in tabs:
                if "체결 내역" in tab.text:
                    tab.click()
                    break
            
            time.sleep(2)
            
            # 거래 내역 추출
            transactions = []
            transaction_items = driver.find_elements(By.CSS_SELECTOR, "div.purchase_list_box .purchase_item")
            
            for item in transaction_items[:10]:  # 최근 10개 거래만 추출
                try:
                    transaction_size = item.find_element(By.CSS_SELECTOR, ".column_size").text.strip()
                    transaction_price_text = item.find_element(By.CSS_SELECTOR, ".column_price").text.strip()
                    transaction_price = int(transaction_price_text.replace(",", "").replace("원", ""))
                    transaction_date_text = item.find_element(By.CSS_SELECTOR, ".column_date").text.strip()
                    
                    transactions.append({
                        "size": transaction_size,
                        "price": transaction_price,
                        "date": transaction_date_text
                    })
                except Exception as e:
                    print(f"거래 내역 추출 오류: {e}")
        
        except Exception as e:
            print(f"체결 내역 탭 오류: {e}")
            transactions = []
        
        # 결과 반환
        product_data = {
            "product_id": product_id,
            "brand": brand,
            "name": name,
            "model_number": model_number,
            "release_date": release_date,
            "original_price": original_price,
            "size_prices": size_price_data,
            "transactions": transactions
        }
        
        return product_data
        
    except Exception as e:
        print(f"상품 상세 정보 스크레이핑 오류: {e}")
        return None

# MySQL에 데이터 저장
def save_to_database(connection, product_data):
    try:
        with connection.cursor() as cursor:
            # 상품 정보 저장
            sql = """
                INSERT INTO products 
                (product_id, brand, name, model_number, release_date, original_price)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                brand = VALUES(brand),
                name = VALUES(name),
                model_number = VALUES(model_number),
                release_date = VALUES(release_date),
                original_price = VALUES(original_price)
            """
            
            # 날짜 변환
            release_date = None
            if product_data["release_date"]:
                try:
                    # YYYY/MM/DD 형식 가정
                    parts = product_data["release_date"].split("/")
                    if len(parts) == 3:
                        release_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
                except:
                    pass
            
            cursor.execute(sql, (
                product_data["product_id"],
                product_data["brand"],
                product_data["name"],
                product_data["model_number"],
                release_date,
                product_data["original_price"]
            ))
            
            # 사이즈별 가격 정보 저장
            if product_data["size_prices"]:
                price_sql = """
                    INSERT INTO prices
                    (product_id, size, price)
                    VALUES (%s, %s, %s)
                """
                
                for size_price in product_data["size_prices"]:
                    cursor.execute(price_sql, (
                        product_data["product_id"],
                        size_price["size"],
                        size_price["price"]
                    ))
            
            # 거래 내역 저장
            if product_data["transactions"]:
                transaction_sql = """
                    INSERT INTO transactions
                    (product_id, size, price, transaction_date)
                    VALUES (%s, %s, %s, %s)
                """
                
                for transaction in product_data["transactions"]:
                    # 거래일자 변환 (현재는 간단히 처리)
                    transaction_date = None
                    try:
                        # 시간 문자열을 MySQL datetime 형식으로 변환
                        from datetime import datetime
                        if "분 전" in transaction["date"]:
                            minutes = int(transaction["date"].replace("분 전", "").strip())
                            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        elif "시간 전" in transaction["date"]:
                            hours = int(transaction["date"].replace("시간 전", "").strip())
                            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            # 2023/05/12 와 같은 형식 가정
                            parts = transaction["date"].split("/")
                            if len(parts) == 3:
                                transaction_date = f"{parts[0]}-{parts[1]}-{parts[2]} 00:00:00"
                    except:
                        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    cursor.execute(transaction_sql, (
                        product_data["product_id"],
                        transaction["size"],
                        transaction["price"],
                        transaction_date
                    ))
            
            connection.commit()
            print(f"상품 ID: {product_data['product_id']} - 데이터베이스 저장 완료")
            
    except Exception as e:
        connection.rollback()
        print(f"데이터베이스 저장 오류: {e}")

# 메인 함수
def main():
    # 데이터베이스 설정
    setup_database()
    
    # 웹드라이버 설정
    driver = setup_driver()
    
    try:
        # 스크레이핑할 카테고리 URL
        category_urls = [
            "https://kream.co.kr/search/shoes",  # 신발
            "https://kream.co.kr/search/clothes"  # 의류
        ]
        
        # 카테고리별 스크레이핑
        for category_url in category_urls:
            print(f"카테고리 {category_url} 스크레이핑 시작")
            
            # 상품 목록 페이지 스크레이핑
            product_links = scrape_product_list(driver, category_url, page_limit=3)
            
            # 데이터베이스 연결
            connection = connect_to_database()
            
            # 상품 상세 페이지 스크레이핑 및 데이터베이스 저장
            for link in product_links:
                print(f"상품 URL 스크레이핑: {link}")
                product_data = scrape_product_detail(driver, link)
                
                if product_data:
                    save_to_database(connection, product_data)
                
                # 요청 간격 조정
                time.sleep(random.uniform(2.0, 4.0))
            
            # 연결 종료
            connection.close()
    
    finally:
        # 웹드라이버 종료
        driver.quit()

if __name__ == "__main__":
    main()