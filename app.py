from flask import Flask, render_template, request, json, session, redirect, url_for, escape, flash
from flaskext.mysql import MySQL
from hashlib import md5
import os

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'sql11158711'
app.config['MYSQL_DATABASE_PASSWORD'] = 'EaNz5AS98v'
app.config['MYSQL_DATABASE_DB'] = 'sql11158711'
app.config['MYSQL_DATABASE_HOST'] = 'sql11.freemysqlhosting.net'
app.secret_key = 'FEF9B%399-!8EF6- 4B16-[9BD4-092B1<85D632D'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


class ServerError(Exception):
    pass


@app.errorhandler(404)
def page_not_found(e):
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]
        # So is this the main page you're meant to go to?
        return render_template('page_not_found.html', session_user_name=username_session)
    return render_template('page_not_found.html'), 404


@app.route("/index")
@app.route("/")
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]
        # So is this the main page you're meant to go to?
        return render_template('index.html', session_user_name=username_session)
    return render_template('index.html')


# @app.route("/login")
# def login():
#     if 'username' in session:
#         username_session = escape(session['username']).capitalize()
#         username_session = username_session.split('@')[0]
#         # So is this the main page you're meant to go to?
#         return redirect(url_for('index'))
#     return render_template('login.html')
#
#
# @app.route("/signup")
# def signup():
#     if 'username' in session:
#         username_session = escape(session['username']).capitalize()
#         username_session = username_session.split('@')[0]
#         # So is this the main page you're meant to go to?
#         return redirect(url_for('index'))
#     return render_template('signup.html')


@app.route("/my_account")
def my_account():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]
        # So is this the main page you're meant to go to?
        return render_template('my_account.html', session_user_name=username_session)
    return redirect(url_for('index'))


@app.route('/action_signup', methods=['POST'])
def action_signup():

    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if not _name and not _email and not _password:
        return json.dumps({'html': '<span>Enter the required fields</span>'})
    else:
        json.dumps({'html': '<span>All fields good !!</span>'})

        cursor.execute("SELECT COUNT(1) FROM tbl_user WHERE user_email = '{0}';".format(_email))

        if cursor.fetchone()[0]:
            flash('Email already used')
            return redirect(url_for('index'))

        _hashed_password = md5(md5(app.secret_key).hexdigest() + md5(_password).hexdigest()).hexdigest()
        query = "INSERT INTO tbl_user (user_name, user_email, user_password) VALUES ('{0}', '{1}', '{2}')".format(
            _name, _email, _hashed_password)
        cursor.execute(query)
        conn.commit()
        return redirect(url_for('index'))


@app.route('/action_login', methods=['POST'])
def action_login():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            email_form = request.form['inputEmail']
            cursor.execute("SELECT COUNT(1) FROM tbl_user WHERE user_email = '{0}';".format(email_form))

            if not cursor.fetchone()[0]:
                raise ServerError('Invalid username')

            password_form = request.form['inputPassword']
            cursor.execute("SELECT user_password FROM tbl_user WHERE user_email = '{0}';".format(email_form))

            for row in cursor.fetchall():
                if md5(md5(app.secret_key).hexdigest() + md5(password_form).hexdigest()).hexdigest() == row[0]:
                    session['username'] = request.form['inputEmail']
                    return redirect(url_for('index'))
            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)

    return render_template('login.html', error=error)


@app.route('/action_logout')
def action_logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/action_add_bookmark')
def action_add_bookmark():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
