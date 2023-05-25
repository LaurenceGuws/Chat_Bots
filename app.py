import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Chat import Chat

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
chat = Chat(project_id='palm-386622',
 model_name='chat-bison@001',
 temperature=0.5,
 max_output_tokens=256,
 top_p=0.9,
 top_k=40)

class Conversation(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(80), nullable=False)
 messages = db.relationship('Message', backref='conversation', lazy=True)

class Message(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 user = db.Column(db.String(80), nullable=False)
 text = db.Column(db.String(120), nullable=False)
 conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

if os.path.isfile('instance/chat.db'):
    with app.app_context():
        print('')
else:
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    if request.method == 'POST':
        message = request.form['message']
        messages = request.args.getlist('messages')
        print('message:'+message)
        conversation_id = request.args.get('conversation_id')
        print(f'conversation_id: {conversation_id}')
        if conversation_id:
            conversation = Conversation.query.get(conversation_id)
        else:
            conversation = Conversation(name=message)
            db.session.add(conversation)
            db.session.commit()
            conversation_id = db.session.query(db.func.max(Conversation.id)).scalar()
            print(f'conversation_id: {conversation_id}')
        
        if message is not None:
            messages.append('You: ' + message)
            message_obj = Message(user='You', text=message, conversation_id=conversation.id)
            db.session.add(message_obj)
        response = chat.send_message(message)
        if message is not None:
            messages.append('Bard: ' + response)
            print('bard: '+response)
            message_obj = Message(user='Bard', text=response, conversation_id=conversation.id)
            db.session.add(message_obj)
            db.session.commit()
        return render_template('index.html', messages=messages, conversation_id=conversation_id)
    else:   
        return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
