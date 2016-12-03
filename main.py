import rest_providers
from flask import Flask
from flask_restful import Api

# Configure the REST app
app = Flask(__name__)
api = Api(app)

# Hook up the REST providers
api.add_resource(rest_providers.OutsetsForLocation, '/outsetsForLocation')

# Run the REST application
if __name__ == '__main__':
    app.run(debug=True)
