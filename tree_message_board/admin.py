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


@app.route('/admin/home', methods=['GET','POST'])
def admin_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'admin':
            # User is loggedin show them the home page and role is admin
            cursor = getCursor()
            cursor.execute('SELECT * FROM messages',)
            allMessages = cursor.fetchall()
            
            return render_template('admin_home.html', username=session['username'], user_role=session['role'], allmessages = allMessages)
        else:
            return render_template('Error.html', user_role=session['role'])
        
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search_users():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'admin':
            # User is loggedin show them the home page and role is staff
            if request.method == "GET":
                return render_template("user_search.html", username=session['username'], user_role=session['role'])
            else:
                searchString = request.form.get('searchstring')
                searchBy=request.form['searchby']
                #SQL to return all of the matches of the search string
                if searchBy == "firstname" :
                    sql ="SELECT * FROM users WHERE first_name LIKE '%"+ searchString + "%' ORDER BY last_name;"
                elif searchBy == "lastname" :
                    sql ="SELECT * FROM users WHERE last_name LIKE '%"+ searchString + "%' ORDER BY last_name;"
                else:
                    sql ="SELECT * FROM users WHERE username LIKE '%"+ searchString + "%' ORDER BY last_name;"

                # sql= "SELECT * FROM users WHERE username LIKE '%"+ searchString + "%' OR first_name LIKE '%"+ searchString + "%' OR last_name LIKE '%"+ searchString + "%' ORDER BY user_id;"
                print(sql)
                connection = getCursor()
                connection.execute(sql)
                searchResults = connection.fetchall()
                print(request.form)
                print(searchResults)
                return render_template("user_search.html",searchresults=searchResults, username=session['username'], user_role=session['role'])
                # usrmsg = "search"
                # return render_template('confirmation.html',usrmsg=usrmsg, username=session['username'], user_role=session['role'])
        
        
        
        else:
            return render_template('Error.html', user_role=session['role'])

        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/profile',methods=['GET','POST'])
@app.route('/profile/<int:userid>',methods=['GET','POST'])
def profileadmin(userid=None):
    profileImage = os.path.join(app.config["UPLOAD_FOLDER"], "Profile.png")

    # Check if user is loggedin
    if 'loggedin' in session:
        print(session['role'])
        if userid == None:
            userid = session['id']
        
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (userid,))
        account = cursor.fetchone()
        print(account)

        if request.method=="POST" and request.form.get("editprofile"):
            return render_template('edit_profile.html',account = account, username=session['username'], user_role=session['role'])
        elif request.method=="POST" and request.form.get("changepassword"):
            return render_template('change_password.html',account = account, username=session['username'], user_role=session['role'])
        elif request.method=="POST" and request.form.get("changepermissions"):
            if session['role'] == 'admin':
                return render_template('change_access.html',account = account, username=session['username'], user_role=session['role'])
        # Show the profile page with account info
        return render_template('profile.html', profileimage =profileImage, account=account, username=session['username'], user_role=session['role'])
    
    # User is not logged in - redirect to login page
    return redirect(url_for('login'))

@app.route('/moderation', methods=['GET','POST'])
def moderation():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'admin' or session['role'] == 'moderator' :
            # User is loggedin show them the home page and role is staff
            if request.method == "GET":
                cursor = getCursor()
                cursor.execute('SELECT * FROM messages',)
                allMessages = cursor.fetchall()
                cursor = getCursor()
                cursor.execute('SELECT * FROM replies',)
                allReplies= cursor.fetchall()
                

                return render_template("moderation.html", username=session['username'], user_role=session['role'], allmessages=allMessages, allreplies=allReplies)
            
        
        
        else:
            return render_template('Error.html', user_role=session['role'])

        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



# @app.route('/access/<int:userid>', methods=['GET', 'POST'])
# def change_access(userid):
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         if session['role'] == 'admin':
#             print(userid)
#             if request.method == 'GET':
#                 cursor = getCursor()
#                 cursor.execute('SELECT * FROM users WHERE user_id = %s', (userid,))
#                 account = cursor.fetchone()
#                 return(render_template("change_access.html", username=session['username'], user_role=session['role']))

#             if request.method == 'POST':
#                 # username = request.form.get('username')
#                 # role = request.form.get('role')
#                 # status = request.form.get('status')
#                 # print(username)
#                 # print(role)
#                 # print(status)

#                 # cursor = getCursor()
                
#                 # cursor.execute("UPDATE users SET role = %s, status = %s WHERE username = %s;", (role, status, username,))
#                 usrmsg = "Access changed"
#                 return render_template("confirmation.html", usrmsg=usrmsg, username=session['username'], user_role=session['role'])
#             else:
#                 return render_template("change_access.html", username=session['username'], user_role=session['role'])
        
        
#         else:
#             return render_template('Error.html', user_role=session['role'])

        
    
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

@app.route('/access', methods=['GET', 'POST'])
def change_access():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'admin':
            
            if request.method == 'GET':
                cursor = getCursor()
                cursor.execute('SELECT user_id, username, email, first_name, last_name,role, status  FROM users;')
                userList = cursor.fetchall()
                return(render_template("change_access.html",userlist=userList, username=session['username'], user_role=session['role']))

            

                    # username = request.form.get('username')
                # role = request.form.get('role')
                # status = request.form.get('status')
                # print(username)
                # print(role)
                # print(status)

                # cursor = getCursor()
                
                # cursor.execute("UPDATE users SET role = %s, status = %s WHERE username = %s;", (role, status, username,))
                usrmsg = "Access changed"
                return render_template("confirmation.html", usrmsg=usrmsg, username=session['username'], user_role=session['role'])
            else:
                return render_template("change_access.html", username=session['username'], user_role=session['role'])
        
        
        else:
            return render_template('Error.html', user_role=session['role'])

        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/access/role/<int:userid>', methods=['GET', 'POST'])
def change_role(userid):
    # Check if user is loggedin
    print(userid)
    if 'loggedin' in session:
        if session['role'] == 'admin':
                if request.method =="GET":
                    cursor = getCursor()
                    cursor.execute('SELECT * FROM users WHERE user_id = %s', (userid,))
                    account = cursor.fetchone()
                    return render_template("change_role.html", userid = userid, account=account,  username=session['username'], user_role=session['role'])
                # return(render_template("change_access.html",userlist=userList, username=session['username'], user_role=session['role']))

            
                if request.method == "POST":
                    
                    role = request.form['role']
                    print(userid)
                    print(role)
                    cursor = getCursor()
                    # sql= "SELECT * FROM users WHERE username LIKE '%"+ searchString + "%' OR first_name LIKE '%"+ searchString + "%' OR last_name LIKE '%"+ searchString + "%' ORDER BY user_id;"
                    updatestring = "UPDATE users SET role = "+ role + " WHERE (user_id =' "+ str(userid) +"');"
                    print(updatestring)
                    # cursor.execute("UPDATE users SET role = %s WHERE username = %s;", (role, int(userid),))
                    cursor.execute(updatestring)
                    usrmsg = "Role changed"
                    return render_template("confirmation.html", usrmsg=usrmsg, username=session['username'], user_role=session['role'])
            
                
        
        
        else:
            return render_template('Error.html', user_role=session['role'])

        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/access/status/<int:userid>', methods=['GET', 'POST'])
def change_status(userid):
    # Check if user is loggedin
    print(userid)
    if 'loggedin' in session:
        if session['role'] == 'admin':
                if request.method =="GET":
                    cursor = getCursor()
                    cursor.execute('SELECT * FROM users WHERE user_id = %s', (userid,))
                    account = cursor.fetchone()
                    return render_template("change_status.html", userid = userid, account=account,  username=session['username'], user_role=session['role'])
                # return(render_template("change_access.html",userlist=userList, username=session['username'], user_role=session['role']))

            
                if request.method == "POST":
                    
                    status = request.form['status']
                    print(userid)
                    print(status)
                    cursor = getCursor()
                    # sql= "SELECT * FROM users WHERE username LIKE '%"+ searchString + "%' OR first_name LIKE '%"+ searchString + "%' OR last_name LIKE '%"+ searchString + "%' ORDER BY user_id;"
                    updatestring = "UPDATE users SET status = "+ status + " WHERE (user_id =' "+ str(userid) +"');"
                    print(updatestring)
                    # cursor.execute("UPDATE users SET role = %s WHERE username = %s;", (role, int(userid),))
                    cursor.execute(updatestring)
                    usrmsg = "Status changed"
                    return render_template("confirmation.html", usrmsg=usrmsg, username=session['username'], user_role=session['role'])
            
                
        
        
        else:
            return render_template('Error.html', user_role=session['role'])

        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))