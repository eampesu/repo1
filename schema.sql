CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE areas (id SERIAL PRIMARY KEY, topic TEXT, secret BOOLEAN); 
CREATE TABLE chains (id SERIAL PRIMARY KEY, area_id INTEGER REFERENCES areas, user_id INTEGER REFERENCES users, topic TEXT, content TEXT, created_at TIMESTAMP); 
CREATE TABLE messages (id SERIAL PRIMARY KEY,  chain_id INTEGER REFERENCES chains, user_id INTEGER REFERENCES users, content TEXT , created_at TIMESTAMP);
CREATE TABLE secret_users (id SERIAL PRIMARY KEY, area_id INTEGER REFERENCES areas, user_id INTEGER REFERENCES users);

