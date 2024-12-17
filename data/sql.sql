UPDATE backend_products
SET platform = REPLACE(REPLACE(platform, '\n', ''), '\r', '')
WHERE platform LIKE '%\n%' OR platform LIKE '%\r%';

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(10, 2),
    comments VARCHAR(50),
    shop VARCHAR(255),
    img VARCHAR(255),
    link VARCHAR(255)
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\jd3.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(title, price, comments, shop, img, link);

SHOW VARIABLES LIKE 'secure_file_priv';

SELECT MAX(id) FROM products;
SELECT COUNT(*) FROM products;

TRUNCATE TABLE products;
ALTER TABLE products ADD COLUMN web VARCHAR(20);
UPDATE products SET platform = '京东';

ALTER TABLE products ADD COLUMN temp_id INT;
UPDATE products SET temp_id = id;
ALTER TABLE products DROP COLUMN id;
ALTER TABLE products ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
ALTER TABLE products DROP COLUMN temp_id;



