from flask import Flask
from flask.ext.script import Manager

app=Flask(__name__)
manager = Manager(app)
@app.route('/')
def init():
	return "hello world"

@app.route('/user/<name>')
def user(name):
	return "<h1>hello ,%s" % name

if __name__=='__main__':
	manager.run()