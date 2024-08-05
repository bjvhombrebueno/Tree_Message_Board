"""Script to generate password hashes for one or more user accounts.

You can use this script to generate flask_hashing password hashes for all of
the initial user accounts in your database creation script. Remember that each
of your user accounts should have its own unique password.

You'll need to make two changes before running this script:

1.  Replace the value of constant PASSWORD_SALT, 'ExampleSaltValue', with
    whateveer salt value you're using in your web app.

2.  Replace the list of user accounts (the block beginning "users = [") with
    the actual list of user accounts you need to generate hashes for.
"""
from collections import namedtuple
from flask import Flask
from flask_hashing import Hashing

# IMPORTANT: Change 'ExampleSaltValue' to whatever salt value you'll use in
# your application. If you don't do this, your password hashes won't work!
PASSWORD_SALT = 'COMP639$@7+V@7u3'

# We use a "named tuple" here to create a simple "User Account" class that can
# store a username and password.
# 
# Don't worry if you haven't seen this before: it's just a simple way of
# storing those two pieces of data together in one variable. It also lets us
# access the username and password by name: for example, if we create a
# UserAccount named "myuser", like this:
# 
# myuser = UserAccount('myusername', 'mypassword')
# 
# We can then access those values via "myuser.username" and "myuser.password",
# instead of having to access myuser[0] and myuser[1] like you would have to
# with a regular tuple.
UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
hashing = Hashing(app)

# Replace the example UserAccount objects below with the initial user accounts
# for your own web app. You can add as many as you need to the list.
users = [UserAccount('user1', 'A7b!eKx9'), 
         UserAccount('user2', 'm*Z4pRj8'),
         UserAccount('user3', 'V@r1dXpW'),
         UserAccount('user4', 'c#L5qTn2'),
         UserAccount('user5', 'T9p!bHjR'),
         UserAccount('user6', 'e@N8vKzW'),
         UserAccount('user7', 'Y$2rZxL1'),
         UserAccount('user8', 'f#H7sPqB'),
         UserAccount('user9', 'j*X4vRdN'),
         UserAccount('user10', 'M2w!QkZ8'),
         UserAccount('user11', 'o@S3tVbP'),
         UserAccount('user12', 'R6b#NfDk'),
         UserAccount('user13', 'k*P8uQjL'),
         UserAccount('user14', 'Z@5tWnC4'),
         UserAccount('user15', 'H7x!M1rJ'),
         UserAccount('user16', 'n#L2vXoT'),
         UserAccount('user17', 'W@9fGmR6'),
         UserAccount('user18', 'Q5r*JpZ7'),
         UserAccount('user19', 'm#Y2dCk8'),
         UserAccount('user20', 'L3b!TzX1'),
         UserAccount('user21', 'G4@dVxLp'),
         UserAccount('user22', 't*H7wKrP'),
         UserAccount('user23', 'R2#nBcYj'),
         UserAccount('user24', 'M8@xZqLr'),
         UserAccount('user25', 'p!J4fVtB'),
         UserAccount('user26', 'W#5uNkLz'),
         UserAccount('user27', 'C3*vQjRh')]

print('Username | Password | Hash | Password Matches Hash')

for user in users:
    # Generate a SHA-256 hash using the default settings for flask_hashing and
    # the salt value we defined earlier. This function returns the hash as a 64
    # character string in hexadecimal.
    password_hash = hashing.hash_value(user.password, PASSWORD_SALT)
    
    # Check whether the hash matches the original password. We don't really
    # need to do this here: this is just to show how your web app would check a
    # password supplied by the user (user.password) against a hash value
    # retrieved from the database (password_hash). Note that your application's
    # salt value is also required when checking a password.
    # 
    # This returns True if the password matches, or False if it doesn't.
    password_matches_hash = hashing.check_value(password_hash, user.password, PASSWORD_SALT)

    # Output username, password, hash, and the result of our verification test.
    # 
    # Note that username is never actually used when generating the hash or
    # checking a password. We only include username here for display purposes,
    # to make it easier for you to copy the right password for each user when
    # creating your database population script.
    print(f'{user.username} | {user.password} | {password_hash} | {password_matches_hash}')