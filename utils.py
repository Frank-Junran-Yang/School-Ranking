def digit(p):
    digits='1234567890'
    for digit in digits:
        for i in p:
            if i==digit:
                return True
    return False

def char(p):
    chars='abcdefghijklmnopqrstuvwxyz'
    for char in chars:
        for i in p:
            if i==char:
                return True
    return False

def capital(p):
    capitals='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for capital in capitals:
        for i in p:
            if i==capital:
                return True
    return False


def onetype(name):
    publics=PublicSchools.query.all()
    boardings=BoardingSchools.query.all()
    privates=PrivateSchools.query.all()
    for public in publics:
        if name==public.name:
            return 'publicschool'
    for boarding in boardings:
        if name==boarding.name:
            return 'boardingschool'
    for private in privates:
        if name==private.name:
            return 'privateschool'


def alltype(name):
    publics=PublicSchools.query.all()
    boardings=BoardingSchools.query.all()
    privates=PrivateSchools.query.all()
    type=[]
    for public in publics:
        if name==public.name:
            type.append('publicschool')
    for boarding in boardings:
        if name==boarding.name:
            type.append('boardingschool')
    for private in privates:
        if name==private.name:
            type.append('privateschool')
    return type

def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele  
        str1 += ','

    return str1[0:-1]