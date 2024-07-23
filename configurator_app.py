from wlan_utility import update
from logge import generate_log as logger
import os
from flask import Flask, request, redirect

app = Flask(__name__)

check_wifi = "/home/pi/check_wifi_status.sh"
restart_wifi = "/home/pi/restart_wifi.sh"

os.system(f"{check_wifi} &")


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


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        ssid = request.form["ssid"]
        password = request.form["password"]
        if update(ssid=ssid, pwd=password):
            os.system(
                f'nmcli con down Hotspot && nmcli device wifi connect "{ssid}" password "{password}" && {check_wifi} &'
            )
            logger(f"sent for update, {ssid}, {password}")
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
