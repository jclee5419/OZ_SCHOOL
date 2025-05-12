from pymongo import MongoClient

def insert_data():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  # 'local' 데이터베이스 사용

    # 책 데이터 삽입
    books = [
        {"title": "Kafka on the Shore", "author": "Haruki Murakami", "year": 2002},
        {"title": "Norwegian Wood", "author": "Haruki Murakami", "year": 1987},
        {"title": "1Q84", "author": "Haruki Murakami", "year": 2009}
    ]
    db.books.insert_many(books)

    # 영화 데이터 삽입
    movies = [
        {"title": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 8.8},
        {"title": "Interstellar", "director": "Christopher Nolan", "year": 2014, "rating": 8.6},
        {"title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008, "rating": 9.0}
    ]
    db.movies.insert_many(movies)

    # 사용자 행동 데이터 삽입
    user_actions = [
        {"user_id": 1, "action": "click", "timestamp": "2023-04-12T08:00:00Z"},
        {"user_id": 1, "action": "view", "timestamp": "2023-04-12T09:00:00Z"},
        {"user_id": 2, "action": "purchase", "timestamp": "2023-04-12T10:00:00Z"}
    ]
    db.user_actions.insert_many(user_actions)

    print("Data inserted successfully")
    client.close()

if __name__ == "__main__":
    insert_data()

# 문제1. "fantasy" 장르의 책을 모두 찾아서 제목과 저자를 찾는 mongoDB 쿼리를 함수로 만들어 문제를 해결해보자.
def find_fantasy_books():
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  # 'local' 데이터베이스 사용
    
    # "fantasy" 장르의 모든 책 찾기
    fantasy_books = db.books.find(
        {"genre": "fantasy"},  # "fantasy" 장르만 필터링
        {"_id": 0, "title": 1, "author": 1}  # _id는 제외하고 title과 author만 포함
    )
    
    # 결과 출력
    print("판타지 장르 책 목록:")
    books_found = False
    
    for book in fantasy_books:
        books_found = True
        print(f"제목: {book['title']}, 저자: {book['author']}")
    
    if not books_found:
        print("판타지 장르의 책이 없습니다.")
    
    # 연결 종료
    client.close()

if __name__ == "__main__":
    find_fantasy_books()

# 문제2. 모든 영화 감독의 영화 평점 평균을 계산하고, 평균 평점이 높은 순으로 정렬하는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 보자.
def calculate_director_ratings():
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  # 'local' 데이터베이스 사용
    
    # 집계 파이프라인을 사용하여 감독별 평균 평점 계산
    pipeline = [
        # 1단계: 감독별로 그룹화하고 평균 평점 계산
        {
            "$group": {
                "_id": "$director",  # 감독 필드로 그룹화
                "averageRating": {"$avg": "$rating"},  # 평점의 평균 계산
                "movieCount": {"$sum": 1}  # 영화 수 카운트
            }
        },
        # 2단계: 평균 평점을 기준으로 내림차순 정렬
        {
            "$sort": {"averageRating": -1}
        },
        # 3단계: 결과 형식 지정
        {
            "$project": {
                "_id": 0,
                "director": "$_id",
                "averageRating": {"$round": ["$averageRating", 2]},  # 소수점 2자리로 반올림
                "movieCount": 1
            }
        }
    ]
    
    # 집계 실행
    results = db.movies.aggregate(pipeline)
    
    # 결과 출력
    print("감독별 평균 영화 평점 (높은 순):")
    print("-" * 50)
    print(f"{'감독':25} {'평균 평점':10} {'영화 수':8}")
    print("-" * 50)
    
    for result in results:
        print(f"{result['director']:25} {result['averageRating']:10.2f} {result['movieCount']:8}")
    
    # 연결 종료
    client.close()

if __name__ == "__main__":
    calculate_director_ratings()

# 문제3. 사용자 ID가 1인 사용자의 최근 행동 5개를 시간 순으로 정렬하여 조회하는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 보자.
from datetime import datetime

def get_recent_user_actions(user_id=1, limit=5):
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  # 'local' 데이터베이스 사용
    
    # 사용자 ID가 1인 사용자의 행동을 시간 기준 내림차순으로 조회하고 최근 5개만 가져오기
    recent_actions = db.user_actions.find(
        {"user_id": user_id}
    ).sort(
        "timestamp", -1  # -1은 내림차순(최신순), 1은 오름차순(과거순)
    ).limit(limit)
    
    # 결과 출력
    print(f"사용자 ID {user_id}의 최근 {limit}개 행동:")
    print("-" * 60)
    print(f"{'행동 유형':15} {'타임스탬프':30} {'시간 경과':15}")
    print("-" * 60)
    
    # ISO 형식 문자열을 datetime 객체로 변환하는 함수
    def parse_time(timestamp_str):
        return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    
    # 현재 시간 (예시용)
    now = datetime.now()
    
    # 결과 출력
    actions_found = False
    for action in recent_actions:
        actions_found = True
        action_type = action['action']
        timestamp = action['timestamp']
        
        # 타임스탬프를 datetime 객체로 변환하여 현재와의 차이 계산
        try:
            action_time = parse_time(timestamp)
            time_diff = now - action_time
            time_ago = f"{time_diff.days}일 {time_diff.seconds//3600}시간 전"
        except:
            time_ago = "시간 계산 불가"
        
        print(f"{action_type:15} {timestamp:30} {time_ago:15}")
    
    if not actions_found:
        print(f"사용자 ID {user_id}의 행동 기록이 없습니다.")
    
    print("-" * 60)
    
    # 연결 종료
    client.close()

if __name__ == "__main__":
    get_recent_user_actions(user_id=1, limit=5)

# 문제4. 각 출판 연도별로 출판된 책의 수를 계산하고, 출판된 책의 수가 많은 순서대로 정렬하는 MongoDB 쿼리를 함수로 만들어 문제를 해결해 보자.
def count_books_by_year():
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  # 'local' 데이터베이스 사용
    
    # 집계 파이프라인을 사용하여 연도별 책 수 계산
    pipeline = [
        # 1단계: 출판 연도별로 그룹화하고 책 수 계산
        {
            "$group": {
                "_id": "$year",  # 출판 연도 필드로 그룹화
                "bookCount": {"$sum": 1}  # 책 수 카운트
            }
        },
        # 2단계: 책 수 기준으로 내림차순 정렬
        {
            "$sort": {"bookCount": -1}
        },
        # 3단계: 결과 형식 지정
        {
            "$project": {
                "_id": 0,
                "year": "$_id",
                "bookCount": 1
            }
        }
    ]
    
    # 집계 실행
    results = db.books.aggregate(pipeline)
    
    # 결과 출력
    print("출판 연도별 책 수 (많은 순):")
    print("-" * 30)
    print(f"{'출판 연도':10} {'책 수':10}")
    print("-" * 30)
    
    results_list = list(results)  # 결과를 리스트로 변환
    
    if results_list:
        for result in results_list:
            print(f"{result['year']:10} {result['bookCount']:10}")
            
        # 데이터 분석 요약
        total_books = sum(result['bookCount'] for result in results_list)
        years_with_books = len(results_list)
        most_prolific_year = results_list[0]['year']
        most_books = results_list[0]['bookCount']
        
        print("\n----- 데이터 분석 요약 -----")
        print(f"총 책 수: {total_books}")
        print(f"데이터가 있는 연도 수: {years_with_books}")
        print(f"가장 많은 책이 출판된 연도: {most_prolific_year} ({most_books}권)")
    else:
        print("책 데이터가 없습니다.")
    
    # 연결 종료
    client.close()

    # 차트로 시각화할 수 있는 데이터 반환 (다른 함수에서 활용할 수 있음)
    return [(result['year'], result['bookCount']) for result in results_list]

if __name__ == "__main__":
    count_books_by_year()

# 문제5. 사용자 ID가 1인 사용자의 2023년 4월 10일 이전의 "view" 행동을 "seen"으로 변경하는 MongoDB 업데이트 쿼리를 함수로 만들어 문제를 해결해 보자.
from datetime import datetime

def update_user_actions(user_id=1, action_to_update="view", new_action="seen", before_date="2023-04-10"):
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  # 'local' 데이터베이스 사용
    
    # 업데이트 전 상태 확인
    print(f"업데이트 전 사용자 ID {user_id}의 행동 기록:")
    show_user_actions(db, user_id)
    
    # ISO 형식의 날짜로 변환
    before_date_iso = datetime.strptime(before_date, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00Z")
    
    # 업데이트 쿼리 실행
    result = db.user_actions.update_many(
        {
            "user_id": user_id,
            "action": action_to_update,
            "timestamp": {"$lt": before_date_iso}  # 지정 날짜보다 이전 기록만
        },
        {
            "$set": {"action": new_action}
        }
    )
    
    # 업데이트 결과 출력
    if result.matched_count > 0:
        print(f"\n업데이트 성공: {result.matched_count}개의 문서 중 {result.modified_count}개 수정됨")
    else:
        print(f"\n업데이트할 문서가 없습니다. (사용자 ID: {user_id}, 행동: {action_to_update}, 날짜: {before_date} 이전)")
    
    # 업데이트 후 상태 확인
    print(f"\n업데이트 후 사용자 ID {user_id}의 행동 기록:")
    show_user_actions(db, user_id)
    
    # 연결 종료
    client.close()
    
    return result.modified_count

# 사용자 행동 기록을 보여주는 헬퍼 함수
def show_user_actions(db, user_id):
    user_actions = db.user_actions.find({"user_id": user_id}).sort("timestamp", 1)  # 오래된 순으로 정렬
    
    print("-" * 60)
    print(f"{'행동 유형':15} {'타임스탬프':30}")
    print("-" * 60)
    
    actions_found = False
    for action in user_actions:
        actions_found = True
        print(f"{action['action']:15} {action['timestamp']:30}")
    
    if not actions_found:
        print(f"사용자 ID {user_id}의 행동 기록이 없습니다.")
    
    print("-" * 60)

# 테스트를 위한 새로운 데이터 삽입 함수
def insert_test_data():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local
    
    # 기존 데이터에 추가 테스트 데이터 삽입
    test_actions = [
        {"user_id": 1, "action": "view", "timestamp": "2023-04-05T10:00:00Z"},
        {"user_id": 1, "action": "view", "timestamp": "2023-04-08T14:30:00Z"},
        {"user_id": 1, "action": "click", "timestamp": "2023-04-09T08:45:00Z"},
        {"user_id": 1, "action": "view", "timestamp": "2023-04-11T09:20:00Z"},
        {"user_id": 1, "action": "purchase", "timestamp": "2023-04-12T16:15:00Z"}
    ]
    
    # 데이터 삽입
    db.user_actions.insert_many(test_actions)
    print(f"{len(test_actions)}개의 테스트 행동 기록이 추가되었습니다.")
    client.close()

if __name__ == "__main__":
    # 선택 사항: 테스트 데이터 추가 (한 번만 실행)
    # insert_test_data()
    
    # 사용자 ID 1의 2023-04-10 이전의 "view" 행동을 "seen"으로 업데이트
    update_user_actions(user_id=1, action_to_update="view", new_action="seen", before_date="2023-04-10")
