
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint( "home", __name__, url_prefix = "/home" )

@bp.route( "/" )
def home():
    return render_template( "index.html" )