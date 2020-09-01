import pandas as pd
import statistics as st
import scipy
import scipy as sp
from scipy.stats import t
import numpy as np
import os

sca=["./SCA/"]
vec=["./VEC/"]

def mean_confidence_interval1(data, confidence=0.95):
    a = 1*(data)
    n = len(a)
    se =scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1 + confidence) / 2., n-1)
    return h

def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

def running_avg(x):
    return np.cumsum(x) / np.arange(1, x.size + 1)
def read(value):
    valCsvVec = pd.read_csv(value,encoding='utf-8',converters = {
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray} )
    return valCsvVec
def readSca(val):

    valCsvSca= pd.read_csv(val, encoding='utf-8', converters = {
        'value': parse_if_number})
    return valCsvSca
for scaPath, vecPath in zip((sca), (vec)):
    for fileSca, fileVec in zip(os.listdir(scaPath),os.listdir(vecPath)):
        print(fileVec)
        print(fileSca)
# Perfetto funziona
index=0

for scaPath, vecPath in zip((sca), (vec)):
    if index==1:
        print()
    if index==1:
        mu=st.mean([1,6])
    elif index==2:
        mu = st.mean([2, 4])
    for fileSca, fileVec in zip(os.listdir(scaPath),os.listdir(vecPath)):
        inp=vecPath+fileVec
        valCsvVec=read(vecPath+fileVec)
        valueServiceTimeNetwork=[]
        valueServiceTimeSPTF=[]
        valueServiceTimeQueue=[]
        valueLifeTime=[]
        valueLifeTimeMax =[]
        valueLifeTimeMin=[]
        valueBustTvgSptf=[]
        meanSPTF=[]
        valueBustTvgQueue=[]
        meanQueue=[]
        valCsvSca = readSca(scaPath+fileSca)
        valuerho=[]
        codaSP=[]
        codaQueu=[]
        prova=[]
        '''
        [1,3,5....]
        res=1-3
        3-5
        [media res ]
        lamb=1/media res 
        mu =1/media service time 
        '''

        for name,module,vecValue,vecTime in zip(valCsvVec['name'],valCsvVec['module'],valCsvVec['vecvalue'],valCsvVec['vectime']):
            if (module == 'Network.sink' and name == 'lifeTime:vector' and vecValue is not None ):
                    valueServiceTimeNetwork.append(st.median(vecValue))
                    prova.append(st.mean(vecValue))
            if(name == 'serviceTime:vector' and vecValue is not None):
                if (module == 'Network.SPTF'):
                    valueServiceTimeSPTF.append(st.median(vecValue))
                    meanSPTF.append(st.mean(vecValue))
                elif(module == 'Network.queue'):
                    valueServiceTimeQueue.append(st.median(vecValue))
                    meanQueue.append(st.mean(vecValue))



            if((module == 'Network.sink' and name == 'lifeTime:vector' and vecValue is not None )):
                valueLifeTime.append(st.mean(vecValue))
                valueLifeTimeMax.append(max(vecValue))
                valueLifeTimeMin.append(min(vecValue))


        pr=0
        for nameSca, moduleSca, vecValueSca in zip(valCsvSca['name'], valCsvSca['module'], valCsvSca['value']):
            if (moduleSca == 'Network.SPTF' and nameSca == 'busy:timeavg' and str(vecValueSca) != "nan"):
                valueBustTvgSptf.append(vecValueSca)
                controlloexp = False
                j = False
            pr+=1
            if (moduleSca == 'Network.queue' and nameSca == 'busy:timeavg' and str(vecValueSca) != "nan"):
                valueBustTvgQueue.append(vecValueSca)
            if (moduleSca == 'Network.SPTF' and nameSca == 'queueingTime:mean' and str(vecValueSca) != "nan"):
                codaSP.append((vecValueSca))
            if (moduleSca == 'Network.queue' and nameSca == 'queueingTime:mean' and str(vecValueSca) != "nan"):
                codaQueu.append((vecValueSca))
            if (moduleSca == 'Network.sink' and nameSca == 'totalServiceTime:mean' and str(vecValueSca) != "nan"):
                valuerho.append(vecValueSca)
        for na, val in zip(valCsvSca['attrname'], valCsvSca['attrvalue']):
            if ((controlloexp and j) == True):
                break
            if (na == 'lamb' or na == 'lam'):
                if (float(val) == 0.5):
                    lambdOmnett= 2.0
                    lambdOmnettScrivere=0.5
                    j = True
                elif (float(val) == 0.7):
                    lambdOmnett = 1.4
                    lambdOmnettScrivere=0.7
                    j = True
                elif (float(val) == 0.8):
                    lambdOmnett = 1.2
                    lambdOmnettScrivere=0.8
                    j = True
                elif (float(val) == 1.0):
                    lambdOmnett = 1
                    lambdOmnettScrivere=1
                    j = True
                if (index >= 1 and j == True):
                    break
            if (na == 'expo'):
                if (float(val) == 0.33):
                    muOmnett = 3.0
                    muOmnettScrivere=0.33
                    controlloexp = True
                if (float(val) == 0.25):
                    muOmnett = 4.0
                    muOmnettScrivere =0.25
                    controlloexp = True

        print(st.mean(prova))

        print("-----------------------------------------------------")
        print(inp)
        if(index==0):
            print('lambdOmnett')
            print(muOmnett)
        else:
            print('lambdOmnett')
            print(mu)

        pr1=mean_confidence_interval1(valueServiceTimeSPTF)
        print(pr1)
        print(st.mean(valueServiceTimeNetwork))
        file1 = open("res.txt", "a")
        if index==0:
            file1.write("----------------------------------------------------------------------------\n")
            file1.write("Exponential---> λ= "+str(lambdOmnettScrivere )+" μ= " +str(muOmnettScrivere)+":\n")
        else:
            file1.write("----------------------------------------------------------------------------\n")
            file1.write("Uniform---> λ= " + str(lambdOmnettScrivere) + "μ" + str(mu) + ":\n")

        file1.write("Mediana della distriubuzione del tempo di risposta:")
        file1.write("["+str("{:.4f}".format(st.mean(valueServiceTimeNetwork)))+"±"+str("{:.4f}".format(pr1))+"] Intervallo di confidenza 95%\n")
        file1.write("Mediana della distriubuzione del tempo di risposta del servente:")
        file1.write("["+str("{:.4f}".format(st.mean(valueServiceTimeSPTF)))+"±"+str("{:.4f}".format(pr1))+"] Intervallo di confidenza 95%\n")
        file1.write("Tempo medio di permanenza nel sistema dei job:")
        file1.write("["+str("{:.4f}".format(st.mean(valueLifeTime)))+"±"+str("{:.4f}".format(pr1))+"] Intervallo di confidenza 95%\n")
        file1.write("Tempo Max di permanenza nel sistema dei job:")
        file1.write("["+str("{:.4f}".format(st.mean(valueLifeTimeMax)))+"±"+str("{:.4f}".format(pr1))+"] Intervallo di confidenza 95%\n")
        file1.write("Tempo Min di permanenza nel sistema dei job")
        file1.write("["+str((st.mean(valueLifeTimeMin)))+"±"+str(format(pr1))+"] Intervallo di confidenza 95%\n")
        file1.write("Fattore di utilizzo del server")
        file1.write("[" +str("{:.4f}".format(st.mean(valueBustTvgSptf)))+"±"+str("{:.4f}".format(pr1))+"] Intervallo di confidenza 95%\n")
        file1.write("Fattore di utilizzo del sistama risulta essere  < 1 ed il sistema può essere definito stabile\n")
        #file1.write("Risultati analitici Rho " +str("{:.4f}".format((lambdOmnett/muOmnett)))+" Rho Omnett "+str("{:.4f}".format(st.mean(valuerho)))+"\n")
        print("------------------------|||||||||||||||||||||||||||||||||||||||||--------------------------------")
        print((muOmnett))
        print(st.mean(valueServiceTimeSPTF))
        MuServenteUno=1/(st.mean(valueServiceTimeSPTF))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        MuServenteUno=1/(st.mean(valueServiceTimeQueue))

        print("Mu : "+ str(MuServenteUno))
        print(lambdOmnettScrivere)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        file1.write("------------------------------- Ws Primo Servente -------------------------------\n")
        file1.write(" (Ws Analitico) " + str("{:.4f}".format(1/(muOmnett-lambdOmnett))) + " (Ws Omnett) " + str(
                 "{:.4f}".format((st.mean(valueBustTvgSptf))+st.mean(codaSP))) + "\n")
        file1.write("------------------------------- Ws Secondo Servente -------------------------------\n")
        file1.write(" (Ws Analitico) " + str("{:.4f}".format(1 / (muOmnett - lambdOmnett))) + " (Ws Omnett) " + str(
            "{:.4f}".format((st.mean(valueBustTvgQueue))+st.mean(codaQueu))) + "\n")
        file1.write("\n")
        file1.write("\n")
#(st.mean(valueServiceTimeQueue)+st.mean(valueServiceTimeSPTF)

file1.close()



