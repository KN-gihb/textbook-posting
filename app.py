from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # フラッシュメッセージ用のシークレットキー
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add-book', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        condition = request.form['condition']
        price = request.form['price']
        contact_email = request.form['contact_email']
        password = request.form['password']

        password_hash = generate_password_hash(password)
        new_book = Book(title=title, author=author, isbn=isbn, condition=condition, price=price, contact_email=contact_email, password_hash=password_hash)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('post.html')

@app.route('/remove-book/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        password = request.form['password']
        if check_password_hash(book.password_hash, password):
            db.session.delete(book)
            db.session.commit()
            flash('投稿が削除されました。')
            return redirect(url_for('index'))
        else:
            flash('パスワードが間違っています。')

    return render_template('delete.html', book=book)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
