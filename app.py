
###### NER
from flask import Flask,url_for,render_template,request
import spacy
from spacy import displacy
nlp = spacy.load('en_ner_bc5cdr_md')
nlp_cus = spacy.load(r'model-best')
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
from PyPDF2 import PdfReader
from flaskext.markdown import Markdown
import pandas as pd


app = Flask(__name__)
Markdown(app)




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/success', methods = ['POST'])
def success():
    if request.method == "POST":
        f= request.files['file']
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            docx = nlp(text)
            docx_cus = nlp_cus(text)
            html = displacy.render(docx_cus,style="ent")
            html = displacy.render(docx,style="ent")
            html = html.replace("\n\n","\n")
            a= [(ent.text, ent.label_) for ent in docx.ents]
            a = set(a)
            a = pd.DataFrame(a,columns=('Named Entity', 'Classes'))
            result = HTML_WRAPPER.format(html)
            myfile = open("all_names.txt",'a')
            for ent in docx.ents:
                names = ent.text
                label = (ent.label_)
                results= names +"   ----->  " +label + '\n'
                myfile.write(results)
            myfile.close()
            lines = open("C:/Users/pavva/Documents/NER/all_names.txt", 'r').readlines()
            lines_set = set(lines)
            out  = open("C:/Users/pavva/Documents/NER/all_names.txt", 'w')
            for line in lines_set:
                out.write(line)

    return render_template('results.html',result=result,tables=[a.to_html(classes='data')], titles=a.columns.values)



@app.route('/text', methods=['POST'])
def text():
    if request.method == 'POST':
        raw_text = request.form['rawtext']
        docx_text = nlp(raw_text)
        docx_cus = nlp_cus(raw_text)
        
        html_text = displacy.render(docx_text,style="ent")
        html_text = displacy.render(docx_cus,style="ent")
        html_text = html_text.replace("\n\n","\n")
        result = HTML_WRAPPER.format(html_text)
        df= [(ent.text, ent.label_) for ent in docx_text.ents]
        df = set(df)
        df = pd.DataFrame(df,columns=('Named Entity', 'Classes'))
        myfile = open("all_names.txt",'a')
        for ent in docx_text.ents:
            names = ent.text
            label = (ent.label_)
            results= names +"   ----->  " + label + '\n'
            myfile.write(results)
            myfile.close()
        lines = open("C:/Users/pavva/Documents/NER/all_names.txt", 'r').readlines()
        lines_set = set(lines)
        out  = open("C:/Users/pavva/Documents/NER/all_names.txt", 'w')
        for line in lines_set:
            out.write(line)    
    return render_template('results.html',rawtext=raw_text,result=result,tables=[df.to_html(classes='data')], titles=df.columns.values)
        


@app.route('/save', methods=['POST'])
def fb():
    str = "Your FeedBack is noted."
    if request.method == 'POST':
        fb = request.form['fb']
        with open('feedback.txt', 'a') as f:
            #f.write('\n')
            f.write(fb +'\n')
            #f.write('\n')
            f.close()
    return render_template('feedback.html', str=str)

            
            
            
        



if __name__ == '__main__':
    app.run(debug=True)