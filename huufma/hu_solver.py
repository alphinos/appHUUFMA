import gurobipy as grbp
from gurobipy import GRB
from . import hu_utility as hu_util

def solverHU( patients : list[ hu_util.Patient ], qtdUTI : int, qtdUTSI : int, qtdUTP : int ) -> list:

    print( *patients )
    print( qtdUTI )
    print( qtdUTSI )
    print( qtdUTP )

    qtd_patients = len( patients )
    
    qtdBeds = qtdUTI + qtdUTSI + qtdUTP

    q = [ qtdUTI, qtdUTSI, qtdUTP ]

    ls_uti = list( range(qtdUTI) )
    ls_utsi = list( range( qtdUTI, qtdUTI + qtdUTSI ) )
    ls_utp = list( range( qtdUTI + qtdUTSI, qtdBeds) )

    K_Types = [ ls_uti, ls_utsi, ls_utp ]
    
    I = list( range( qtd_patients ) )
    J = [ 0, 1, 2 ] # 0 = uti | 1 = utsi | 2 = utp
    K = list( range(qtdBeds) )

    m = grbp.Model()
    x = m.addVars( qtd_patients, 3, qtdBeds, vtype = GRB.BINARY)

    #Objective function
    sum_prioridade = 0
    for i1 in I:
        for i2 in I:
            if i1 == i2:
                continue
            for j in J:
                for k in K_Types[j]:
                    # Cada item de patients é uma lista
                    # Na posição 0, está a chance de sobrevivência
                    # Na posição 1, está uma lista com as prioridades de cada paciente
                    # para cada tipo de leito
                    if patients[i1].ls_beds[j] > patients[i2].ls_beds[j]:
                        sum_prioridade += x[i1, j, k] - x[i2, j, k]

    sum_ = 0
    for i in I:
        for j in J:
            for k in K_Types[j]:
                sum_ += x[i, j, k] * patients[i].surviving_chance

    m.setObjective( sum_ + sum_prioridade, sense = grbp.GRB.MAXIMIZE )

    # Constraints

    # C1
    for j in J:
        for k in K_Types[j]:
            sum_c1 = 0
            for i in I:
                sum_c1 += x[i, j, k]
            
            m.addConstr( sum_c1 <= 1 )
    
    # C2
    for i in I:
        sum_c2 = 0
        for j in J:
            for k in K_Types[j]:
                sum_c2 += x[i, j, k]
        
        m.addConstr( sum_c2 <= 1 )
    
    # C3
    for j in J:
        sum_c3 = 0
        for i in I:
            for k in K_Types[j]:
                sum_c3 += x[i, j, k]
        
        m.addConstr( sum_c3 <= q[j] )
    
    #Execute
    m.optimize()

    # Gerar dados de retorno

    suggestion = list()

    allocated_uti = list()
    allocated_utsi = list()
    allocated_utp = list()

    non_allocated = list()

    suggestion = [ allocated_uti, allocated_utsi, allocated_utp, non_allocated ]

    for j in J:
        for k in K_Types[j]:
            for i in I:
                print( patients[i].name, patients[i].surviving_chance, patients[i].uti_chance, patients[i].utsi_chance, patients[i].utp_chance )
                if x[i, j, k].X == 1:
                    patients[ i ].allocated = True
                    patient_ = [ patients[i].name, patients[i].surviving_chance, patients[i].uti_chance, patients[i].utsi_chance, patients[i].utp_chance ]
                    suggestion[ j ].append( patient_ )
    
    print()
    print()

    for patient in patients:
        print( patient.name, patient.surviving_chance, patient.uti_chance, patient.utsi_chance, patient.utp_chance )
        if patient.allocated == False:
            patient_ = [ patient.name, patient.surviving_chance, patient.uti_chance, patient.utsi_chance, patient.utp_chance ]
            non_allocated.append( patient_ )
    
    return suggestion