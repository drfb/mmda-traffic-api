from flask import Flask

from mmda import config
from mmda.api import v1


app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(v1.blueprint, url_prefix='/v1')

if __name__ == '__main__':
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
