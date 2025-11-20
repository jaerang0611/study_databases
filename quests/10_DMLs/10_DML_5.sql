CREATE TABLE shop_products (
    product_id INT PRIMARY KEY,
    name VARCHAR(500),
    price INT,
    stock INT,
    category VARCHAR(500)
);

INSERT INTO shop_products (product_id, name, price, stock, category) VALUES
(1, 'USB 메모리', 12000, 50, '전자제품'),
(2, '블루투스 스피커', 45000, 20, '전자제품'),
(3, '물병', 5000, 100, '생활용품');

SELECT *
FROM shop_products;

SELECT product_id, name, price, stock, category
FROM shop_products
WHERE price >= 10000;

UPDATE shop_products
SET stock = 80
WHERE name = '물병';

DELETE FROM shop_products
WHERE name = '블루투스 스피커';