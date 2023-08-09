
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

from . import hu_instance_gen as hu_gen
from . import hu_utility as hu_util
from . import hu_solver

bp = Blueprint( "bp_solver", __name__, url_prefix = "/solver" )

@bp.route( "/", methods = [ "GET", "POST" ] )
def solver():

    logo = url_for( 'static', filename = 'LORE-logo-black.png' )
    patients = session.get( "patients" )
    ranges = [ "", "Muito baixa", "Baixa", "Média", "Alta", "Muito alta" ]

    if request.method == "POST":

        gen_suggestion = request.form.get( "suggestion" )
        gen_instances = request.form.get( "instances" )

        print( gen_suggestion, gen_instances )

        if gen_suggestion is not None:
            total_patients = request.form.get( "total_patients", type = int )
            beds_uti = request.form.get( "beds_uti", type = int )
            beds_utsi = request.form.get( "beds_utsi", type = int )
            beds_utp = request.form.get( "beds_utp", type = int )

            s_patients = list[ hu_util.Patient ]()

            for i in range( total_patients ):
                patient_name = request.form.get( f"name_{ i + 1 }" )
                surviving_chance = request.form.get( f"surviving_chance{ i + 1 }", type = int )
                uti_chance = request.form.get( f"select_uti_{ i + 1 }", type = int )
                utsi_chance = request.form.get( f"select_utsi_{ i + 1 }", type = int )
                utp_chance = request.form.get( f"select_utp_{ i + 1 }", type = int )

                s_patients.append( hu_util.Patient( patient_name, surviving_chance, uti_chance, utsi_chance, utp_chance ) )
            
            solution = hu_solver.solverHU( s_patients, beds_uti, beds_utsi, beds_utp )

            session[ "solution" ] = solution

            # return solution
            return redirect( url_for( "bp_solver.answer" ) )
        
        if gen_instances is not None:

            print( "Tá mudando" )
            
            i_uti = int( request.form.get( "int_uti" ) )
            i_utsi = int( request.form.get( "int_utsi" ) )
            i_utp = int( request.form.get( "int_utp" ) )

            n_patients = hu_gen.genQtdPatients( i_uti, i_utsi, i_utp )

            patients = hu_gen.generatePatientList( n_patients )

            session[ "patients" ] = patients
            session[ "n_patients" ] = n_patients
            session[ "n_uti" ] = i_uti
            session[ "n_utsi" ] = i_utsi
            session[ "n_utp" ] = i_utp

            return redirect( url_for( "bp_solver.solver" ) )

            return render_template( "solver/solver.html.jinja", logo = logo,
                                   n_patients = n_patients, n_uti = i_uti, n_utsi = i_utsi, n_utp = i_utp,
                                   ranges = ranges, range = range,
                                   enumerate = enumerate, patients = patients )

        try:
            n_patients = int( request.form.get( "n_patients" ) )
            n_uti = int( request.form.get( "p_uti" ) )
            n_utsi = int( request.form.get( "p_utsi" ) )
            n_utp = int( request.form.get( "p_utp" ) )

            if n_patients < 0:
                n_patients = 0
            if n_uti < 0:
                n_uti = 0
            if n_utsi < 0:
                n_utsi = 0
            if n_utp < 0:
                n_utp = 0

        except Exception as e:
            n_patients = 0
            n_uti = 0
            n_utsi = 0
            n_utp = 0
            print( e )

        patients = [ [ f"patient_{ i + 1 }", 0, 0, 0, 0 ] for i in range( n_patients ) ]

        session[ "patients" ] = patients
        session[ "n_patients" ] = n_patients
        session[ "n_uti" ] = n_uti
        session[ "n_utsi" ] = n_utsi
        session[ "n_utp" ] = n_utp

        return redirect( url_for( "bp_solver.solver" ) )
        return render_template( "solver/solver.html.jinja", logo = logo,
                               n_patients = n_patients, n_uti = n_uti, n_utsi = n_utsi, n_utp = n_utp,
                               ranges = ranges, range = range,
                               enumerate = enumerate, patients = patients )

    n_patients = session.get( "n_patients" )
    n_uti = session.get( "n_uti" )
    n_utsi = session.get( "n_utsi" )
    n_utp = session.get( "n_utp" )

    if not n_patients:
        n_patients = 0
    if not n_uti:
        n_uti = 0
    if not n_utsi:
        n_utsi = 0
    if not n_utp:
        n_utp = 0

    return render_template( "solver/solver.html.jinja", logo = logo,
                           n_patients = n_patients, n_uti = n_uti, n_utsi = n_utsi, n_utp = n_utp,
                           ranges = ranges, range = range,
                           enumerate = enumerate, patients = patients )

@bp.route( "/answer",  methods = [ "GET", "POST" ] )
def answer():

    logo = url_for( 'static', filename = 'LORE-logo-black.png' )

    # content = request.args.keys()
    # print( content )

    # solution = request.args[ "solution" ]
    solution = session[ "solution" ]

    return render_template( "solver/answer.html.jinja", logo = logo, solution = solution, enumerate = enumerate )