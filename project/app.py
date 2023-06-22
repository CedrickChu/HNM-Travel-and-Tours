from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/more")
def learnmore():
  return render_template('learnMore.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)

