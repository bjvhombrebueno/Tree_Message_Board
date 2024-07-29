from flask import Flask
import os
app = Flask(__name__)
app.secret_key = 'Example Secret Key (Change this!)'


IMAGES_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER


from tree_message_board import user
from tree_message_board import staff
from tree_message_board import admin