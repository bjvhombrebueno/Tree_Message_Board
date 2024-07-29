
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
DEFAULT_USER_ROLE = 'user'

# Default status assigned to new users upon registration.
DEFAULT_STATUS = 'active'

# Default user profile picture assigned to new users upon registration.
DEFAULT_PROFILE_PICTURE = 'link me'



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





@app.route('/staff/home')
def staff_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        if session['role'] == 'staff':
            # User is loggedin show them the home page and role is staff
            cursor = getCursor()
            cursor.execute('SELECT * FROM messages',)
            allMessages = cursor.fetchall()
            return render_template('staff_home.html', username=session['username'], user_role=session['role'])
        else:
            return render_template('Error.html', user_role=session['role'])
       
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search_users():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'staff':
            # User is loggedin show them the home page and role is staff
            if request.method == "GET":
                return render_template("user_search.html")
            else:
                searchString = request.form.get('searchstring')
                #SQL to return all of the matches of the search string
                sql= "SELECT * FROM users WHERE username LIKE '%"+ searchString + "%' OR first_name LIKE '%"+ searchString + "%' OR last_name LIKE '%"+ searchString + "%' ORDER BY user_id;"
                print(sql)
                connection = getCursor()
                connection.execute(sql)
                searchResults = connection.fetchall()
                print(request.form)
                print(searchResults)
                return render_template("user_search.html",searchresults=searchResults)
                # usrmsg = "search"
                # return render_template('confirmation.html',usrmsg=usrmsg, username=session['username'], user_role=session['role'])
        
        
        
        else:
            return render_template('Error.html', user_role=session['role'])

        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

