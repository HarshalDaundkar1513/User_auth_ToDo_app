from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from login_database import get_database, open_database

app = Flask(__name__)
app.secret_key = "Login_App_Auth"

@app.route('/')
def index():
    session.pop('email', None)
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
            flash("Account Created successfully")
            db = get_database()
            db.execute('INSERT INTO Users (UserName, UserEmail, Password) VALUES (?, ?, ?)', 
                       [UserName, UserEmail, hashed_password])
            db.commit()
            return redirect(url_for('index'))
        else:
            error = "Passwords do not match"
            return render_template('createacc.html', error=error)

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
            return redirect(url_for('TodosApp'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('LoginPage'))
    

@app.route('/TodosApp')
def TodosApp():
    if g.email:
        db = get_database()
        task_entry = db.execute("select * from todos")
        all_tasks = task_entry.fetchall()
        return render_template('Todo_Home.html' , all_task = all_tasks)
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
        db.execute('insert into todos( todaystask, Tmember) values (?,?) ',[tmember,task])
        db.commit()
        return redirect(url_for('TodosApp'))
    return render_template('Todo_Home.html')


@app.route('/deletetask/<int:id>', methods=['POST', 'GET'])
def deletetask(id):
    if request.method == "GET":
        db = get_database()
        db.execute('delete from todos where id = ? ',[id])
        db.commit()
        return redirect(url_for('TodosApp'))
    return render_template('Todo_Home.html')


@app.route('/updatetask/<int:id>', methods=['POST', 'GET'])
def updatetask(id):
    db = get_database()
    if request.method == "POST":
        tmember = request.form['tmember']
        task = request.form['task']
        db.execute('UPDATE todos SET todaystask = ? , Tmember = ? WHERE id = ?', [task , tmember, id])
        
        db.commit()
        return redirect(url_for('TodosApp'))
    else:
        task = db.execute("select * from todos where id = ?",[id]).fetchone()
        return render_template('update.html', task = task)
    
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
