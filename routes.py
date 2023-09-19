from app import app
from flask import render_template, request
import areas
#import messages
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    list=areas.get_list()
    return render_template("list_of_areas.html", areas=list)

#@app.route("/message", id)
#def message():
#    return render_template("message.html", id=id)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/check_login", methods=["GET", "POST"])
def check_login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/list")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message="Salasanat eroavat")
    if users.register(username, password):
        return redirect("/list")
    else:
        return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/answers(<int:id>)")
def answers(id):
    list=answers.get_list(id)
    return render_template("list_answers.html", list=list)

@app.route("/chains(<int:id>)")
def chains(id):
    chains_list=chains.get_list(id)
    if bool(chains_list):
        return render_template("zero_chains.html", area_id=id)
    return render_template("list_of_chains.html", chains=chains_list)

@app.route("/new_chain")
def new_chain():
    id=request.form["area_id"]
    return render_template("new_chain.html", area_id=id)

@app.route("/chain(<int:id>)")
def chain(id):
    first=chains.get_topic(id)
    chain_list=chains.get_messages(id)
    return render_template("chain.html",first=first, messages=chain_list)

@app.route("/answer(<int>:id)")
def answer(id):
    return render_template("answer.html", chain_id=id)

@app.route("/add_answer", methods=["POST"])
def add_answer():
    user_id=users.user_id()
    chain_id=request.form["chain_id"]
    answers.add(request.form["content"],request.form["chain_id"], user_id)
    return redirect("/answers(chain_id)")

