from wlan_utility import update
from logge import generate_log as logger
from time import sleep
import os
from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

start_hotspot = "/home/pi/start_server.sh"
restart_wifi = "/home/pi/restart_wifi.sh"


def check_wifi():
    for i in range(10):
        try:
            result = subprocess.check_output(
                ("grep", "ESSID"),
                stdin=subprocess.Popen(
                    ["iwgetid"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                ).stdout,
            )
            logger(f"Result: {result}")
            sleep(3)
            break
        except Exception as exc:
            print(exc)
            logger(f"Did not find active connection...{i+1}")
            if i > 8:
                subprocess.run(
                    start_hotspot, shell=True, text=True, stdout=subprocess.PIPE
                ).stdout
                break
            sleep(3)


check_wifi()


@app.get("/")
def home():
    html_content = """
		<!DOCTYOE html>
		<html>
			<head><title>Mind Charger</title></head>
			<body>
				<h1>Mind Charger WiFi Setup</h1>
				<form action="/submit" method="post">
					<label for="ssid">Enter SSID:</label>
					<input id="ssid" name="ssid"/>
					<br>
					<label for="password">Enter Password:</label>
					<input id="password" name="password" type="password"/>
					<br>
					<input type="submit" value="Connect"/>
				</form>
			</body>
		</html>"""
    return html_content


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        ssid = request.form["ssid"]
        password = request.form["password"]
        if update(ssid=ssid, pwd=password):
            # subprocess.run(
            #     restart_wifi, shell=True, text=True, stdout=subprocess.PIPE
            # ).stdout
            # sleep(2)
            os.system("nmcli con down Hotspot")
            sleep(3)
            os.system(f'nmcli device wifi connect "{ssid}" password "{password}"')
            sleep(5)
            check_wifi()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
