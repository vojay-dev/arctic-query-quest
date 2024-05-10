CREATE TABLE player (
    id INTEGER PRIMARY KEY,
    score INTEGER,
    name VARCHAR
);

CREATE TABLE match (
    id INTEGER PRIMARY KEY,
    match_date DATE,
    player1_id INTEGER,
    player2_id INTEGER,
    winner_id INTEGER,
    FOREIGN KEY (player1_id) REFERENCES player (id),
    FOREIGN KEY (player2_id) REFERENCES player (id),
    FOREIGN KEY (winner_id) REFERENCES player (id)
);

CREATE TABLE device (
    id INTEGER PRIMARY KEY,
    manufacturer VARCHAR,
    model VARCHAR
);

CREATE TABLE login (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    device_id INTEGER,
    login_date DATE,
    FOREIGN KEY (player_id) REFERENCES player (id),
    FOREIGN KEY (device_id) REFERENCES device (id)
);

INSERT INTO player (id, score, name) VALUES (1, 100, 'Alice');
INSERT INTO player (id, score, name) VALUES (2, 200, 'Bob');
INSERT INTO player (id, score, name) VALUES (3, 300, 'Charlie');
INSERT INTO player (id, score, name) VALUES (4, 400, 'David');

INSERT INTO match (id, match_date, player1_id, player2_id, winner_id) VALUES (1, '2024-01-01', 1, 2, 2);
INSERT INTO match (id, match_date, player1_id, player2_id, winner_id) VALUES (2, '2024-01-02', 3, 4, 3);
INSERT INTO match (id, match_date, player1_id, player2_id, winner_id) VALUES (3, '2024-01-03', 1, 3, 1);
INSERT INTO match (id, match_date, player1_id, player2_id, winner_id) VALUES (3, '2024-01-03', 1, 4, 2);

INSERT INTO device (id, manufacturer, model) VALUES (1, 'Apple', 'iPhone');
INSERT INTO device (id, manufacturer, model) VALUES (2, 'Samsung', 'Galaxy');
INSERT INTO device (id, manufacturer, model) VALUES (3, 'Google', 'Pixel');

INSERT INTO login (id, player_id, device_id, login_date) VALUES (1, 1, 1, '2024-01-01');
INSERT INTO login (id, player_id, device_id, login_date) VALUES (2, 2, 2, '2024-01-02');
INSERT INTO login (id, player_id, device_id, login_date) VALUES (3, 3, 2, '2024-01-03');
INSERT INTO login (id, player_id, device_id, login_date) VALUES (4, 4, 1, '2024-01-04');
