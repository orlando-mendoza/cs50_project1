CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  pass VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  surname VARCHAR NOT NULL
);

CREATE TABLE books (
  isbn VARCHAR PRIMARY KEY,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year VARCHAR NOT NULL
);

CREATE TABLE reviews (
  rate DECIMAL(1,1) NOT NULL,
  comment VARCHAR,
  user_id INTEGER REFERENCES users,
  isbn_no VARCHAR REFERENCES books,
  PRIMARY KEY (user_id, isbn_no)
);