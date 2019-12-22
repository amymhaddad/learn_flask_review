from flask import Flask, render_template, abort, request, url_for, redirect, flash

from model import db, save_db

from templates.forms import BookmarkForm


app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "~t\xef\xf4\xfe\xad\xb89\x84\x81\xa7\xf9>\x9e\x92\xed\xf0>\x95\x16\x0em\x00\x91\xf4\x81"


@app.route("/")
def welcome():
    return render_template("welcome.html", cards=db)


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template(
            "card.html", card=card, index=index, max_index=len(db) - 1
        )
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form["question"], "answer": request.form["answer"]}
        db.append(card)
        save_db()
        flash(f"Stored card {card}")
        return redirect(url_for("card_view", index=len(db) - 1))
    else:
        return render_template("add_card.html")


@app.route("/delete_card", methods=["POST", "GET"])
def delete_card():
    if request.method == "POST":
        card = {"question": request.form["question"], "answer": request.form["answer"]}

        db.remove(card)
        save_db()

        return redirect(url_for("welcome"))
    else:
        return render_template("delete_card.html")


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    if request.method == "POST":
        try:
            card = db[index]
            db.remove(card)
            save_db()
            return redirect(url_for("welcome", cards=db))
        except IndexError:
            abort(404)
    else:
        return render_template("remove_card.html", card=db[index])


@app.route("/add_bookmark", methods=["GET", "POST"])
def add_bookmark():

    form = BookmarkForm()

    if form.validate_on_submit():

        url = form.url.data
        description = form.description.data
        db.append(url)
        save_db()
        flash(f"Stored {description}")
        return redirect(url_for("welcome"))

    return render_template("add_bookmark.html", form=form)
