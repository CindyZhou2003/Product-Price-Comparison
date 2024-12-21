DELETE FROM backend_products
WHERE MOD(id, 2) = 1;

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

ALTER TABLE backend_products ADD COLUMN temp_id INT;
UPDATE backend_products SET temp_id = id;
ALTER TABLE backend_categories DROP FOREIGN KEY backend_products_category_id_2badbf24_fk_backend_categories_id;
ALTER TABLE backend_likes DROP FOREIGN KEY backend_likes_product_id_8a73949a_fk_backend_products_id;
ALTER TABLE backend_prices DROP FOREIGN KEY backend_prices_product_id_113f0f24_fk_backend_products_id;

ALTER TABLE backend_products DROP COLUMN id;
ALTER TABLE backend_products ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
ALTER TABLE backend_products AUTO_INCREMENT = 1;
ALTER TABLE backend_products DROP COLUMN temp_id;

SHOW TABLE STATUS LIKE 'backend_products';


SET FOREIGN_KEY_CHECKS = 1;

SELECT CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'backend_products' AND TABLE_SCHEMA = DATABASE()
AND REFERENCED_TABLE_NAME IS NOT NULL;


ALTER TABLE backend_categories
ADD CONSTRAINT backend_categories_parent_id_fk
FOREIGN KEY (parent_id) REFERENCES backend_categories (id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE backend_prices
ADD CONSTRAINT backend_prices_product_id_fk
FOREIGN KEY (product_id) REFERENCES backend_products (id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE backend_likes
ADD CONSTRAINT backend_likes_product_id_fk
FOREIGN KEY (product_id) REFERENCES backend_products (id)
ON DELETE CASCADE ON UPDATE CASCADE;


SET @count = 0;
UPDATE backend_products SET id = (@count := @count + 1);
ALTER TABLE backend_products AUTO_INCREMENT = 3339;