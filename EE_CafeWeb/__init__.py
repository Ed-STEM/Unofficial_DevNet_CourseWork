import os
from flask import (Flask, render_template)
from flask_wtf.csrf import (CSRFProtect, CSRFError)

secret_key = os.urandom(20)
cookie_value = os.urandom(45)

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
    
        #Database mapping
    app.config.from_mapping(SECRET_KEY=secret_key,DATABASE=os.path.join(app.instance_path, 'EE_CafeWeb.sqlite'))

    #Security Features
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    
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
    
#    @app.after_request
#    def apply_caching(response):
#        response.headers["X-Frame-Options"]="SAMEORIGIN"
#        response.headers["Content-Security-Policy"]="default-src 'self';"
#        response.headers["X-Permitted-Cross-Domain-Policies"]="master-only"
#        response.headers["X-XSS-Protection"]="1, mode=block"
#        response.headers["X-Download-Options"]="noopen"

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('error.html',reason=e.description), 400
    
#    from . import db
#    db.init_app(app)

    #@blueprint_home.route('/comingsoon', methods=(['GET']))
    #def comingsoon():
    #    try:
    #        session['name'] = "Coming Soon Splash Page."
    #        return render_template('home/comingsoon.html', code =302)
    #    except:
    #        return render_template('home/home.html')

    from . import db
    try:
        db.init_app(app)
    except Error as err_num:
        print("Error Initializing database.")
        print(err_num)

    return app

