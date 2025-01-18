from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask アプリケーションの作成
app = Flask(__name__)
# SQLite データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bbs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# データベースのモデル定義
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

# データベースの初期化
with app.app_context():
    db.create_all()

# トップページ
@app.route('/')
def index():
    threads = Thread.query.order_by(Thread.date.desc()).all()
    return render_template('index.html', threads=threads)

# スレッド詳細ページ
@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.date.desc()).all()
    return render_template('thread.html', thread=thread, posts=posts)

# スレッドを作成する処理
@app.route('/add_thread', methods=['POST'])
def add_thread():
    title = request.form['title']

    if not title:
        return "スレッドタイトルは必須です。", 400

    new_thread = Thread(title=title)
    db.session.add(new_thread)
    db.session.commit()
    return redirect('/')

# 投稿を追加する処理
@app.route('/thread/<int:thread_id>/add_post', methods=['POST'])
def add_post(thread_id):
    name = request.form['name']
    content = request.form['content']

    if not name or not content:
        return "名前と投稿内容は必須です。", 400

    new_post = Post(thread_id=thread_id, name=name, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('thread', thread_id=thread_id))

# テンプレート用HTML (templates/index.html)
index_html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>簡易掲示板</title>
</head>
<body>
    <h1>簡易掲示板</h1>
    <form action="/add_thread" method="post">
        <p>
            スレッドタイトル: <input type="text" name="title">
        </p>
        <button type="submit">スレッド作成</button>
    </form>

    <h2>スレッド一覧</h2>
    {% for thread in threads %}
        <div>
            <p><a href="/thread/{{ thread.id }}">{{ thread.title }}</a> ({{ thread.date.strftime('%Y-%m-%d %H:%M:%S') }})</p>
            <hr>
        </div>
    {% endfor %}
</body>
</html>
"""

# テンプレート用HTML (templates/thread.html)
thread_html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ thread.title }}</title>
</head>
<body>
    <h1>{{ thread.title }}</h1>
    <form action="/thread/{{ thread.id }}/add_post" method="post">
        <p>
            名前: <input type="text" name="name">
        </p>
        <p>
            投稿内容:<br>
            <textarea name="content" rows="4" cols="50"></textarea>
        </p>
        <button type="submit">投稿</button>
    </form>

    <h2>投稿一覧</h2>
    {% for post in posts %}
        <div>
            <p><strong>{{ post.name }}</strong> ({{ post.date.strftime('%Y-%m-%d %H:%M:%S') }})</p>
            <p>{{ post.content }}</p>
            <hr>
        </div>
    {% endfor %}
    <p><a href="/">トップに戻る</a></p>
</body>
</html>
"""

if __name__ == '__main__':
    # HTML テンプレートをファイルに書き込む
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html_template)

    with open('templates/thread.html', 'w', encoding='utf-8') as f:
        f.write(thread_html_template)

    # アプリケーションの実行
    app.run(debug=True)
