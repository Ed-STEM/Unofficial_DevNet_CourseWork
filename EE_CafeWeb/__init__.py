import os
from flask import (Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for)

def create_app(test_config=None):
    """
    Many of the flask parameters and functions must be used exactly so copy most of these verbatim and 
    double check any changes with official documentation. create_app instantiats the flask web app, provides the configuration
    of flask and sets up global parameters, urls, and flask functions.
    """

    app = Flask(__name__,
                instance_relative_config=True,
                static_url_path='',
                static_folder='static',
                template_folder='templates')
    
    app.config.update(
        SESSION_COOKIE_SECURE = True,
        SESSION_COOKIE_HTTPONLY = True,
        SESSION_COOKIE_SAMESITE = "Lax",
    )



    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    from . import home
    app.register_blueprint(home.blueprint_home)

    from . import dashboard
    app.register_blueprint(dashboard.blueprint_dash)

    @app.route('/test')
    def whatup():
        return 'what, up'
    
    from . import db
    db.init_app(app)

    #@blueprint_home.route('/comingsoon', methods=(['GET']))
    #def comingsoon():
    #    try:
    #        session['name'] = "Coming Soon Splash Page."
    #        return render_template('home/comingsoon.html', code =302)
    #    except:
    #        return render_template('home/home.html')

#    from . import db
#    try:
#        db.init_app(app)
#    except Error as err_num:
#        print("Error Initializing database.")
#        print(err_num)

    return app

