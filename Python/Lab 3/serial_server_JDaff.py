import flask
import plateloader
import threading


app = flask.Flask(__name__, static_url_path="", static_folder="Public")

serial_lock = threading.Lock()
loader = plateloader.PlateLoader("/dev/ttyACM1") # TODO: Set the Port if needed.
# "/dev/ttyUSB0"

@app.get("/")     # Naked Domain
def handle_naked_domain():
    return flask.redirect("/index.html")

@app.get("/api/<command>")
def handle_plateloader_commands(command):
    with serial_lock:
        response = loader.send_command(command)
    return response


if __name__ == "__main__":
    print("Running Flask!")
    loader.connect()
    try:
        app.run(host="0.0.0.0", port=8082, use_reloader=False) #debug=True)
    finally:
        print("Disconnecting plate loader")
        loader.disconnect()