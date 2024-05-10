CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    description VARCHAR,
    category_id INTEGER,
    price DECIMAL,
    FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE shop_order (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    date DATE,
    FOREIGN KEY (customer_id) REFERENCES customer (id)
);

CREATE TABLE shop_order_product (
    shop_order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (shop_order_id, product_id),
    FOREIGN KEY (shop_order_id) REFERENCES shop_order (id),
    FOREIGN KEY (product_id) REFERENCES product (id)
);

INSERT INTO category (id, name) VALUES (1, 'Games');
INSERT INTO category (id, name) VALUES (2, 'Books');
INSERT INTO category (id, name) VALUES (3, 'Movies');

INSERT INTO product (id, name, description, category_id, price) VALUES (1, 'The Witcher 3', 'An action RPG game', 1, 49.99);
INSERT INTO product (id, name, description, category_id, price) VALUES (2, 'Doom', 'A first-person shooter game', 1, 29.99);
INSERT INTO product (id, name, description, category_id, price) VALUES (3, 'The Lord of the Rings', 'A fantasy book', 2, 19.99);
INSERT INTO product (id, name, description, category_id, price) VALUES (4, 'The Matrix', 'A sci-fi movie', 3, 9.99);

INSERT INTO customer (id, name) VALUES (1, 'Alice');
INSERT INTO customer (id, name) VALUES (2, 'Bob');

INSERT INTO shop_order (id, customer_id, date) VALUES (1, 1, '2024-01-01');
INSERT INTO shop_order (id, customer_id, date) VALUES (2, 2, '2024-01-02');

INSERT INTO shop_order_product (shop_order_id, product_id, quantity) VALUES (1, 1, 4);
INSERT INTO shop_order_product (shop_order_id, product_id, quantity) VALUES (1, 2, 2);
INSERT INTO shop_order_product (shop_order_id, product_id, quantity) VALUES (2, 3, 1);
INSERT INTO shop_order_product (shop_order_id, product_id, quantity) VALUES (2, 4, 5);
