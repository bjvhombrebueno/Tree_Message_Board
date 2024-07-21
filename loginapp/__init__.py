from flask import Flask

app = Flask(__name__)
app.secret_key = 'Example Secret Key (Change this!)'

from loginapp import user
from loginapp import staff
from loginapp import admin