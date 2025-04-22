from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os, sqlite3, hashlib

app = Flask(__name__)
app.secret_key = "supersecret2025"

# Create database
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# List of available phrases with GIFs
gif_lst = ['all the best', 'are you sick', 'any questions', 'are you angry',
    'are you busy', 'are you hungry', 'be careful', 'can we meet tomorrow',
    'clean the room', 'did you eat lunch', 'did you finish homework',
    'do you go to office', 'do you have money', 'do you want something to drink',
    'do you watch tv', 'dont worry', 'flower is beautiful', 'good afternoon',
    'good morning', 'good question', 'good evening', 'good night', 'happy journey',
    'what do you want tea or coffee', 'what is your name', 'how many people are in your family',
    'i am a clerk', 'i am bored', 'i am fine', 'i am sorry', 'i am thinking',
    'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
    'i had to say something but i forgot', 'i have a headache', 'i like pink colour',
    'lets go for lunch', 'my mother is a housewife', 'nice to meet you', 'please dont smoke',
    'open the door', 'call me later', 'please call the ambulance', 'give me your pen',
    'please wait for sometime', 'can i help you', 'shall we go together tomorrow',
    'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was a traffic jam',
    'wait i am thinking', 'what are you doing', 'what is the problem', 'what is todays date',
    'what does your father do', 'what is your job', 'what is your age', 'what is your mobile number',
    'whats up', 'when is your interview', 'when will we go', 'where do you live',
    'where is the bathroom', 'where is the police station', 'you are wrong'
]

# Alphabets for individual signs
alphabets = list('abcdefghijklmnopqrstuvwxyz')

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = hashlib.sha256(request.form["password"].encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        return "<h3 style='color:red;'>Invalid login. <a href='/login'>Try again</a></h3>"

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = hashlib.sha256(request.form["password"].encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return redirect(url_for("login_page"))

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login_page"))
    return render_template("dashboard.html")

@app.route("/how_it_works")
def how_it_works():
    if "username" not in session:
        return redirect(url_for("login_page"))
    return render_template("how_it_works.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login_page"))

@app.route("/process_speech", methods=["POST"])
def process_speech():
    text = request.form.get("text", "").lower()
    result = {}

    if text in gif_lst:
        gif_path = f"/static/Indian_Speech_Language_GIFS/{text}.gif"
        if os.path.exists("." + gif_path):
            result["type"] = "gif"
            result["path"] = gif_path
        else:
            result["type"] = "error"
            result["message"] = f"No GIF found for '{text}'."
    else:
        images = []
        for char in text:
            if char in alphabets:
                img_path = f"/static/Alphabets/{char}.jpg"
                if os.path.exists("." + img_path):
                    images.append(img_path)
        if images:
            result["type"] = "alphabets"
            result["paths"] = images
        else:
            result["type"] = "error"
            result["message"] = "No matching images found."

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
