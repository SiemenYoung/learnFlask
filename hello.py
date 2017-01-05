from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ysm:123456@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Role(db.Model):
	"""docstring for Role"""
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User',backref='role',lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	"""docstring for User"""
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True)
	role_id =  db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.name
		

class NameForm(Form):
	name = StringField('What is your name',validators=[Required()])
	submit = SubmitField('Submit')


@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['konwn']=False
		else:
			session['konwn']=True
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),konwn=session.get('known',False))


# @app.route('/user/<name>')
# def user(name):
# 	return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found():
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
     return render_template('500.html'), 500

 if __name__ == '__main__':
#	#db.create_all()
 	manager.run()
