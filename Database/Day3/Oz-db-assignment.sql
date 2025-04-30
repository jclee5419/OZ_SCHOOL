USE ozdatabase;

-- employees 테이블 생성
-- CREATE TABLE employees(
-- 	id INT AUTO_INCREMENT PRIMARY KEY,
--  name VARCHAR(100),
--  position VARCHAR(100),
--  salary DECIMAL(10, 2)
-- );

-- 직원데이터를 emplyees에 추가
-- INSERT INTO employees (name, position, salary) VALUES
-- 	('혜린', 'PM', 90000),
-- 	('은우', 'Frontend', 80000),
-- 	('가을', 'Backend', 92000),
-- 	('지수', 'Frontend', 78000),
-- 	('민혁', 'Frontend', 96000),
-- 	('하은', 'Backend', 130000);

-- 모든 직원의 이름과 연봉 정보만으로 조회하는 쿼리 작성
-- SELECT name, salary FROM employees; 

-- Frontend 직책을 가진 직원중에서 연봉이 90000 이하인 직원의 이름과 연봉 조회
-- SELECT * FROM employees WHERE position = 'Frontend' AND salary <= 90000;

-- PM 직책을 가진 모든 직원의 연봉을 10%씩 인상한 후 결과 확인 
-- SET SQL_SAFE_UPDATES = 0;

-- UPDATE employees
-- SET salary = salary * 1.10
-- WHERE position = 'PM';

-- SELECT * FROM employees WHERE position = 'PM';

--  모든 Backend 직책을 가진 직원의 연봉을 5% 인상
-- UPDATE employees
-- SET salary = salary * 1.05
-- WHERE position = 'Backend';

-- SELECT * FROM employees WHERE position = 'Backend';

-- 민혁 사원의 데이터 삭제
-- DELETE FROM employees WHERE name = '민혁';

-- 모든 직원을 position별로 그룹화 하여 각 직책의 평균 연봉을 계산
-- SELECT position, AVG(salary) AS average_salary
-- FROM employees
-- GROUP BY position;

-- employee 테이블 삭제
-- DROP TABLE emloyees;
