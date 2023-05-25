from flask import Flask, render_template, request, redirect, url_for
from Chat import Chat

app = Flask(__name__)
messages = []
chat = Chat(project_id='palm-386622',
                model_name='chat-bison@001',
                temperature=0.5,
                max_output_tokens=256,
                top_p=0.9,
                top_k=40)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        messages.append('You: ' + message)
        response = chat.send_message(message)
        messages.append('Bard: ' + response)
        return redirect(url_for('index'))
    else:
        return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
