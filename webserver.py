from flask import Flask, request, render_template
import lib
import threading
from Weekday import Weekday
import socket_server as socks
import json
import Task

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')


@app.route('/')
def get_index() -> any:
    return render_template("index.html")


@app.route('/settings', methods=["POST", "GET"])
def http_send_settings() -> str:
    if request.method == "GET":

        lib.log(f"Sending settings back to {request.remote_addr}")
        return json.dumps(lib.serializeSettings())

    elif request.method == "POST":

        lib.log(f"Setting settings to {request.json}")
        print(lib.settings)
        lib.settings.update(lib.parse_settings(request.json))
        print(lib.settings)
        lib.saveSettings()
        return json.dumps(lib.serializeSettings())


@app.route('/add-task', methods=["POST", "GET"])
def http_add_task():
    request_json: dict = request.json
    weekday = request_json.get("day")
    time = request_json.get("time")
    dispense_seconds = int(request_json.get("amount"))
    return lib.add_task_to_schedule_object(Task(Weekday(weekday), time, dispense_seconds))


@app.route("/dispense")
def http_dispense_seconds():
    lib.dispense(int(request.args.get("amount")))
    return {"dispensed": True}


if __name__ == '__main__':
    """
    Creates a second thread that runs the main loop of the machine.
    Then runs the flask api server for incoming orders.
    """

    lib.init()
    main_thread = threading.Thread(target=lib.main, daemon=True)
    main_thread.start()
    socket_thread = threading.Thread(target=socks.start_sockets)
    socket_thread.start()

    app.run()
