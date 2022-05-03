# Flask

- create an application
```py
from flask import Flask
app = Flask(__name__)

app.run() # to run the application (debug=True => to enable debug)
```

- create a blueprint (extension of application)
```py
from flask import Blueprint

_ = Blueprint('name', __name__, url_prefix='/route_prefix')

app.register_blueprint(_) # to register a blueprint
```

- set a route
```py
# to get a parameter => type: int; name: id
# 'methods' sets the methods allowed
@app.route('/routename/<int:id>', methods=['POST'])
def mymethod(id): pass
```

- get input
```py
from flask import request

request.method # get the method used (GET, POST, PUT...)
request.form # get form content
request.authorization # get authorization information (username, password)

request.get_json() # get json body of POST request
```

- define output
```py
from flask import render_template, jsonify

# the methods return a string

render_template('index.html', param=value) # 'index.html' must be in 'templates' (a subfolder of the script's folder)

jsonify({ "message": "this will be converted" }) # converts the object into a JSON string
```

- redirect to a route: `redirect('/route')` (`from flask import redirect`)

- configure the SQLite database to use:
```py
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///path-to-the-sqlite.db" # mysql://username:password@server/db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```
