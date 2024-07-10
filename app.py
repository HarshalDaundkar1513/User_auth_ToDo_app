from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from login_database import get_database, open_database

app = Flask(__name__)
app.secret_key = "Login_App_Auth"

@app.route('/')
def index():
    session.pop('email', None)
    session.pop('user_id', None)
    return render_template('index.html')

@app.route('/createacount')
def createacount():
    return render_template('createacc.html')

@app.route('/UserLogDetails', methods=['POST'])
def UserLogDetails():
    if request.method == "POST":
        UserName = request.form['UserName']
        UserEmail = request.form['UserEmail']
        UserPassword = request.form['UserPassword']
        UserPassRepeat = request.form['UserPassRepeat']
        
        if UserPassword == UserPassRepeat:
            hashed_password = generate_password_hash(UserPassword, method='pbkdf2:sha256')
            flash("Account created successfully", "success")
            db = get_database()
            db.execute('INSERT INTO Users (UserName, UserEmail, Password) VALUES (?, ?, ?)', 
                       [UserName, UserEmail, hashed_password])
            db.commit()
            return redirect(url_for('index'))
        else:
            flash("Passwords do not match", "danger")
            return redirect(url_for('createacount'))


@app.route('/LoginPage')
def LoginPage():
    return render_template('loginpage.html')

@app.route('/LoginAuth', methods=['POST', 'GET'])
def LoginAuth():
    if request.method == "POST":
        db = open_database()
        UserEmail = request.form['UserEmail']
        UserPassword = request.form['UserPassword']
        
        cur = db.execute('SELECT * FROM Users WHERE UserEmail = ?', [UserEmail])
        user = cur.fetchone()
        
        if user and check_password_hash(user['Password'], UserPassword):
            session['email'] = UserEmail
            session['user_id'] = user['UserID']
            return redirect(url_for('TodosApp'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('LoginPage'))

@app.route('/TodosApp')
def TodosApp():
    if g.email:
        db = get_database()
        task_entry = db.execute("SELECT * FROM todos WHERE user_id = ?", [session['user_id']])
        all_tasks = task_entry.fetchall()
        return render_template('Todo_Home.html', all_task=all_tasks)
    return render_template('index.html')

@app.before_request
def before_request():
    g.email = None
    if 'email' in session:
        g.email = session['email']

@app.route('/inserttask', methods=['POST'])
def inserttask():
    if request.method == "POST":
        tmember = request.form['tmember']
        task = request.form['task']
        db = get_database()
        db.execute('INSERT INTO todos (todaystask, Tmember, user_id) VALUES (?, ?, ?)',
                   [task, tmember, session['user_id']])
        db.commit()
        return redirect(url_for('TodosApp'))
    return render_template('Todo_Home.html')

@app.route('/deletetask/<int:id>', methods=['POST', 'GET'])
def deletetask(id):
    if request.method == "GET":
        db = get_database()
        db.execute('DELETE FROM todos WHERE id = ? AND user_id = ?', [id, session['user_id']])
        db.commit()
        return redirect(url_for('TodosApp'))
    return render_template('Todo_Home.html')

@app.route('/updatetask/<int:id>', methods=['POST', 'GET'])
def updatetask(id):
    db = get_database()
    if request.method == "POST":
        tmember = request.form['tmember']
        task = request.form['task']
        db.execute('UPDATE todos SET todaystask = ?, Tmember = ? WHERE id = ? AND user_id = ?', 
                   [task, tmember, id, session['user_id']])
        db.commit()
        return redirect(url_for('TodosApp'))
    else:
        task = db.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", [id, session['user_id']]).fetchone()
        return render_template('update.html', task=task)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)
