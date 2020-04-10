import datetime

from flask import Flask, redirect, render_template, session, flash, url_for, request, abort, jsonify
from application import app, db
from goodreads import get_good_reads_review, get_book_cover
from forms import LoginForm, RegisterForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/", methods=['GET', 'POST'])
def index():
    search_option = request.form.get("search_option")
    search_text = request.form.get("search_text")

    if search_text is None:
        books = db.execute("SELECT * FROM books").fetchall()
    else:
        books = db.execute("SELECT * FROM books WHERE " + search_option + " iLIKE '%" + search_text + "%'").fetchall()

    if not books:
        flash("Sorry, no results. Try selecting ISBN, Title or Author and doule-check the spelling.", "warning")

    return render_template('index.html', books=books)


@app.route("/isbn/<string:isbn>", methods=['GET', 'POST'])
def isbn(isbn):
    # Fetch the book details
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    good_read_review = get_good_reads_review(isbn)
    review_count = good_read_review['books'][0]['work_ratings_count']
    average_score = good_read_review['books'][0]['average_rating']
    book_cover = get_book_cover(isbn)

    # Fetch the reviews
    reviews = db.execute(
        "SELECT first_name, last_name, rate, comment, date, isbn_no FROM reviews LEFT JOIN users ON users.id = reviews.user_id WHERE reviews.isbn_no = :isbn",
        {"isbn": isbn}).fetchall()

    form = ReviewForm()

    # Check is a logged user is posting a review
    if request.method == 'POST':
        if session.get('user_id') is None:
            flash("You need to log in to write a review", "danger")
        elif db.execute("SELECT * FROM reviews WHERE user_id = :user_id and isbn_no = :isbn",
                        {"user_id": session.get('user_id'), "isbn": isbn}).rowcount != 0:
            flash("Oops! You already reviewed this book!", "danger")
        else:
            rate = form.rate.data
            review = form.review.data
            user_id = session.get('user_id')
            db.execute(
                "INSERT INTO reviews (rate, comment, user_id, isbn_no, date) VALUES (:rate, :comment, :user_id, :isbn_no, :date)",
                {"rate": rate, "comment": review, "user_id": user_id, "isbn_no": isbn,
                 "date": datetime.datetime.today().strftime('%d-%m-%Y')})
            db.commit()
            flash("Thank you for reviewing this book!", "success")
        return redirect(url_for('isbn', isbn=isbn))
    else:
        return render_template('isbn.html', book=book, form=form, ratings_count=review_count, avg_rating=average_score,
                               cover=book_cover, reviews=reviews)


@app.route("/api/<string:isbn>", methods=['GET'])
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "ISBN number not found!"}), 404
    else:
        good_read_review = get_good_reads_review(isbn)
        review_count = good_read_review['books'][0]['work_ratings_count']
        average_score = good_read_review['books'][0]['average_rating']
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_count,
            "average_score": average_score
        })


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('usename'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = db.execute(
            "INSERT INTO users (email, password, first_name, last_name) VALUES (:email, :password, :first_name, :last_name)",
            {"email": email, "password": generate_password_hash(password), "first_name": first_name,
             "last_name": last_name})
        db.commit()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))

    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone()
        if user and check_password_hash(user.password, password):
            flash(f"{user.first_name}, you are sucessfully logged in!", "success")
            session['user_id'] = user.id
            session['username'] = user.first_name
            return redirect(url_for('index'))
        else:
            flash("Sorry, wrong username or password.", "danger")
    return render_template("login.html", title="login", form=form, login=True)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))
