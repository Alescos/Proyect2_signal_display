# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:45:27 2020

@author: ASUS
"""
import scipy.io as sio;
import matplotlib.pyplot as plt;
import numpy as np;
import scipy.signal as signal;
from chronux.mtspectrumc import mtspectrumc
class Biosenal(object):
    def __init__(self,data=None):
        if not data==None:
            self.asignarDatos(data)
        else:
            self.__data=np.asarray([])
            self.__canales=0
            self.__puntos=0
    def asignarDatos(self,data,key,fs):
        self.__data=data
        self.__key=key
        self.__datos_key=np.squeeze(data[key])
        self.__fs=int(fs)
    def determinarTiempo(self):
        self.__tiempo=np.arange(0,len(self.__datos_key)/self.__fs,1/self.__fs)
        return self.__tiempo
    def devolver_segmento(self,x_min,x_max):
        #prevengo errores logicos
        if x_min>=x_max:
            return None
        #cojo los valores que necesito en la biosenal
        return self.__datos_key[x_min:x_max]
    
    def escalar_senal(self,x_min,x_max,escala):
        copia_datos=self.__datos_key[x_min:x_max].copy()
        return copia_datos*escala
    
    #analisis usando welch

    def period_welch(self,ventana,longitud,solapamiento):
        #signal.welch(x, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, 
        #detrend='constant', return_onesided=True, scaling='density', axis=-1)
        noverlap=longitud*(solapamiento/100)
        welch = signal.welch(self.__datos_key,self.__fs,ventana,longitud,noverlap,scaling='density')
        return welch
    def multitaper(self,frec1,frec2,W,T,P,num_seg):
        params = dict(fs = self.__fs, fspass=[frec1,frec2], tapers=[W,T,P], trialave = 1)
        x= int(self.__datos_key.shape[0]/(self.__fs*num_seg))
        datos=self.__data[self.__key]
        datos=datos[:self.__fs*num_seg*x]
        print(datos)
        data=np.reshape(datos,(self.__fs*num_seg, x),order='F')
        Pxx, f = mtspectrumc(data, params)
        return f,Pxx
    def wavelet(self):
        pass
