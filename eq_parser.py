import cexprtk

def resolver(symbol):
    if symbol == "x" or symbol == "y":
        value = 0.0
        return (True, cexprtk.USRSymbolType.VARIABLE, value, "")
    errormsg = "Unknown variable " + symbol
    return (False, cexprtk.USRSymbolType.VARIABLE, 0.0, errormsg)

def CreateEq(str_eq):
    st = cexprtk.Symbol_Table({})
    eqation = cexprtk.Expression(str_eq, st, resolver)