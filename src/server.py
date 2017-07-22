from flask import Flask, jsonify

from mmda import config
from mmda.api import v1


app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(v1.blueprint, url_prefix='/v1')


@app.route('/')
def root():
    return jsonify(
        name='TV5-MMDA Traffic Monitoring API',
    )


if __name__ == '__main__':
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
