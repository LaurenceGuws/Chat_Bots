import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from Chat import Chat
from werkzeug.utils import secure_filename
import zipfile


def get_conversation_names():
    conversation_names = [row[0] for row in db.session.query(Conversation.name).all()]
    return conversation_names

def get_conversation_id(conversation_name):
    conversation_id = db.session.query(Conversation.id).filter(Conversation.name == conversation_name).scalar()
    return conversation_id

def load_messages(conversation_id):
    messages = [row[0] for row in db.session.query(Message.text).filter(Message.conversation_id == conversation_id).all()]
    session['messages'] = messages
    return messages

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
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
        print('DB already created')
else:
    with app.app_context():
        print('Creating DB in /instances dir.')
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        messages = session['messages']
        # need to figure out how to add conversation_id here
        if session.get('conversation_id') is None:
            conversation = Conversation(name=message)
            db.session.add(conversation)
            db.session.commit()
            conversation_id = db.session.query(db.func.max(Conversation.id)).scalar()
            session['conversation_id'] = conversation_id
        conversation_id = session['conversation_id']
        name = session['model_name']

        if message is not None:
            messages.append(message)
            message_obj = Message(user='You', text=message, conversation_id=conversation_id)
            db.session.add(message_obj)
        if session['model_name'] == 'bard':
            response = chat.send_bard_message(message)
            if message is not None:
                messages.append(response)
                message_obj = Message(user='Bard', text=response, conversation_id=conversation_id)
                db.session.add(message_obj)
                db.session.commit()
                session['messages'] = messages
        if session['model_name'] == 'gpt_35_turbo':
            response = chat.chat_gpt_interact(session['messages'])
            if message is not None:
                messages.append(response)
                message_obj = Message(user='gpt', text=response, conversation_id=conversation_id)
                db.session.add(message_obj)
                db.session.commit()
                session['messages'] = messages
        
        return render_template('index.html')
    else:   
        if session.get('messages') is None:
            session['messages'] = []
            session['model_names'] = ['gpt_35_turbo','bard']
            session['model_name'] = 'bard'
        return render_template('index.html')
    
@app.route('/conversations')
def conversations():
    conversation_names = get_conversation_names()
    # render a template with the conversation names
    return render_template('conversations.html', conversation_names=conversation_names)

@app.route('/postfile', methods=['GET', 'POST'])
def postfile():
    if request.method == 'POST':
            # Handling File Uploads
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '':
                    # if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    if filename.rsplit('.', 1)[1].lower() == 'zip':
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(app.config['UPLOAD_FOLDER'])
    return render_template('index.html')

@app.route('/models')
def goto_models():
    session['model_names'] = ['gpt_35_turbo','bard']
    return render_template('models.html', model_names=session['model_names'])

@app.route('/goto_conversation', methods=['POST'])
def goto_new_conversation():
    conversation_name = request.form['conversation_name']
    session['conversation_id'] = get_conversation_id(conversation_name)
    session['messages'] = load_messages(session['conversation_id'])
    return redirect(url_for('index'))

@app.route('/goto_model', methods=['POST'])
def goto_new_model():
    model_name = request.form['model_name']
    session['model_name'] = model_name
    print(f'model name changed to : ' + session['model_name'])
    return redirect(url_for('index'))   

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
