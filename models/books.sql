CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE author (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    category_id INTEGER,
    author_id INTEGER,
    pages INTEGER,
    release_year INTEGER,
    FOREIGN KEY (category_id) REFERENCES category (id),
    FOREIGN KEY (author_id) REFERENCES author (id)
);

INSERT INTO category (id, name) VALUES (1, 'Science Fiction');
INSERT INTO category (id, name) VALUES (2, 'Fantasy');

INSERT INTO author (id, name) VALUES (1, 'Isaac Asimov');
INSERT INTO author (id, name) VALUES (1, 'J.R.R. Tolkien');

INSERT INTO book (id, name, category_id, author_id, pages, release_year) VALUES (1, 'Foundation', 1, 1, 255, 1951);
INSERT INTO book (id, name, category_id, author_id, pages, release_year) VALUES (2, 'The Hobbit', 2, 2, 310, 1937);
INSERT INTO book (id, name, category_id, author_id, pages, release_year) VALUES (3, 'The Lord of the Rings', 2, 2, 1178, 1954);
