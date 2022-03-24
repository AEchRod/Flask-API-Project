from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField #this means we will have two inputs.
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'asdf'

crypto_prices = [
    {"name": "BTC",
     "price": 44000},
    {"name": "ETH",
     "price": 3000},
    {"name": "Chafacoin",
     "price": 20}
]

messages = [{'title': 'Welcome to ChafAPI main page.',
             'content': 'To login click above'},
            #{'title': 'Message Two',
             #'content': 'Message Two Content'}
            ]

portfolio = []

#this is to create a form using flask wtf forms.
class NameForm(FlaskForm): #this class INHERITS from FlaskForm.
    name = StringField("What is your name?", validators=[DataRequired()]) #the validator ensures the field is not submitted empty.
    password = PasswordField("What's your password", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET'])
def welcomepage():
    #return "Welcome to ChafAPI's main page"
    return render_template('ChafAPI2index.html', messages=messages) #this makes the variable accessible to html.

@app.route('/crypto/', methods=['GET'])
def get_list():
    return jsonify({'crypto_prices': crypto_prices}), render_template('ChafAPI2crypto.html', crypto_prices=crypto_prices) #this converts the store variable, which has a list of dictionaries into a json. we need to convert it to as dict to process it.

# GET /crypto/<string:name> (get a crypto and return some data about it)
@app.route('/crypto/<string:name>', methods=['GET']) #<string:name means that our parameter can have a name>
def get_prices(name):
    return next(crypto for crypto in crypto_prices if crypto['name'] == name) #next() to search the list of dictionaries.


@app.route('/login', methods=['GET', 'POST']) #<string:name means that our parameter can have a name>
def login():
    if request.method == "POST": #this check to see if the request method is POST.
        user = request.form["nm"] #this stores username data.
        return redirect(url_for("user", usr=user))
    else:
        return render_template("ChafAPI2login.html")



@app.route('/loginwtf', methods=['GET', 'POST']) #when form is first navigated to, the server receives a GET request.
def loginwtf():
    name = None #this is set to None as name is not known
    form = NameForm() #this variable contains the NameForm() class.
    if form.validate_on_submit(): 
        name = form.name.data
        form.name.data = ''
    return render_template("ChafAPI2loginwtf.html", form=form, name=name)


@app.route('/portfolio/', methods=['GET'])
def create_portfolio():

    return jsonify({'portfolio': portfolio})


@app.route('/portfolio/<string:name>', methods=['GET', 'POST'])
def add_to_portfolio(name):

    request_data = request.get_json()


    if request.method == 'POST':

        for crypto in crypto_prices:
            if crypto['name'] == name:
                add_portfolio = {
                    "name": request_data['name'],
                    "price": request_data['price']}
                portfolio.append(add_portfolio)
                return jsonify({'portfolio': portfolio})
            else:
                return jsonify({'message': 'Unable to add crypto to portfolio'})

    if request.method == 'GET':
        return jsonify({'portfolio': portfolio})



if __name__ == "main":
    app.run(port=5000, debug= True) #debug= True means that we won't have to restart our app every time we make a change.







