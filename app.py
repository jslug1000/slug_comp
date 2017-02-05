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
                return redirect('/competitorHome')
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
                return redirect('/competitorHome')
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


@app.route('/competitorHome')
def competitorHome():
    if session.get('user'):
        message = 'welcome home, ' + session.get('user')
        return render_template('competitorHome.html', message=message)
    else:
        return render_template('error.html', error='you need to login first')

@app.route('/createTournament', methods=['POST', 'GET'])
def createTournament():
    if session.get('user'):
        return render_template('createTournament.html', user=session.get('user'))
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
            session['tournament'] = _tournament
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/addCompetitors')
        else:
            return render_template('error.html', error='a tournament of that name already exists, please choose another')

    except Exception as e:
        return render_template('error.html', error=str(e))
    # finally:
    #     return render_template('error.html', error=str(e))


@app.route('/showCompetitors', methods=['POST', 'GET'])
def showCompetitors():
    if session.get('user'):
        return render_template('showCompetitors.html', user=session.get('user'))
    else:
        return render_template('error.html', error='you need to login first')

@app.route('/displayCompetitors')
def displayCompetitors():
    try:
        if session.get('user'):
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetAllUsers')
            users = cursor.fetchall()

            users_list = []
            for user in users:
                user_dict = {'username': user[0]}
                users_list.append(user_dict)

            cursor.close()
            con.close()

            return json.dumps(users_list)
        else:
            return render_template('error.html', error='unauthorised access')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/addCompetitors', methods=['POST', 'GET'])
def addCompetitors():
    if session.get('user'):
        return render_template('addCompetitors.html')
    else:
        return render_template('error.html', error='you need to login first')

@app.route('/validateCompetitor', methods=['POST', 'GET'])
def validateCompetitor():
    try:
        _entered_by = session.get('user')
        _tournament = session.get('tournament')
        _competitor = request.form['inputCompetitor']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createCompetitor', (_tournament, _competitor, _entered_by))
        data = cursor.fetchall()

        if 'this' in data:   # check for error message
            return render_template('error.html', error=data)

        elif len(data) == 0:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/addCompetitors')
        else:
            return render_template('error.html', error=data)

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/createGame')
def createGame():
    if session.get('user'):
        return render_template('createGame.html')
    else:
        return render_template('error.html', error='you need to login first')

@app.route('/validateGame', methods=['POST', 'GET'])
def validateGame():
    try:
        _entered_by = session.get('user')
        _tournament = request.form['inputTournamentName']
        _game = request.form['inputGameName']
        _1points = request.form['input1Points']
        _2points = request.form['input2Points']
        _3points = request.form['input3Points']
        _4points = request.form['input4Points']
        # _partpoints = request.form['inputParticipationPoints']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createGame', (_tournament, _game, _entered_by, _1points, _2points, _3points, _4points))
        data = cursor.fetchall()

        if 'this' in data:   # check for error message
            return render_template('error.html', error=data)

        elif len(data) == 0:
            conn.commit()
            cursor.close()
            conn.close()
            message = 'game created successfully'
            return render_template('competitorHome.html', message=message)
        else:
            return render_template('error.html', error=data)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/setupGame')
def setupGame():
    if session.get('user'):
        return render_template('gameSetup.html')
    else:
        return render_template('error.html', error='you need to login first')



@app.route('/validateResults', methods=['POST', 'GET'])
def validateResults():
    try:
        _entered_by = session.get('user')
        _tournament = request.form['inputTournamentName']
        _game = request.form['inputGameName']
        _1place = request.form['input1Place']
        _2place = request.form['input2Place']
        _3place = request.form['input3Place']
        _4place = request.form['input4Place']
        _partpoints = request.form['inputParticipationPoints']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createGame', (_tournament, _game, _entered_by, _1place, _2place, _3place, _4place))
        data = cursor.fetchall()

        if 'this' in data:   # check for error message
            return render_template('error.html', error=data)

        elif len(data) == 0:
            conn.commit()
            cursor.close()
            conn.close()
            message = 'results entered successfully'
            return render_template('competitorHome.html', message=message)
        else:
            return render_template('error.html', error=data)

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/validateResults', methods=['POST', 'GET'])
def validateResults():
    try:
        _entered_by = session.get('user')
        _tournament = request.form['inputTournamentName']
        _game = request.form['inputGameName']
        _1place = request.form['input1Place']
        _2place = request.form['input2Place']
        _3place = request.form['input3Place']
        _4place = request.form['input4Place']
        _partpoints = request.form['inputParticipationPoints']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createGame', (_tournament, _game, _entered_by, _1place, _2place, _3place, _4place))
        data = cursor.fetchall()

        if 'this' in data:   # check for error message
            return render_template('error.html', error=data)

        elif len(data) == 0:
            conn.commit()
            cursor.close()
            conn.close()
            message = 'results entered successfully'
            return render_template('competitorHome.html', message=message)
        else:
            return render_template('error.html', error=data)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":    # check if executed file is main program
    app.run(port=8080)