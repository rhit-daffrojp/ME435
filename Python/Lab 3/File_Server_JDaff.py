import flask

app = flask.Flask(__name__, static_url_path="", static_folder="Public")

@app.route("/")     # Naked Domain
#def handle_naked_domain():
def handle_naked_domain():
    return flask.redirect("/index.html")#"Hello, World!!! Hi Dr. Fisher!"




if __name__ == "__main__":
    print("Running Flask!")
    app.run(host="0.0.0.0", port=8080, debug=True)#, use_reloader=False)