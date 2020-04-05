from flask import Flask, redirect, render_template, session, flash, url_for, request
from application import app, db
from goodreads import getGoodReadsReview, getBookCover
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
    '''   if 'username' in session:
         return 'Logged in as %s' % escape(session['username'])
    '''

@app.route("/isbn/<string:isbn>", methods=['GET', 'POST'])
def isbn(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    good_reads_isbn = getGoodReadsReview(isbn)
    ratings_count = good_reads_isbn['books'][0]['work_ratings_count']
    avg_rating = good_reads_isbn['books'][0]['average_rating']

    book_cover = getBookCover(isbn)
    # when user is posting a review
    form = ReviewForm()

    if request.method == 'POST':
        rate = form.rate.data
        review = form.review.data
        user_id = session.get('user_id')
        db.execute("INSERT INTO reviews (rate, comment, user_id, isbn_no) VALUES (:rate, :comment, :user_id, :isbn_no)", {"rate": rate, "comment": review, "user_id": user_id, "isbn_no": isbn})
        db.commit()
        flash("Thank you for reviwing this book!", "success")

    return render_template('isbn.html', book=book, form=form, ratings_count=ratings_count, avg_rating=avg_rating, cover=book_cover)


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
        user = db.execute("INSERT INTO users (email, password, first_name, last_name) VALUES (:email, :password, :first_name, :last_name)", {"email": email, "password": generate_password_hash(password), "first_name": first_name, "last_name": last_name})
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
