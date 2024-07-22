from flask import Flask

app = Flask(__name__)
app.secret_key = 'Example Secret Key (Change this!)'

from tree_message_board import user
from tree_message_board import staff
from tree_message_board import admin