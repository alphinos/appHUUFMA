from random import randint
from . import hu_utility
import os

def genQtdPatients( uti : int, utsi : int, utp : int ):
    min = uti + utsi + utp
    if ( min != 0 ):
        min += 1
    qtd_Patients = randint(min, 20 * min)
    return qtd_Patients

def genPatient( i : int ):
    chance = randint(0, 100)
    uti = randint(1, 5)
    utsi = randint(1, 5)
    utp = randint(1, 5)
    
    patient = hu_utility.Patient( f"patient_{i}", chance, uti, utsi, utp )
    return patient

def generatePatientList(qtd_items: int) -> list[hu_utility.Patient]:
    return [genPatient( i ) for i in range(qtd_items)]

def writeInstances( patients : list[hu_utility.Patient], uti : int, utsi : int, utp : int  ):
    id = countFilesInDir( "huufma/static/insts" )
    qtd_patients = len( patients )
    with open( f"huufma/static/insts/inst_{ id }" ) as f:
        f.write( f"{ qtd_patients }" )
        f.write( f"{ uti } { utsi } { utp }" )

        for patient in patients:
            f.write( f"{ patient.name } { patient.surviving_chance } { patient.uti_chance } { patient.utsi_chance } { patient.utp_chance }" )

def countFilesInDir( pathDir : str ):
    counter : int = 0
    for path in os.listdir( pathDir ):
        if os.path.isfile( os.path.join( pathDir, path ) ):
            counter += 1
    return counter

