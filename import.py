import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

f = open("resources/seeds/books.csv")
reader = csv.reader(f)
for isbn, title, author, year in reader: #loop gives each column a name
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
    print(f"Added book {title} to Book Reviews")
db.commit()
