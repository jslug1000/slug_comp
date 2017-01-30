from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'comp_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/validateSignup', methods=['POST', 'GET'])
def validateSignup():
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _username and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _username, _password)) # this checks whether there is a user with the same name and inserts
            data = cursor.fetchall()
            # return render_template('error.html', error=str(data))

            if len(data) == 0:
                conn.commit()
                session['user'] = _username
                return redirect('/userHome')
            else:
                return render_template('error.html', error='this username is already taken')
        else:
            return render_template('error.html', error='please enter something for each field')

    except Exception as e:
        # return render_template('error.html', str(_name, _username))
        return render_template('error.html', error='something has gone horribly wrong, speak to the slug')
    # removed the following because i don't think they make a difference but they were suggested by tutorial
    # finally:
    #     cursor.close()
    #     conn.close()


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if data[0][3] == _password:
                session['user'] = data[0][1]
                return redirect('/userHome')
            else:
                return render_template('error.html', error='wrong username or password')
        else:
            return render_template('error.html', error='wrong username or password')

    except Exception as e:
        return render_template('error.html', error=str(e))
    # removed the following because i don't think they make a difference but they were suggested by tutorial
    # finally:
    #     cursor.close()
    #     con.close()


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html', user=session.get('user'))
    else:
        return render_template('error.html', error='unauthorised access')

@app.route('/createTournament', methods=['POST', 'GET'])
def createTournament():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_GetAllUsers', ())
        users = cursor.fetchall()
        users_list = []
        for u in users:
            users_dict = {'user': u[0]}
        users_list.append(users_dict)
        return json.dumps(wishes_dict)
        return render_template('error.html', error=users_list)
        # return render_template('create_tournament.html', user=session.get('user'))
    else:
        return render_template('error.html', error='you need to login first')

@app.route('/validateTournament', methods=['POST', 'GET'])
def validateTournament():
    try:
        _username = session.get('user')
        _tournament = request.form['inputTournamentName']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createTournament', (_tournament, _username))
        data = cursor.fetchall()

        if len(data)==0:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/userHome')
        else:
            return render_template('error.html', error='a tournament of that name already exists, please choose another')

    except Exception as e:
        return render_template('error.html', error=str(e))
    # finally:
    #     return render_template('error.html', error=str(e))


# @app.route('/getWish')
# def getWish():
#     try:
#         if session.get('user'):
#             _user = session.get('user')
#
#             con = mysql.connect()
#             cursor = con.cursor()
#             cursor.callproc('sp_GetWishByUser', (_user,))
#             wishes = cursor.fetchall()
#
#             wishes_dict = []
#             for wish in wishes:
#                 wish_dict = {
#                     'Id': wish[0],
#                     'Title': wish[1],
#                     'Description': wish[2],
#                     'Date': wish[4]}
#                 wishes_dict.append(wish_dict)
#
#             return json.dumps(wishes_dict)
#         else:
#             return render_template('error.html', error='Unauthorized Access')
#     except Exception as e:
#         return render_template('error.html', error=str(e))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":    # check if executed file is main program
    app.run()