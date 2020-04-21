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
    def recibirDatosSenal(self,data,key):
        self.__mi_biosenal.asignarDatos(data,key)
    #Entrega los datos al modelo
    def devolverDatosSenal(self,x_min,x_max):
        return self.__mi_biosenal.devolver_segmento(x_min,x_max)
    
    def escalarSenal(self,x_min,x_max,escala):
        return self.__mi_biosenal.escalar_senal(x_min,x_max,escala)
    def escogercanal(self,n):
        return self.escogercanal(n)
    def filtrarSenal(self,senal,nivel,forma,umbral):
        return self.__mi_biosenal.filtrar_senal(senal,nivel,forma,umbral);
p=Principal()
p.main()