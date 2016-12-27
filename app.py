from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bookmarklist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/signup")
def show_signup():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def sign_up():

    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        json.dumps({'html': '<span>All fields good !!</span>'})

        _hashed_password = generate_password_hash(_password)
        query = "INSERT INTO tbl_user (user_name, user_email, user_password) VALUES ('{0}', '{1}', '{2}')".format(
            _name, _email, _hashed_password)
        cursor.execute(query)
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()
