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
import pywt #1.1.1
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
        self.__datos=np.squeeze(data[key])
        self.__datos_key=self.__datos-np.mean(self.__datos)
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
        datos=self.__datos
        datos=datos-np.mean(datos)
        print(datos)
        x= int(datos.shape[0]/(self.__fs*num_seg))
        datos=datos[:self.__fs*num_seg*x]
        print(datos)
        data=np.reshape(datos,(self.__fs*num_seg, x),order='F')
        Pxx, f = mtspectrumc(data, params)
        return f,Pxx
    def wavelet(self,frec1,frec2):
        sampling_period =  1/self.__fs
        Frequency_Band = [frec1, frec2] # Banda de frecuencia a analizar

        # Métodos de obtener las escalas para el Complex Morlet Wavelet  
        # Método 1:
        # Determinar las frecuencias respectivas para una escalas definidas
        scales = np.arange(1, 250)
        frequencies = pywt.scale2frequency('cmor', scales)/sampling_period
        # Extraer las escalas correspondientes a la banda de frecuencia a analizar
        scales = scales[(frequencies >= Frequency_Band[0]) & (frequencies <= Frequency_Band[1])] 
        
        N = self.__datos_key.shape[0]
        
        #%%
        # Obtener el tiempo correspondiente a una epoca de la señal (en segundos)
        time_epoch = sampling_period*N

        # Analizar una epoca de un montaje (con las escalas del método 1)
        # Obtener el vector de tiempo adecuado para una epoca de un montaje de la señal
        time = np.arange(0, time_epoch, sampling_period)
        # Para la primera epoca del segundo montaje calcular la transformada continua de Wavelet, usando Complex Morlet Wavelet

        [coef, freqs] = pywt.cwt(self.__datos_key, scales, 'cmor', sampling_period)
        print(coef)
        print(freqs)
        # Calcular la potencia 
        power = (np.abs(coef)) ** 2
        
        return time, freqs, power
