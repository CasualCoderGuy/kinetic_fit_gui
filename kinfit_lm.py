import symfit
from lmfit import Parameters, fit_report, minimize
import scipy
from numpy import exp, sign, sin, pi, array
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import uncertainties
import asteval
import csv

def residual(pars, t, data=None, eps=None):#t=x, 
    # unpack parameters: extract .value attribute for each parameter
    parvals = pars.valuesdict()

    k = parvals['k']
    A0 = parvals['A0']
    Ainf = parvals['Ainf']

    model = (A0 - Ainf) * exp(- k * t) + Ainf

    if data is None:
        return model
    if eps is None:
        return model - data
    return (model-data) / eps

def recalc(pars, t):#t=x, 
    # unpack parameters: extract .value attribute for each parameter
    parvals = pars.valuesdict()
    k = parvals['k']
    A0 = parvals['A0']
    Ainf = parvals['Ainf']
    result = (A0 - Ainf) * exp(- k * t) + Ainf
    return result

def fit_data(filename, xstart, xend, xcorrect, kval, Aval, AinfVal, kfix, Afix, AinfFix, skipNeg):
    xdataL = []
    ydataL = []
    if ".csv" in filename:
        csvfile = open(filename)
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            if len(row) < 2:
                continue
            try:
                if xstart != 0.0 and float(row[0]) < xstart:
                    continue
                elif float(row[1]) < 0.0 and skipNeg:
                    xdataL.clear()
                    ydataL.clear()
                elif xend != 0.0 and float(row[0]) > xend:
                    break
                else:
                    xdataL.append(float(row[0]))
                    ydataL.append(float(row[1]))
            except ValueError:
                continue
    elif ".xlsx" in filename:
        print("xlsx")
    elif ".xls" in filename:
        print("xls")
    else:
        print("text")

    xdata = array(xdataL)
    data = array(ydataL)

    if xcorrect:
        if float(xcorrect) != 0.0:
            xdata += xcorrect

    fit_params = Parameters()
    fit_params.add('k', value=kval, vary=kfix)
    fit_params.add('A0', value=Aval, vary=Afix)
    fit_params.add('Ainf', value=AinfVal, vary=AinfFix)

    out = minimize(residual, fit_params, args=(xdata,), kws={'data': data})

    print(fit_report(out))

    plt.plot(xdata, recalc(out.params, xdata), c='orange')
    plt.scatter(xdata, data, s=2)
    plt.show()