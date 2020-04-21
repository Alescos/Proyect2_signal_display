# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:45:27 2020

@author: ASUS
"""
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal;
class Biosenal(object):
    def __init__(self,data=None):
        if not data==None:
            self.asignarDatos(data)
        else:
            self.__data=np.asarray([])
            self.__canales=0
            self.__puntos=0
    def asignarDatos(self,data,key):
        self.__data=data
        self.__datos_key=np.squeeze(data[key])
        self.__tiempo=np.arange(0,len(self.__datos_key)/250,1/250)
    def devolver_segmento(self,x_min,x_max):
        #prevengo errores logicos
        if x_min>=x_max:
            return None
        #cojo los valores que necesito en la biosenal
        return self.__datos_key[x_min:x_max]
    def escalar_senal(self,x_min,x_max,escala):
        copia_datos=self.__data[:,x_min:x_max].copy()
        return copia_datos*escala
    
    #analisis usando welch
    def period_welch(self,data,fs,ventana):
        f, Pxx = signal.welch(data,fs,ventana, 512*0.5, 256*0.5, 512*0.5, scaling='density')
        print(f.shape)
        plt.plot(f[(f >= 4) & (f <= 40)],Pxx[(f >= 4) & (f <= 40)])
        plt.show()

