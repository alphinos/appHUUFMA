import os

from flask import Flask, redirect

from . import home
from . import bp_solver

def create_app( test_config = None ):

    #Create app and configure the app
    app = Flask( __name__, instance_relative_config = True )
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join( app.instance_path, "huufma.sqlite" )
    )

    if test_config is None:
        # Load the instance config if it exists when not testing
        app.config.from_pyfile( "config.py", silent = True )
    else:
        # Load the test config if passed in
        app.config.from_mapping( test_config )

    @app.route( "/" )
    def start():
        return redirect( "/home" )
    
    app.register_blueprint( home.bp )

    app.register_blueprint( bp_solver.bp )

    return app