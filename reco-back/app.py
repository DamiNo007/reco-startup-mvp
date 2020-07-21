from flask import Flask
from database.db import initialize_db
from views.user import users
from views.product import products

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/reco-app'
}

initialize_db(app)
app.register_blueprint(users)
app.register_blueprint(products)

app.run()


