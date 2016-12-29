from flask import Flask

app=Flask(__name__)

@app.route('/')
def init():
	return "hello world"

@app.route('/user/<name>')
def user(name):
	return "<h1>hello ,%s" % name

if __name__=='__main__':
	app.run(debug=True)