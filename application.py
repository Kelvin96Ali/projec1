from flask import Flask, request, render_template, jsonify, session, flash, redirect
from dotenv import load_dotenv
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import login_required
import os
import requests
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Tu clave de API de Google Books
GOOGLE_BOOKS_API_KEY = 'AIzaSyB6ixcKe_VngRjPOUyAh3-um7PogrW-DGk'

@app.route('/')
def home():
    return render_template('index.html')


"""@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if query:
        # Llamar a la API de Google Books con tu clave de API
        google_books_api_url = 'https://www.googleapis.com/books/v1/volumes'
        params = {'q': query, 'key': GOOGLE_BOOKS_API_KEY}
        response = requests.get(google_books_api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            books = data.get('items', [])
            return render_template('search.html', books=books)
        else:
            return 'Error en la búsqueda'
"""

        
@app.route("/log")
@login_required
def log():
    
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        rows = db.execute(text("SELECT * FROM users WHERE username = :username"),
                  {"username": request.form.get("username")}).fetchone()

        result = rows  # No es necesario llamar a fetchone() nuevamente

        if result == None or not check_password_hash(result[2], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        session["user_id"] = result[0]
        session["user_name"] = result[1]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    """
    Log user out
    """

    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        userCheck = db.execute(text("SELECT * FROM users WHERE username = :username"),
                      {"username": request.form.get("username")}).fetchone()

        if userCheck:
            return render_template("error.html", message="username already exist")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        elif not request.form.get("confirmation"):
            return render_template("error.html", message="must confirm password")

        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("error.html", message="passwords didn't match")

        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        db.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"),
            {"username": request.form.get("username"),
             "password": hashedPassword})

        db.commit()

        flash('Account created', 'info')

        return redirect("/login")

    
    else:
        return render_template("register.html")

@app.route("/searchs", methods=["POST"])

def search_books():
    
    print(request.form.get("book"))

    """if not request.form.get("book"):
        return render_template("error.html", message="Please enter the Book Description.")

    
    searchs =  request.form.get("book").upper() 

    
    query = query.title()

    query = text("SELECT * FROM books WHERE upper(isbn) LIKE :search or upper(title) LIKE :search or upper(author) LIKE :search limit 100 ")
    rows = db.execute(query, {"search": f"%{searchs}%"}).fetchall()

    rows = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query LIMIT 15",
                        {"query": query})

    print(rows)
  
    if rows == 0:
        return render_template("error.html", message="No description available for this book.")"""
    

    if request.method == "POST":
        book_description = request.form.get("book")

        if not book_description:
            return render_template("error.html", message="Please enter a book description.")

        search_query = "%" + book_description + "%"  # Mantener la entrada original

        query = text("SELECT * FROM books WHERE isbn ILIKE :search OR title ILIKE :search OR author ILIKE :search LIMIT 100")
                     
                     
        rows = db.execute(query, {"search": f"{search_query}"}).fetchall()

        print(rows)

        query1 = text("SELECT * FROM books")

        

        if not rows:
            return render_template("error.html", message="No description available for this book.")

    return render_template("results.html", rows=rows)

@app.route('/book/<isbn>', methods=['GET', 'POST'])
def book(isbn):
    if request.method == "POST":
        
        currentUser = session.get("user_id")

        
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        
        row = db.execute(text("SELECT isbn FROM books WHERE isbn = :isbn"),
                {"isbn": isbn})


        
        bookId = row.fetchone()
        bookId = bookId[0]

        
        row2 = db.execute(text("SELECT * FROM reviewss WHERE user_id = :user_id AND book_id = :book_id"),
                  {"user_id": currentUser, "book_id": bookId})


        
        if row2.rowcount == 1:
            flash('You already submitted a review for this book', 'warning')
            return redirect("/book/" + isbn)

        
        rating = int(rating)

        db.execute(text("INSERT INTO reviewss (user_id, book_id, comment, rating) VALUES \
                (:user_id, :book_id, :comment, :rating)"),
           {"user_id": currentUser,
            "book_id": bookId,
            "comment": comment,
            "rating": rating})


        db.commit()

        flash('Review submitted!', 'info')

        return redirect("/book/" + isbn)
    else:
        row = db.execute(text("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn"),
                 {"isbn": isbn})


        bookInfo = row.fetchall()

        key = os.getenv("AIzaSyB6ixcKe_VngRjPOUyAh3-um7PogrW-DGk")

        query = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key": key, "isbns": isbn})

        
        response = query.json()

        response = response['books'][0]

        
        bookInfo.append(response)

        
        row = db.execute(text("SELECT isbn FROM books WHERE isbn = :isbn"),
                 {"isbn": isbn})

        book = row.fetchone() 
        book = book[0]

        results = db.execute(text("SELECT users.username, comment, rating, "
                          "to_char(time, 'DD Mon YY - HH24:MI:SS') as time "
                          "FROM users "
                          "INNER JOIN reviewss "
                          "ON users.id = reviewss.user_id "
                          "WHERE book_id = :book "
                          "ORDER BY time"),
                     {"book": book})

        reviews = results.fetchall()

        return render_template("book.html", bookInfo=bookInfo, reviews=reviews)


@app.route("/api/<isbn>", methods=['GET'])
def api_call(isbn):
    print(session.get("user_id")
)
    row = db.execute(text("SELECT title, author, year, isbn, \
                    COUNT(reviewss.id) as review_count, \
                    AVG(reviewss.rating) as average_score \
                    FROM books \
                    INNER JOIN reviewss \
                    ON books.isbn = reviewss.book_id \
                    WHERE isbn = :isbn \
                    GROUP BY title, author, year, isbn"),
                    {"isbn": isbn}).all()
    print(row)
    return ("hello my friends")
    """"url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'"
    "response = requests.get(url)
    data = response.json()
#crear el diccionario# pasas el jsofi#
#agregar rese'as
    if row.rowcount != 1:
        return jsonify({"Error": "Invalid book ISBN"}), 422

    tmp = row.fetchone()
    result = dict(tmp.items())
    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)"""


if __name__ == '__main__':
    app.run(debug=True,port=5000)

