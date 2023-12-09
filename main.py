from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(300), default=datetime.utcnow())


    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<string:name>&<int:id>')
def user(name, id):
    return f'{name} and {id}'


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles) #шаблон можно назвать и не артиклес
#элеменет артикла - словарь, ключи - колонки


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id) # better use get_or_404
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id) # better use get_or_404
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'delete error'

@app.route('/posts/<int:id>/update')
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Status error'
    else:
        return render_template("post_update.html", article=article)


@app.route('/article', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']#name of input
        article = Article(title=title, intro=intro)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Status error'
    else:
        return render_template("article.html")


if __name__ == '__main__':
    app.run(debug=True)
