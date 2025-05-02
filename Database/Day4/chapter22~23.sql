-- 생성(CREATE)초급 10문제

-- customers 테이블에 새 고객을 추가하세요.
(1) INSERT INTO customers(name, age, address) VALUES ('Jongchan', 29, 'jinju_gyeongsangnam-do');

-- products 테이블에 새 제품을 추가하세요.
(2) INSERT INTO products(name, product_category, price) VALUES ('fujifilm_x-100v', 'camera', 1700000)

-- employees 테이블에 새 직원을 추가하세요.
(3) INSERT INTO employees(FirstName, age, address) VALUES ('chunsam', 52, 'hapcheon_gyeongsangnam-do');

-- offices 테이블에 새 사무실을 추가하세요.
(4) INSERT INTO offices(city, telephone, address) VALUES ('seoul', '02-123-4567', 'yongsan-gu_seoul');

-- orders 테이블에 새 주문을 추가하세요.
(5) INSERT INTO orders(order_date, customer_id, product_id) VALUES ('2025-05-02', 52, 100);

-- orderdetails 테이블에 주문 상세정보를 추가하세요.
(6) INSERT INTO orderdetails(order_id, product_id, quantity) VALUES (2, 100, 1);

-- payments 테이블에 지불 정보를 추가하세요.
(7) INSERT INTO payments(customer_id, order_id, price) VALUES (52, 2, 1700000);

-- productlines 테이블에 제품 라인을 추가하세요.
(8) INSERT INTO productlines(productLine, textDescription, ) VALUES ('camera', '한손에 들고다니면서 간편하게!');

-- customers 테이블에 다른지역의 고객을 추가하세요.
(9) INSERT INTO customers(name, age, address) VALUES ('inhye', 32, 'goyang_gyeonggi-do');

-- products 테이블에 다른 카테고리의 제품을 추가하세요.
(10) INSERT INTO products(name, product_category, price) VALUES ('ps5-pro', 'console_gamemachine', 1118000);

-- 읽기(READ) 초급 10문제

-- customers 테이블에서 모든 고객 정보를 조회하세요.
(1) SELECT * FROM customers;

-- products 테이블에서 모든 제품 목록을 조회하세요.
(2) SELECT * FROM products;

-- employees 테이블에서 모든 직원의 이름과 직급을 조회하세요.
(3) SELECT name, employees_rank FROM employees;

-- offices 테이블에서 모든 사무실의 위치를 조회하세요.
(4) SELECT address FROM offices;

-- orders 테이블에서 최근 10개의 주문을 조회하세요.
(5) SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;

-- orderdetails 테이블에서 특정 주문의 모든 상세정보를 조회하세요.
(6) SELECT * FROM orderdetails WHERE order_id = 2;

-- payments 테이블에서 특정 고객의 모든 지불 정보를 조회하세요.
(7) SELECT * FROM payments WHERE customer_id = 52;

-- productlines 테이블에서 각 제품 라인의 설명을 조회하세요.
(8) SELECT textDescription FROM productlines;

-- customers 테이블에서 특정 지역의 고객을 조회하세요.
(9) SELECT * FROM customers WHERE address 'gyeongsangnam-do';

-- products 테이블에서 특정 가격범위의 제품을 조회하세요.
(10) SELECT * FROM products WHERE price BETWEEN 1500000 AND 2000000;

-- 갱신(UPDATE) 초급 10문제

-- customers 테이블에서 특정 고객의 주소를 갱신하세요.
(1) UPDATE customers SET adress = 'gyungsangbuk-do' WHERE name = 'inhye';

-- products 테이블에서 특정 제품의 가격을 갱신하세요.
(2) UPDATE products SET price = 1800000 WHERE name = 'fujifilm_x-100v';

-- employees 테이블에서 특정 직원의 직급을 갱신하세요.
(3) UPDATE employees SET employees_rank = 'manager' WHERE FirstName = 'chunsam';

-- offices 테이블에서 특정 사무실의 전화번호를 갱신하세요.
(4) UPDATE offices SET telephone = '02-987-6543' WHERE city = 'seoul';

-- orders 테이블에서 특정 주문의 상태를 갱신하세요.
(5) UPDATE orders SET status = 'shipped' WHERE order_id = 2;

-- orderdetails 테이블에서 특정 주문의 상세의 수량을 갱신하세요.
(6) UPDATE orderdetails SET quantity = 2 WHERE order_id = 2;

-- payments 테이블에서 특정 고객의 지불 금액을 갱신하세요.
(7) UPDATE payments SET price = 1800000 WHERE customer_id = 52;

-- productlines 테이블에서 특정 제품 라인의 설명을 갱신하세요.
(8) UPDATE productlines SET textDescription = '최고의 카메라' WHERE productLine = 'camera';

-- customers 테이블에서 특정 지역의 고객의 이메일을 갱신하세요.
(9) UPDATE customers SET email = 'gyungnam@gmail.com' WHERE address = 'gyeongsangnam-do';

-- products 테이블에서 여러 제품의 가격을 한번에 갱신하세요.
(10) UPDATE products SET price = price * 0.9;

-- 삭제(DELETE) 초급 10문제

-- customers 테이블에서 특정 고객을 삭제하세요.
(1) DELETE FROM customers WHERE name = 'inhye';

-- products 테이블에서 특정 제품을 삭제하세요.
(2) DELETE FROM products WHERE name = 'ps5-pro';

-- employees 테이블에서 특정 직원을 삭제하세요.
(3) DELETE FROM employees WHERE FirstName = 'chunsam';

-- offices 테이블에서 특정 사무실을 삭제하세요.
(4) DELETE FROM offices WHERE city = 'seoul';

-- orders 테이블에서 특정 주문을 삭제하세요.
(5) DELETE FROM orders WHERE order_id = 2;

-- orderdetails 테이블에서 특정 주문의 상세를 삭제하세요.
(6) DELETE FROM orderdetails WHERE order_id = 2;

-- payments 테이블에서 특정 고객의 지불 내역을 삭제하세요.
(7) DELETE FROM payments WHERE customer_id = 52;

-- productlines 테이블에서 특정 제품 라인을 삭제하세요.
(8) DELETE FROM productlines WHERE productLine = 'camera';

-- customers 테이블에서 특정 지역의 모든 고객을 삭제하세요.
(9) DELETE FROM customers WHERE address = 'gyeongsangnam-do';

-- products 테이블에서 특정 카테고리의 모든 제품을 삭제하세요.
(10) DELETE FROM products WHERE product_category = 'console_gamemachine';
