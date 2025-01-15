from flask import Flask, render_template, request, redirect, url_for # type: ignore
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)

# メッセージを保存するデータベース
db_url = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URL'] = db_url
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    pub_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    name=db.Column(db.Text())
    article = db.Column(db.Text())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, pub_date, name, article, thread_id):
        self.pub_date = pub_date
        self.name = name
        self.article = article
        self.thread_id = thread_id

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threadname = db.Column(db.String(80))
    articles = db.relationship('Article', backref='thread', lazy=True)

    def __init__(self, threadname, articles=[]):
        self.threadname = threadname
        self.articles = articles

@app.route("/")
def myproject():
    text = Article.query.all()
    return render_template("index.html",lines = text)

@app.route("/")
def main():
    threads = Thread.query.all()
    return render_template("index.html", threads=threads)

@app.route("/thread", methods=["POST"])
def thread():
    thread_get = request.form["thread"]
    threads = Thread.query.all()
    thread_list = []
    threads = Thread.query.all()
    for th in threads:
        thread_list.append(th.threadname)
    if thread_get in thread_list:
        thread = Thread.query.filter_by(threadname=thread_get).first()
        articles = Article.query.filter_by(thread_id=thread.id).all()
        return render_template("thread.html",
                                articles=articles,
                                thread=thread_get)
    else:
        thread_new = Thread(thread_get)
        db.session.add(thread_new)
        db.session.commit()
        articles = Article.query.filter_by(thread_id=thread_new.id).all()
        return render_template("thread.html",
                                articles=articles,
                                thread=thread_get)

@app.route("/result", methods=["POST"])
def result():
    date = datetime.now()
    article = request.form["article"]
    name = request.form["name"]
    thread = request.form["thread"]
    thread = Thread.query.filter_by(threadname=thread).first()
    admin = Article(pub_date=date, name=name, article=article, thread_id=thread.id)
    db.session.add(admin)
    db.session.commit()
    return render_template("bbs_result.html", article=article, name=name, now=date)

if __name__ == "__main__":
    app.run(debug=True)
