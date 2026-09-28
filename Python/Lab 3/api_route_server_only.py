import flask
 
app = flask.Flask(__name__,static_url_path='', static_folder='public')
 
@app.get('/')
def handle_naked_domain():
    return flask.redirect("/api/hello/Eric")

@app.get("/api/hello/<name>")
def hello_name(name):
    return f"Hello, {name}!"
 
if __name__ == '__main__':
    print("Running flask!")
    app.run(host = '0.0.0.0', port = 8082, debug=True) # use_reloader=False