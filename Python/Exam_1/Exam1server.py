import flask
import flash
import threading

app = flask.Flask(__name__, static_url_path="", static_folder="Public")
serial_lock = threading.Lock()
loader = flash.Flash("/dev/ttyACM0") # TODO: Set the Port if needed.

@app.get("/")     # Naked Domain
def handle_naked_domain():
    return flask.redirect("/index.html")

@app.get("/api/led/<command>")
def handle_led_toggle_commands(command):
    with serial_lock:
        # response = loader.send_command(command)
        response = loader.send_command("LED "+ command)
    return response

@app.get("/api/flash/<numFlashes>/<periodMs>")
def handle_flash_commands(numFlashes, periodMs):
    with serial_lock:
        response = loader.send_command("FLASH "+numFlashes+ " " + periodMs)
    return response

if __name__ == "__main__":
    print("Running Flask!")
    loader.connect()
    try:
        app.run(host="0.0.0.0", port=8080, use_reloader=False) #debug=True)
    finally:
        print("Disconnecting")
        loader.disconnect()