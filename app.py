from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# メッセージを保存するリスト
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # フォームからメッセージを取得
        message = request.form.get('message')
        if message:
            messages.append(message)
        return redirect(url_for('index'))
    
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
