from flask import Flask, request
import subprocess

app = Flask(__name__)

wifi_device = "wlan0"

@app.get('/')
def home():
	#result = subprocess.check_output(["nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", wifi_device])
	#ssid_list = result.decode()
	html_content = f"""
		<!DOCTYOE html>
		<html>
		<head><title>Mind Charger</title></head>
		<body>
		<h1>Wifi Control</h1>
		<form action="/submit" method="post">
		<label for="ssid">Enter SSID:</label>
		<input name="ssid"/>
		<label for="password">Enter Password:</label>
		<input name="password" type="password"/>
		<input type="submit" value="Connect"/>
		</form>
		</body>
		</html>
		"""
	return html_content

@app.route('/submit', methods=['POST'])
def submit():
	if request.method == "POST":
		ssid = request.form['ssid']
		password = request.form['password']
		connection_command = ["nmcli", "--colors", "no", "device", "wifi", "connect", ssid, "password", password, "ifname", wifi_device]
		result = subprocess.run(connection_command, capture_output=True)
		if result.stderr:
			return "Error: Cannot connect to this WiFi"
		elif result.stdout:
			return "Success: Connection Successful"
		else:
			"Error: Cannot process"



app.run(host='0.0.0.0', port=80)
