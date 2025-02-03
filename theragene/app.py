from flask import Flask, render_template

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for an about page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
