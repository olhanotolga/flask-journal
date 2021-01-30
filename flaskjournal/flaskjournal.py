from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

posts = [
	{
		'author': 'Olha H.',
		'title': 'Fish',
		'content': 'As food, fish is gross.',
		'date_posted': '30th Jan 2021'
	},
	{
		'author': 'Rory Bobich',
		'title': 'Notes on turkeys',
		'content': 'Turkeys are weird and scary',
		'date_posted': '30th Jan 2021'
	}
	
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# this allows to run the app with 'python <filename>' instead of first setting up the env. variable with 'export FLASK_APP=flaskjournal.py' and running the app with 'flask run'
if __name__ == '__main__':
	# debug=True replaces setting up the env. variable with 'export FLASK_DEBU1(blogenv)'
	app.run(debug=True)