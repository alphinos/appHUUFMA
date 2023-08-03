
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint( "bp_solver", __name__, url_prefix = "/solver" )

@bp.route( "/", methods = [ "GET", "POST" ] )
def solver():

    if request.method == "POST":
        pass

    return render_template( "solver/solver.html" )