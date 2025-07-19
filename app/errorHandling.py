errors = []

def setError(error):
    errors.append(error)

def errorExists():
    if len(errors) > 0:
        return True
    else:
        return False
    
def removeErrors():
    global errors
    errors = []

def getErrors():
    return errors