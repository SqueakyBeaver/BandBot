from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "All booted"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    '''
	Creates and starts new thread that runs the function run.
	'''
    t = Thread(target=run)
    t.start()


