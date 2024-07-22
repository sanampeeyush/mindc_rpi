from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
	return  open('/home/pi/.ssh/id_ed25519.pub').read()


if __name__ == '__main__':
	app.run(port=80, host='0.0.0.0')
