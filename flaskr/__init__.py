import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # "instance_relative_config=True tells the app that configuration files are relative to the instance folder. The instance folder is located outside the flaskr package and can hold local data that shouldn’t be committed to version control, such as configuration secrets and the database file." 
    app.config.from_mapping(
        SECRET_KEY='dev',
        # "used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during development, but it should be overridden with a random value when deploying."
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # "the path where the SQLite database file will be saved. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder."
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        # "overrides the default configuration with values taken from the config.py file in the instance folder if it exists."
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        # "ensures that app.instance_path exists. Flask doesn’t create the instance folder automatically, but it needs to be created because your project will create the SQLite database file there."
    except OSError:
        pass


    from . import db
    db.init_app(app)

    from . import company_list
    app.register_blueprint(company_list.bp)
    app.add_url_rule('/', endpoint='index')

    return app
