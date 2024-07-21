from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from loginapp import app

@app.route('/admin/home')
def admin_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'admin':
            # User is loggedin show them the home page and role is admin
            return render_template('admin_home.html', username=session['username'], user_role=session['role'])
        else:
            return render_template('Error.html', user_role=session['role'])
        
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))