from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
import datetime
import os
import mysql.connector
from flask_hashing import Hashing
from tree_message_board import app
from tree_message_board import connect

hashing = Hashing(app)  #create an instance of hashing

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'COMP639$3cr3+K3y'

# IMPORTANT: Change 'ExampleSaltValue' to whatever salt value you'll use in
# your application. If you don't do this, your password hashes won't work!
PASSWORD_SALT = 'COMP639$@7+V@7u3'

# Default role assigned to new users upon registration.
DEFAULT_USER_ROLE = 'member'

# Default status assigned to new users upon registration.
DEFAULT_STATUS = 'active'

# Default user profile picture assigned to new users upon registration.
DEFAULT_PROFILE_PICTURE = 'profile.png'



db_connection = None

def getCursor():
    """Gets a new dictionary cursor for the database.
    
    If necessary, a new database connection be created here and used for all
    subsequent to getCursor()."""
    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    
    return cursor

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():

    image = os.path.join(app.config["UPLOAD_FOLDER"], "trees.jpg")
    print(image)
    # Output message if something goes wrong...
    msg = ''
    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT user_id, username, password_hash, role FROM users WHERE username = %s', (username,))
        
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password_hash = account['password_hash']
            if hashing.check_value(password_hash, user_password, PASSWORD_SALT):

            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['user_id']
                session['username'] = account['username']
                session['role'] = account['role']
               
                # Redirect to home page
                if session['role'] == 'member':
                    return redirect(url_for('member_home'))
                elif session['role'] == 'moderator':
                    return redirect(url_for('moderator_home'))
                else:
                    return redirect(url_for('admin_home'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg, image = image)

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('birthdate')
        location = request.form.get('location')
        profileimage = request.form.get('profileimage')

        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not firstname or not lastname or not birthdate or not location or not profileimage:
            msg = 'Please fill out the form!'
        else:
            # Account doesn't exist and the form data is valid, now insert new account into accounts table
            password_hash = hashing.hash_value(password, PASSWORD_SALT)
            cursor.execute('INSERT INTO users (username, password_hash, email,first_name, last_name, birth_date, location, profile_image,  role, status) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)',
                           (username, password_hash, email, firstname, lastname, birthdate, location,DEFAULT_PROFILE_PICTURE, DEFAULT_USER_ROLE, DEFAULT_STATUS))
            db_connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/member/home', methods=['GET','POST'])
def member_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # Get all the messages in the database
        cursor = getCursor()
        cursor.execute('SELECT * FROM messages',)
        allMessages = cursor.fetchall()
        
        return render_template('home.html', username=session['username'], user_role=session['role'],  allmessages= allMessages)
    
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))




@app.route("/view_post", methods=['GET','POST'])
@app.route("/view_post/<int:messageid>", methods=['GET','POST'])
def view_post(messageid):
    print(messageid)
    if 'loggedin' in session:
        # cursor = getCursor()
        # cursor.execute("SELECT username FROM messages WHERE message_id = %s;", (int(messageid),))
        # username = cursor.fetchone()
        cursor = getCursor()
        cursor.execute("SELECT * FROM messages WHERE message_id = %s;", (int(messageid),))
        messageData = cursor.fetchone()
        cursor = getCursor()
        cursor.execute("SELECT * FROM replies WHERE message_id = %s;", (int(messageid),))
        replyData = cursor.fetchall()
        sql = "SELECT * FROM messages JOIN replies ON messages.message_id = replies.message_id;"

        
        if request.method =='POST'and request.form.get('reply'):
            messageId = request.form.get('messageid')
            messageData = request.form.get('messagedata')
            userId = session['id']
            content = request.form.get('content')
            created_at = datetime.datetime.now()                
            cursor = getCursor()
            cursor.execute("INSERT INTO replies (message_id, user_id, content, created_at) VALUES(%s,%s,%s,%s);",(messageId, userId, content, created_at,))
            usrmsg = "REPLY ADDED"
            # return render_template('view_post.html',messageid=messageId, username=session['username'], user_role=session['role'], messagedata=messageData, replydata=replyData)    
            return render_template('confirmation.html', usrmsg = usrmsg,username=session['username'], user_role=session['role'])
        if request.method =='POST'and request.form.get('delete'):
            
            cursor = getCursor()
            cursor.execute("DELETE FROM replies WHERE message_id = %s;",(int(messageid),))            
            cursor = getCursor()
            cursor.execute("DELETE FROM messages WHERE message_id = %s;",(int(messageid),))
            
            usrmsg = "POST DELETED"
            # return render_template('view_post.html',messageid=messageId, username=session['username'], user_role=session['role'], messagedata=messageData, replydata=replyData)    
            return render_template('confirmation.html', usrmsg = usrmsg,username=session['username'], user_role=session['role'])
        
        return render_template('view_post.html',messageid=messageid, username=session['username'], user_role=session['role'], messagedata=messageData, replydata=replyData)

    # User is not logged in - redirect to login page
    return redirect(url_for('login'))
    

@app.route("/view_reply", methods=['GET','POST'])
@app.route("/view_reply/<int:replyid>", methods=['GET','POST'])
def view_reply(replyid):
    print(replyid)
    if 'loggedin' in session:
        
        cursor = getCursor()
        cursor.execute("SELECT * FROM replies WHERE reply_id = %s;", (int(replyid),))
        replyData = cursor.fetchall()
        if request.method =='POST':
                         
            cursor = getCursor()
            cursor.execute("DELETE FROM replies WHERE reply_id = %s;",(int(replyid),))
            usrmsg = "REPLY DELETED"
            # return render_template('view_post.html',messageid=messageId, username=session['username'], user_role=session['role'], messagedata=messageData, replydata=replyData)    
            return render_template('confirmation.html', usrmsg = usrmsg,username=session['username'], user_role=session['role'])
        
        return render_template('view_reply.html', replyid=replyid, username=session['username'], user_role=session['role'], replydata=replyData)

    # User is not logged in - redirect to login page
    return redirect(url_for('login'))



@app.route('/create_post',methods=['GET','POST'])
def create_post():
   
    if 'loggedin' in session:
        
        print(datetime.datetime.now())
        print(request.method)
        if request.method == "POST":
            print("increatepost post method")
            userId = session['id']
            title = request.form.get('title')
            content = request.form.get('content')
            created_at = datetime.datetime.now()
            print(userId)
            print(title)
            print(content)
            print(created_at)
            cursor = getCursor()
            cursor.execute("INSERT INTO messages (user_id, title, content, created_at) VALUES(%s,%s,%s,%s);",(userId, title, content, created_at,))
            return redirect(url_for('member_home'))
        return render_template('create_post.html',username=session['username'], user_role=session['role'])
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))

@app.route('/delete_post',methods=['GET','POST'])
def delete_post():
    if 'loggedin' in session:
        cursor = getCursor()
        cursor.execute("SELECT * FROM messages WHERE user_id = %s;", (int(session['id']),))
        messageData = cursor.fetchall()
        cursor = getCursor()
        cursor.execute("SELECT * FROM replies WHERE user_id = %s;", (int(session['id']),))
        replyData = cursor.fetchall()
        print(messageData)
        print(replyData)
        # if request.method =='POST':
        #     messageId = request.form.get('messageid')
        #     messageData = request.form.get('messagedata')
        #     userId = session['id']
        #     content = request.form.get('content')
        #     created_at = datetime.datetime.now()                
        #     cursor = getCursor()
        #     cursor.execute("INSERT INTO replies (message_id, user_id, content, created_at) VALUES(%s,%s,%s,%s);",(messageId, userId, content, created_at,))

        #     # return render_template('view_post.html',messageid=messageId, username=session['username'], user_role=session['role'], messagedata=messageData, replydata=replyData)    
        #     return render_template('confirmation.html')
        return render_template('delete_post.html', username=session['username'], user_role=session['role'], messagedata=messageData, replydata=replyData)

    # User is not logged in - redirect to login page
    return redirect(url_for('login'))

@app.route('/create_reply',methods=['GET','POST'])
def create_reply():
    # print(message_id)
    if 'loggedin' in session:
        print("increatereply session")
        
    #     print(datetime.datetime.now())
    #     print(request.method)
    #     if request.method == "POST":
    #         print("increatepost post method")
    #         userId = session['id']
    #         title = request.form.get('title')
    #         content = request.form.get('content')
    #         created_at = datetime.datetime.now()

             
                
    #             # content = request.form.get('content')
    #             # created_at = datetime.datetime.now()                
    #             # cursor = getCursor()
    #             # cursor.execute("INSERT INTO replies (message_id, user_id, content, created_at) VALUES(%s,%s,%s,%s);",(messageid, userId, content, created_at,))
    #             # return render_template('view_post.html', messageid=messageid ,username=session['username'], user_role=session['role'])
    #         print(userId)
    #         print(title)
    #         print(content)
    #         print(created_at)
    #         cursor = getCursor()
    #         cursor.execute("INSERT INTO messages (user_id, title, content, created_at) VALUES(%s,%s,%s,%s);",(userId, title, content, created_at,))
    #         return redirect(url_for('user_home'))
        return render_template('view_post.html',username=session['username'], user_role=session['role'])
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))

# # http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
# @app.route('/profile',methods=['GET','POST'])
# def profile(account=None):
#     profileImage = os.path.join(app.config["UPLOAD_FOLDER"], "Profile.png")

#     # Check if user is loggedin
#     if 'loggedin' in session:
        
#         # We need all the account info for the user so we can display it on the profile page
#         cursor = getCursor()
#         cursor.execute('SELECT user_id, username, email,first_name, last_name, birth_date, location, profile_image, role, status FROM users WHERE user_id = %s', (session['id'],))
#         account = cursor.fetchone()
        
#         if request.method=="POST" and request.form.get("editprofile"):
#             return render_template('edit_profile.html',account = account, username=session['username'], user_role=session['role'])
#         elif request.method=="POST" and request.form.get("editpassword"):
#             return render_template('edit_password.html',account = account, username=session['username'], user_role=session['role'])

#         # Show the profile page with account info
#         return render_template('profile.html', profileimage =profileImage, account=account, username=session['username'], user_role=session['role'])
    
#     # User is not logged in - redirect to login page
#     return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile',methods=['GET','POST'])
@app.route('/profile/<int:userid>',methods=['GET','POST'])
def profile(userid=None):
    print(userid)

    


    # Check if user is loggedin
    if 'loggedin' in session:

    #     if userid== None:
    #     profileImage = os.path.join(app.config["UPLOAD_FOLDER"], "Profile.png")
    # else:
        

        
        if userid == None:
            userid = session['id']

            # cursor = getCursor()
            # cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (userid,))
            # image = cursor.fetchone()
            # print(userid)
            # print(image)
            # profileImage = os.path.join(app.config["UPLOAD_FOLDER"], image['profile_image'])
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (userid,))
        account = cursor.fetchone()
        image = account['profile_image']
           
        profileImage = os.path.join(app.config["UPLOAD_FOLDER"], image)

        if request.method=="POST" and request.form.get("editprofile"):
            return render_template('edit_profile.html',account = account, username=session['username'], user_role=session['role'])
        elif request.method=="POST" and request.form.get("changepassword"):
            return render_template('change_password.html',account = account, username=session['username'], user_role=session['role'])
        elif request.method=="POST" and request.form.get("changeimage"):
            return render_template('change_image.html',account = account, username=session['username'], user_role=session['role'])
        elif request.method=="POST" and request.form.get("removeimage"):
            cursor = getCursor()
            cursor.execute('UPDATE users SET profile_image = %s WHERE user_id = %s;', (DEFAULT_PROFILE_PICTURE, session['id'],))
            usrmsg="Image updated"
            return render_template('confirmation.html',usrmsg=usrmsg, username=session['username'], user_role=session['role'])
            
        elif request.method=="POST" and request.form.get("changeaccess"):
            if session['role'] == 'admin':
                return redirect( url_for('change_access',userid=userid ))
                # return render_template('change_access.html',account = account, username=session['username'], user_role=session['role'])
            else:
                return render_template('error.html',account = account, username=session['username'], user_role=session['role'])
        # Show the profile page with account info
        return render_template('profile.html', profileimage =profileImage, account=account, username=session['username'], user_role=session['role'])
    
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile/edit',methods=['GET','POST'])
def profileedit():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        # cursor = getCursor()
        # cursor.execute('SELECT user_id, username, email,first_name, last_name, birth_date, location, profile_image, role, status FROM users WHERE user_id = %s', (session['id'],))
        # account = cursor.fetchone()
        
        print(session['id'])
        
        if request.method=="POST":        
            email = request.form.get('email')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            birthdate = request.form.get('birthdate')
            location = request.form.get('location')
            
            print(email)
            print(firstname)
            print(lastname)
            print(birthdate)
            print(location)
            

            cursor = getCursor()
             # cursor.execute('SELECT user_id, username, email,first_name, last_name, birth_date, location, profile_image, role, status FROM users WHERE user_id = %s', (session['id'],))
            cursor.execute("UPDATE users SET email = %s, first_name = %s, last_name = %s, birth_date = %s, location = %s WHERE user_id = %s;", (email, firstname, lastname, birthdate, location, session['id'],))
            # Show the profile page with account info
            usrmsg="Profile updated"
            return render_template('confirmation.html',usrmsg = usrmsg, username=session['username'], user_role=session['role'])
        return render_template('edit_profile.html', username=session['username'], user_role=session['role'])
    
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))

@app.route('/password',methods=['GET','POST'])
def password():
    

    # Check if user is loggedin
    if 'loggedin' in session:
        
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute('SELECT password_hash FROM users WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()
        dbPassword_hash = account['password_hash']
        print(dbPassword_hash)
        if request.method=="POST":
            oldPassword = request.form.get('oldpassword')
            oldPassword_hash = hashing.hash_value(oldPassword, PASSWORD_SALT)
            newPassword = request.form.get('newpassword')
            newPassword_hash = hashing.hash_value(newPassword, PASSWORD_SALT)
            if dbPassword_hash != oldPassword_hash:
                usrmsg="Old password does not match saved password, please change" 
            elif dbPassword_hash == oldPassword_hash and oldPassword_hash == newPassword_hash:
                usrmsg="Old and new passwords cannot be the same, please change"
            else:
                cursor = getCursor()
                cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s;', (newPassword_hash, session['id'], ))
                usrmsg="Password updated"

            return render_template('confirmation.html',usrmsg=usrmsg, username=session['username'], user_role=session['role'])

        # Show the profile page with account info
        return render_template('edit_password.html', account=account, username=session['username'], user_role=session['role'])
    
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))


@app.route('/image',methods=['GET','POST'])
def image():
    profileImage = os.path.join(app.config["UPLOAD_FOLDER"], "Profile.png")

    # Check if user is loggedin
    if 'loggedin' in session:
        
        

        # # We need all the account info for the user so we can display it on the profile page
        if request.method=="POST":
            newImage = request.form.get('image')
            # newProfileImage = os.path.join(app.config["UPLOAD_FOLDER"], str(newImage))
            cursor = getCursor()
            cursor.execute('UPDATE users SET profile_image = %s WHERE user_id = %s;', (newImage, session['id'],))
            usrmsg="Image updated"

            return render_template('confirmation.html',usrmsg=usrmsg, username=session['username'], user_role=session['role'])
            

        #     return render_template('confirmation.html',usrmsg=usrmsg, username=session['username'], user_role=session['role'])

        # Show the profile page with account info
        return render_template('change_image.html', username=session['username'], user_role=session['role'])
    
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)

   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)