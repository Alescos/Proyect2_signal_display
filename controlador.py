# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:44:57 2020

@author: ASUS
"""
from modelo import Biosenal
from interfaz import InterfazGrafico
import sys
from PyQt5.QtWidgets import QApplication
class Principal(object):
    def __init__(self):        
        self.__app=QApplication(sys.argv)
        self.__mi_vista=InterfazGrafico()
        self.__mi_biosenal=Biosenal()
        self.__mi_controlador=Coordinador(self.__mi_vista,self.__mi_biosenal)
        self.__mi_vista.asignar_Controlador(self.__mi_controlador)
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())
    
class Coordinador(object):
    def __init__(self,vista,biosenal):
        self.__mi_vista=vista
        self.__mi_biosenal=biosenal
        self.__mi_vista.show()
        
    #Función que recibe los datos
    def recibirDatosSenal(self,data,key,fs):
        self.__mi_biosenal.asignarDatos(data,key,fs)
    #Entrega los datos al modelo
    def devolverDatosSenal(self,x_min,x_max):
        datos = self.__mi_biosenal.devolver_segmento(x_min,x_max)
        return datos    
    def escalarSenal(self,x_min,x_max,escala):
        return self.__mi_biosenal.escalar_senal(x_min,x_max,escala)
    def period_welch(self,ventana,longitud,solapamiento):
        return self.__mi_biosenal.period_welch(ventana,longitud,solapamiento)
    def multitaper(self,frec1,frec2,W,T,P,num_seg):
        return self.__mi_biosenal.multitaper(frec1,frec2,W,T,P,num_seg)
    def wavelet(self,frec1,frec2):
        return self.__mi_biosenal.wavelet(frec1,frec2)
    def determinarTiempo(self):
        return self.__mi_biosenal.determinarTiempo()
    def devolverTiempo(self,x_min,x_max):
        return self.__mi_biosenal.desplazarTiempo(x_min,x_max)
    
    def escogercanal(self,n):
        return self.escogercanal(n)
    def filtrarSenal(self,senal,nivel,forma,umbral):
        return self.__mi_biosenal.filtrar_senal(senal,nivel,forma,umbral);
p=Principal()
p.main()