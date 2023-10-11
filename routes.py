from app import app
from flask import render_template, request, redirect, session
import areas
import messages
import users
import chainz
import secretUsers

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    user_id=users.user_id()
    username=users.get_username(user_id)
    admin=users.is_admin(user_id)
    list=areas.get_list()
    slist=areas.get_secret_list()
    return render_template("list_of_areas.html", areas=list, admin=admin, secret_areas=slist, username=username)

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
    #print("admin:", request.form["yes"], request.form["no"])
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
    if users.register(username, password1):
        return redirect("/list")
    else:
        return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/chains/<int:id>")
def chains(id):
    chains_list=chainz.get_list(id)
    if bool(chains_list)==False:
        return render_template("zero_chains.html", area_id=id)
    return render_template("list_of_chains.html", area_id=id, chains=chains_list)

@app.route("/new_chain/<int:id>")
def new_chain(id):
    return render_template("new_chain.html", area_id=id)

@app.route("/chain/<int:id>")
def chain(id):
    user_id=users.user_id()
    username=users.get_username(user_id)
    chain=chainz.get_chain(id)
    chain_list=chainz.get_messages(id)
    return render_template("chain.html", username=username, first=chain, messages=chain_list)

@app.route("/remove_chain/<int:id>")
def remove_chain(id):
    area_id=chainz.get_area(id)
    messages.remove_chain(id)
    chainz.remove(id)
    return redirect("/chains/"+str(area_id))

@app.route("/answer/<int:id>")
def answer(id):
    return render_template("answer.html", chain_id=id)

@app.route("/add_answer", methods=["POST"])
def add_answer():
    user_id=users.user_id()
    chain_id=request.form["chain_id"]
    messages.add(request.form["content"],request.form["chain_id"], user_id)
    return redirect("/chain/"+str(chain_id))

@app.route("/edit_answer", methods=["POST"])
def edit_answer():
    return render_template("edit_answer.html", chain_id=request.form["chain_id"], message_id=request.form["message_id"])

@app.route("/finish_edit", methods=["POST"])
def finish_edit():
    chain_id=request.form["chain_id"]
    messages.edit(request.form["message_id"], request.form["content"])
    return redirect("/chain/" +str(chain_id))

@app.route("/remove_answer", methods=["POST"])
def remove_answer():
    messages.remove(request.form["message_id"])
    chain_id=request.form["chain_id"]
    return redirect("/chain/"+str(chain_id))

@app.route("/add_new_chain", methods=["POST"])
def add_new_chain():
    user_id=users.user_id()
    area_id=request.form["area_id"]
    chainz.add(user_id, request.form["topic"], request.form["content"], request.form["area_id"])
    return redirect("/chains/"+str(area_id))

@app.route("/edit_topic/<int:id>")
def edit_topic(id):
    return render_template("edit_topic.html", chain_id=id)

@app.route("/change_topic", methods=["POST"])
def change_topic():
    chain_id=request.form["chain_id"]
    chainz.change_topic(request.form["chain_id"], request.form["topic"])
    return redirect("/chain/" +str(chain_id))

@app.route("/edit_message/<int:id>")
def edit_message(id):
    return render_template("edit_message.html", chain_id=id)
@app.route("/edit", methods=["POST"])
def edit():
    chain_id=request.form["chain_id"]
    chainz.edit_message(chain_id, request.form["content"])
    return redirect("/chain/"+str(chain_id))

@app.route("/remove_message/<int:id>")
def remove_message(id):
    chainz.remove(id)
    return redirect("/chain/" +str(id))
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/delete_area/<int:id>")
def delete_area(id):
    areas.delete(id)
    return redirect("/list")

@app.route("/new_area")
def new_area():
    return render_template("new_area.html")

@app.route("/add_new_area", methods=["POST"])
def add_new_area():
    if request.form["yesno"]=="Ei":
        areas.add(request.form["topic"], False)
        return redirect("/list")
    elif request.form["yesno"]=="Kyllä":
        userlist=users.get_users()
        topic=request.form["topic"]
        return render_template("choose_users.html", topic=topic, users=userlist)
    else:
        return redirect("/new_area")

@app.route("/new_secret_area", methods=["POST"])
def new_secret_area():
    secret_users=request.form.getlist("user_id")
    topic=request.form["topic"]
    areas.add(topic, True)
    area_id=areas.get_area_id(topic)
    secretUsers.add(area_id, secret_users)
    return redirect("/list")
@app.route("/result")
def result():
    query=request.args["query"]
    finds1=messages.find_normal(query)
    finds2=chainz.find_normal(query)
    if bool(finds1)==False and bool(finds2)==False:
        return render_template("no_match.html")
    return render_template("result.html", messages=finds1, chains=finds2)

@app.route("/secret_result", methods=["GET"])
def secret_result():
    query=request.args["query"]
    finds1=messages.find_secret(query)
    finds2=chainz.find_secret(query)
    uid=users.user_id()
    if bool(finds1)==False and bool(finds2)==False:
        return render_template("no_match.html")
    return render_template("secret_result.html", messages=finds1, chains=finds2, uid=uid)


