from flaskjournal import app

# this allows to run the app with 'python <filename>' instead of first setting up the env. variable with 'export FLASK_APP=flaskjournal.py' and running the app with 'flask run'
if __name__ == '__main__':
	# debug=True replaces setting up the env. variable with 'export FLASK_DEBU1(blogenv)'
	app.run(debug=True)