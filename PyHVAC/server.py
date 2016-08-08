# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import settings as mode_settings


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pyhvac.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))

modes_list = []
modes_list.append(mode_settings.mode1)
modes_list.append(mode_settings.mode2)
modes_list.append(mode_settings.mode3)
modes_list.append(mode_settings.mode4)
modes_list.append(mode_settings.mode5)

def set_mode(i):
	global selected_mode
	selected_mode = modes_list[i-1]
	print(selected_mode)
	
def get_mode():
	global selected_mode
	print(selected_mode)
	return selected_mode
    
def edit_mode(mode_num, temperature, relative_humidity, misting, light_on, light_off, pressure, co2, wind_speed):
    modes_list[mode_num-1]['TEMPERATURE']=int(temperature)
	
set_mode(1)

app.config.from_envvar('PYHVAC_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
#@app.route('/')
#def show_entries():
    #db = get_db()
    #cur = db.execute('select date_time, mode_num, mode_params, sensor_data, actuator_data from entries order by id desc')
    #entries = cur.fetchall()
    #return render_template('show_entries.html', entries=entries)
    
@app.route('/')
def show_mode():
    #db = get_db()
    #cur = db.execute('select mode_num, temperature, relative_humidity, misting, pressure, co2, wind_speed from modes order by id desc')
    #modes = cur.fetchall()
    return render_template('select_mode.html', selected_mode=get_mode()) #to show modes, add modes=modes, 
    
#@app.route('/add', methods=['POST'])
#def add_entry():
    #if not session.get('logged_in'):
        #abort(401)
    #db = get_db()
    #db.execute('insert into entries (date_time, mode_num, mode_params, sensor_data, actuator_data) values (?,?,?,?,?)',
                 #[request.form['date_time'], request.form['mode_num'],request.form['mode_params'],request.form['sensor_data'],request.form['actuator_data']])
    #db.commit()
    #flash('New entry was successfully posted')
    #return redirect(url_for('show_entries'))
    
@app.route('/select_mode', methods=['POST'])
def select_mode():
    if not session.get('logged_in'):
		abort(401)	
    print(request.form['mode_num'])
    set_mode(int(request.form['mode_num']))
    if int(request.form['mode_num']) == 5:
        edit_mode(int(request.form['mode_num']), request.form['temperature'],request.form['relative_humidity'],
            request.form['misting'],request.form['light_on'],request.form['light_off'],request.form['pressure'],
            request.form['co2'],request.form['wind_speed'])
        #db = get_db()
		#db.execute('insert into modes (mode_num, temperature, relative_humidity, misting, pressure, co2, wind_speed) values (?,?,?,?,?,?,?)',
                 #[request.form['mode_num'], request.form['temperature'],request.form['relative_humidity'],request.form['misting'],request.form['pressure'],request.form['co2'],request.form['wind_speed']])
		#db.commit()
    flash('New mode was successfully set!')
    return redirect(url_for('show_mode'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
