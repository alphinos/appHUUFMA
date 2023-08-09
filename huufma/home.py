
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import os
from random import randint

bp = Blueprint( "home", __name__, url_prefix = "/home" )

def countFilesInDir( pathDir : str ):
    counter : int = 0
    for path in os.listdir( pathDir ):
        if os.path.isfile( os.path.join( pathDir, path ) ):
            counter += 1
    return counter

@bp.route( "/" )
def home():

    images_path = "huufma/static/show"
    chose_img = randint( 0, countFilesInDir( images_path ) - 1 )

    src_img = url_for( 'static', filename = f'show/{ chose_img }.jpg' )
    logo = url_for( 'static', filename = 'LORE-logo-black.png' )

    session[ "patients" ] = None
    session[ "n_patients" ] = 0
    session[ "n_uti" ] = 0
    session[ "n_utsi" ] = 0
    session[ "n_utp" ] = 0

    return render_template( "index.html.jinja", src_img = src_img, logo = logo )