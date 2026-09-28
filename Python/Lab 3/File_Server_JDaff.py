import flask

app = flask.Flask(__name__, static_url_path="", static_folder="Public")

@app.get("/")     # Naked Domain
def handle_naked_domain():
    return flask.redirect("/api/hello/JDaff")#"Hello, World!!! Hi Dr. Fisher!"

@app.get("/api/hello/<name>")
def hello_name(name):
    return f"Hello, {name}!!"



if __name__ == "__main__":
    print("Running Flask!")
    app.run(host="0.0.0.0", port=8080, debug=True)#, use_reloader=False)