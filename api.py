from flask import Flask, request, render_template, url_for, session, escape, redirect
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


#class HelloWorld(Resource):
	#def get(self):
		#return {'hello': 'world'}
		
#api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
	app.run(debug=True)

#@app.errorhandler(404)
#def page_not_found(error):
    #return render_template('page_not_found.html'), 404s

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	
@app.route('/index')
@app.route('/index/<name>')
def hello(name=None):
	return render_template('login.html', name=name);
		
#@app.route('/user/<username>')
#def show_user_profile(username):
    ## show the user profile for that user
    #return 'User %s' % username

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        set_controls()
    else:
        show_controls()
