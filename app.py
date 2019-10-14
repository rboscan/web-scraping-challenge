from Flask import Flask, render_template, redirect
import scrape_mars

app = Flask(__name__)

@app.route('/')
def index():
    