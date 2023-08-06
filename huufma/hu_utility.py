
class Patient:

    name : str
    
    surviving_chance : int
    uti_chance : int
    utsi_chance : int
    utp_chance : int

    ls_beds : list[ int ]

    allocated : bool

    def __init__( self, name : str, surviving_chance : int, uti : int, utsi : int, utp : int ):
        self.name = name
        self.surviving_chance = surviving_chance
        self.uti_chance = uti
        self.utsi_chance = utsi
        self.utp_chance = utp

        self.ls_beds = [ self.uti_chance, self.utsi_chance, self.utp_chance ]

        self.allocated = False

def readInstances(file_name: str) -> list :
    file = open(file_name, "r")

    rows = file.readlines()
    values = rows[0].strip().split()
    qtd_Patients = int(values[0])

    del(rows[0])

    unities = rows[0].strip().split()
    # for i in range(len(unities)):
    #     unities[i] = int(unities[i])
    
    unities = map( int, unities )

    del(rows[0])

    lsPatients = list()
    for row in rows:
        [name, sc, utic, utsic, utpc] = row.strip().split()

        patient = Patient( name, int( sc ), int( utic ), int( utsic ), int( utpc ) )

        lsPatients.append( patient )
    
    uti = unities[0]
    utsi = unities[1]
    utp = unities[2]
    
    return lsPatients, uti, utsi, utp, qtd_Patients