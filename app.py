from distutils.log import debug 
from fileinput import filename 
from flask import *  
import pdf_reader
from pdf_reader import load_db, load_db_sum
from langchain.memory import ConversationBufferMemory
from werkzeug.exceptions import InternalServerError, BadRequest, MethodNotAllowed


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
        api_key = request.form['api_key']

        # Check if the file has a ".pdf" file extension
        if f.filename.endswith(".pdf") and api_key != "":
            f.filename = "upload.pdf"
            global file
            file = f.filename
            # Use the custom path along with the original file name
            f.save(f.filename)

            # create a global variable for the chat
            global chat
            chat = load_db(file, api_key)

            # create a global variable for the summary
            global summary
            summary = load_db_sum(file, api_key)

            # create a global variable for the history
            global history
            history = {}
            conversation = {}
            
            return render_template("chatbot.html", name=f.filename, history=history, conversation=conversation, summary=summary)
        elif f.filename.endswith(".pdf") == False:
            return render_template("index.html", error_text="Only PDF files are allowed for upload.")
        elif api_key == "":
            return render_template("index.html", error_text="Please enter your OpenAI API key.")

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
    
# Internal Server Error reroute
@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return render_template("index.html", error_text="The API key you entered was invalid, please enter your OpenAI API key.")

# Bad Request Error reroute
@app.errorhandler(BadRequest)
def handle_bad_reqeust_error(e):
    return render_template("index.html")

# Method Not Allowed Error reroute
@app.errorhandler(MethodNotAllowed)
def handle_bad_reqeust_error(e):
    return render_template("index.html")

if __name__ == '__main__':   
    app.run(debug=True)


