from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
import os, binascii 
from flask_bcrypt import Bcrypt

import md5 
bcrypt = Bcrypt(app)
app = Flask(__name__)
mysql = MySQLConnector(app,'userdb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

app.secret_key = 'KeepItSecretKeepItSafe'

# https://github.com/felisadeang/CD_thewall/blob/master/server.py
@app.route('/')
def index():
# try:
#     session['user_id']
#     return redirect('/wall')

    if session.has_key('user'):
        return redirect('/')
    return render_template('index.html')


@app.route('/process_login', methods=['POST'])
def process_login():
    post = request.post 
    if 'email' in post and 'password' in post:
        email =escape(post['email'].lower)]
        password = escape(post['email']))

    if email and password:
        #                     
  
    if len(request.form['email']) < 9:
        flash("Please enter your email!")
  
    if len(request.form['password']) < 8:
        flash('Please enter your password')
        return redirect('/')
    
    email = request.form['email']
    password = request.form['password']
    query="SELECT * FROM users WHERE users.email=:email LIMIT 1"

    data={'email':email}

    user=mysql.query_db(query, data)

    print 'Login results', result
    # Login results [{u'first_name': u'Franklin', u'last_name': u'Kirimi', u'created_at': datetime.datetime(2017, 12, 9, 2, 31, 27), u'updated_at': datetime.datetime(2017, 12, 9, 2, 31, 27), u'email': u'frank@yahoo.com', u'password': u'12345678', u'salt': None, u'id': 1L}]

    if not user:
        flash("Please enter valid email.", 'login_error')
        return redirect ('/')
    elif bcrypt.check_password_hash(user[0]['password'], password):
        session['user_id'] = user[0]['id']
        return redirect('/wall')
    else:
        flash('Invalid login!')
        return render_template('index.html')


@app.route('/process_register', methods=['POST'])
def process_register():
    error =0

    if len(request.form['email']) == 0:
        flash('Enter a valid email address')
        error = 1
    
    
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email format!')
        error = 1

    else: 
        all_users =mysql.query_db("SELECT * FROM users")
        for i['email'] == request.form['email']:
            flash('Please choose a unique email address')
        error = 1
        
        
    if len(request.form['first_name']) < 2:
        flash('First_name too short')
    error = 1

    elif not request.form['first_name'].isalpha():
        flash('First name has non-alpha character!', )
    error = 1

    if len(request.form['last_name']) < 1:
        flash('Last name too short ')
    error = 1

    elif not request.form['last_name'].isalpha():
        flash('Last name has a non-alpha character!')
    error = 1


    if len(request.form['password']) < 8:
        flash('Password must contain at least 8 characters!')
    error = 1

    if request.form['password'] != request.form['passwd_conf']:
        flash('Password mismatch!')
    error = 1

        first_name =request.form['first_name']
        last_name =request.form['last_name']
        email =request.form['email']
        password = request.form['password']
        salt =  binascii.b2a_hex(os.urandom(15))
        hashed_pw = md5.new(password + salt).hexdigest()

    if error ==0:

        insert_query="INSERT INTO users (first_name,last_name, email, password,salt, created_at, updated_at) VALUES(:fn,:ln,:em,:hashed_pw,:salt,NOW(),NOW() );"
    
        data={
            'fn':first_name,
            'ln':last_name,
            'em':email,
            'hashed_pw':hashed_pw,
            'salt':salt
        }

        newid=mysql.query_db(insert_query, data)
        session['id']= newid
    print "Print new id", newid
return redirect('/wall')

    # if int(user) == 0:
    #     flash('Unexpected error!!!!!!')
    #     return redirect('/')

    # else:
    #     session['first_name']= user['first_name']
    #     session['last_name']= user['last_name']
@app.route('/wall')
def wall():
    # if email in post and comment in comment:
    # print "session['id]", session['id']
    # if session['id']:
    #     query="SELECT CONCAT('first_name', ' ', 'last_name')AS message_creator_name FROM users JOIN messages ON user_id = messages.user_id"   

    #     messages=mysql.query_db(query)
    #     print "messages", messages

        # a range will return a list of numbers because you cannot iterate thru len()
        # for i in range(len(messages)):
        #     messages[i]['comments']=[]
            
    return render_template('wall.html')

@app.route('/process_message', methods=['POST'])
def process_message():

    user_input = request.form['message']
    if len(user_input) > 0:
        query = "INSERT INTO messages (message, created_at, updated_at,user_id)VALUES(:ui,mg,NOW(),NOW(),:id)"
        data={
            'message':user_input,
            'id':session['id']
        }
        new_message_id=mysql.query_db(query,data)

        print "Got the new messsage_id", new_message_id
    else:
        print "nothing in the input field" 
      
    return redirect('/wall')

@app.route('/logoff')
def logoff():
    # if session.has_key('user'):
    #    session.pop('user')
    session.clear()
    return redirect('/')

app.run(debug=True)

# ////////////////////////////
# for registration
# /////////////////////////////
 # if not request.form.has_key('first_name') or len(request.form['first_name'] < 2:
    #     flash('Please enter your first_name')
    #     redirect('/')

    # if not request.form.has_key('last_name') or len(request.form['last_name'] < 2:
    #     flash('Please enter your last_name')
    #     redirect('/')

    # if not request.form.has_key('email') or len(request.form['email'] < 2:
    #     flash('Please enter your email')
    #     redirect('/')

    # if not request.form.has_key('password') or len(request.form['password'] < 2:
    #     flash('Please enter your password')
