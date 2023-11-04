from distutils.log import debug 
from fileinput import filename 
from flask import *  
import pdf_reader
from pdf_reader import load_db



app = Flask(__name__)   
  
# importing function for calculations
from basic_calculator_function import basic_calculator

# Define calculator
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
# def predict():
#     loaded_file = "./docs/Anthony_ResumeATS.pdf"
#     chat = load_db(loaded_file,"stuff", 4)
#     user_input = request.form['user_input']
#     result = chat({'question': user_input})

#     return render_template('index.html', prediction_text=str(result['answer']))  
        
def success():
    if request.method == 'POST':
        f = request.files['file']

        # Check if the file has a ".pdf" file extension
        if f.filename.endswith(".pdf"):
            f.filename = "upload.pdf"
            # Use the custom path along with the original file name
            f.save(f.filename)
            
            return render_template("chatbot.html", name=f.filename)
        else:
            return render_template("index.html", error_text="Only PDF files are allowed for upload.")


@app.route('/chatbot', methods=['GET', 'POST'])  

def pdf():
    loaded_file = 'upload.pdf'
    chat = load_db(loaded_file,"stuff", 4)
    user_input = request.form['user_input']
    result = chat({"question": user_input})
    return render_template('chatbot.html', prediction_text=str(result['answer']))
    # return render_template('chatbot.html')
  
if __name__ == '__main__':   
    app.run(debug=True)

