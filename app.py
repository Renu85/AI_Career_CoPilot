from flask import Flask, render_template, request, redirect, session
from db import Base, engine, SessionLocal
import models
import PyPDF2
import docx
import json
from dotenv import load_dotenv
load_dotenv()
from analyzer import analyze_resume



app = Flask(__name__)
app.secret_key = "*********"

Base.metadata.create_all(bind=engine)

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


#HOME
@app.route("/")
def home():
    if "user" in session:
         return redirect("/dashboard")
    return redirect("/login")

#-----SINGUP

@app.route("/signup", methods=["GET", "POST"])
def signup():
    db = SessionLocal()

    if request.method =="POST":
        email=request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(models.Users).filter_by(email).first()
        if existing_user:
            return "User already exists"
        
        user = models.Users(email=email, password=password)
        db.add(user)
        db.commit()
 
        return redirect("/login")
    
    return render_template("/signup.html")


#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    db = SessionLocal()

    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(models.Users).filter_by(email=email, password=password).first()
        
        if user:
            session["user"]=user.email
            return
            redirct("/dashboard")
        else:
            return
            "Invalid credentials"
        
    return render_template("login.html")
    
#DASHBOAD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    
    result = None

    if request.method == "POST":
        user_goal=request.form.get("role")
        resume_text = request.form.get("resume")

        file= request.files.get("file")

    #File Handling

        if file and file.name  !="":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text=""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text=text
                except Exception as e:
                    result={"error": f"PDF error: {str(e)}" }
            elif file.filename.endswith(".docx"):
                try:
                    doc= docx.Document(file)
                    text=""
                    for para in doc.paragraphs:
                        text += para.text+"\n"
                    resume_text =text
                except Exception as e:
                    result = {"error:" f"Docx error:{str(e)}"}
                

        if resume_text and user_goal:
            try:
                result = analyze_resume(resume_text, user_goal)

                #Save to db

                db= SessionLocal()
                user = db.query(models.User).filter_by(email=session["user"]).fisrt()

                report = models.Reports(
                user_id = user.id,
                resume_text = resume_text,
                result = json.dumps(result)

                 )

                db.add(report)
                db.commit()

            except Exception as e:
              result={"error":f"AI error: {str(e)}"}
            return render_template(
            "dashboard.html",
             user=session["user"],
             result = result
             )           

#History

@app.route("/history")
def history(): 
    if "user" not in session:
        return redirect("/login")

    db=SessionLocal()
    user = db.query(models.Users).filter_by(email=session["user"]).first()

    reports= db.query(models.Reports).filter_by(user_id = user.id).all()


   
    
#Convert json > dict 

    parsed_reports= []
    for r in reports:
         try:
          parsed_result = json.loads(r.result)
         except:
          parsed_result=[]

          parsed_reports.append({
            "resume":r.resume_text,
            "result":parsed_result
        })
        
          return render_template("history.html", reports=parsed_reports)
        


#Logout routedir

@app.route("/user")
def logout():
    session.pop("user")
    return redirect("/logout")

 

if __name__ == "__main__":
    app.run(debug=True)

      