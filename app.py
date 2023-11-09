from distutils.log import debug 
from fileinput import filename 
from flask import *  
import pdf_reader
from pdf_reader import load_db, load_db_sum
from langchain.memory import ConversationBufferMemory



app = Flask(__name__, static_folder='static')   
from flask_session import Session
 
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define bot
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
        
def success():
    if request.method == 'POST':
        f = request.files['file']

        # Check if the file has a ".pdf" file extension
        if f.filename.endswith(".pdf"):
            f.filename = "upload.pdf"
            global file
            file = f.filename
            # Use the custom path along with the original file name
            f.save(f.filename)
            global chat
            chat = load_db(file)
            summ = load_db_sum(file)
            global history
            history = {}
            conversation = {}
            global summary
            summary_result = summ({"question": "Can you summarize in detail?"})
            summary = str(summary_result['answer'])

            
            return render_template("chatbot.html", name=f.filename, history=history, conversation=conversation, summary=summary)
        else:
            return render_template("index.html", error_text="Only PDF files are allowed for upload.")

history = {}
conversation = {}
@app.route('/chatbot', methods=['GET', 'POST'])  

def pdf():
    user_input = request.form['user_input']
    result = chat({"question": user_input})
    answer_text = str(result['answer'])
    question_text = str(result['question'])
    user = "User: "
    chatbot = "Chat Bot: "
    conversation.update({user: question_text, chatbot: answer_text})
    history.update({question_text : answer_text})
    return render_template('chatbot.html', answer_text=answer_text, question_text=question_text, history = history, conversation = conversation, summary = summary)
    

if __name__ == '__main__':   
    app.run(debug=True)


