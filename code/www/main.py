from flask import Flask
from .index import Index

app = Flask(__name__)

@app.route('/')

def index():
    return Index.render_index()
