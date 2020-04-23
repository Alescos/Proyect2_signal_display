# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:05:09 2020

@author: ASUS
"""
#%%ñibrerias
import sys
#Qfiledialog es una ventana para abrir yu gfuardar archivos
#Qvbox es un organizador de widget en la ventana, este en particular los apila en vertcal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog,QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator

from matplotlib.figure import Figure

from PyQt5.uic import loadUi

from numpy import arange, sin, pi
#contenido para graficos de matplotlib
from matplotlib.backends. backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import scipy.io as sio
import numpy as np
# clase con el lienzo (canvas=lienzo) para mostrar en la interfaz los graficos matplotlib, el canvas mete la grafica dentro de la interfaz
class MyGraphCanvas(FigureCanvas):
    #constructor
    def __init__(self, parent= None,width=5, height=4, dpi=100):
        
        #se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        self.axes = self.fig.add_subplot(111)
        
        #llamo al metodo para crear el primer grafico
        self.compute_initial_figure()
        
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self,self.fig)
        
    #este metodo me grafica al senal senoidal que yo veo al principio, mas no senales
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t,s)
        
        
    #hay que crear un metodo para graficar lo que quiera
    def graficar_gatos(self,datos,tiempo):
        #primero se necesita limpiar la grafica anterior
        self.axes.clear()
        #ingresamos los datos a graficar
        if len(datos)<=len(tiempo):
            self.axes.plot(tiempo[0:len(datos)],datos)
        else: 
            self.axes.plot(tiempo,datos[0:len(tiempo)])
        #y lo graficamos
        print("datos")
        #voy a graficar en un mismo plano varias senales que no quecden superpuestas cuando uso plot me pone las graficas en un mismo grafico
        #self.axes.plot(tiempo,datos)
        self.axes.set_xlabel("tiempo")
        self.axes.set_ylabel("voltaje (uV)")
        #self.axes.set
        #ordenamos que dibuje
        self.axes.figure.canvas.draw()
        
    def graficar_metodo(self,datos,f,fmin,fmax):
        self.axes.clear()
        self.axes.set_xlabel("Frcuencia")
        self.axes.set_ylabel("Amplitud")
        frec_min=float(fmin)
        frec_max=float(fmax)
        self.axes.plot(f[(f >= frec_min) & (f <= frec_max)],datos[(f >= frec_min) & (f <= frec_max)])
        self.axes.figure.canvas.draw()
        
    def graficar_espectro(self,time, freqs, power,frec1,frec2):
        #primero se necesita limpiar la grafica anterior
        self.axes.clear()
        #ingresamos los datos a graficar
        self.axes.contourf(time,
                 freqs[(freqs >= frec1) & (freqs <= frec2)],
                 power[(freqs >= frec1) & (freqs <= frec2),:],
                 20, # Especificar 20 divisiones en las escalas de color 
                 extend='both')
        #ordenamos que dibuje
        self.axes.figure.canvas.draw()
        

       
        
class InterfazGrafico(QMainWindow):
    #condtructor
    def __init__(self):
        #siempre va
        super(InterfazGrafico,self).__init__()
        #se carga el diseno
        loadUi ('anadir_grafico.ui',self)
        #se llama la rutina donde configuramos la interfaz
        self.setup()
    def setup(self):
        self.solapamiento.setValidator(QIntValidator(0, 10000000))
        self.longitud_ventana2.setValidator(QIntValidator(0, 10000000))
        self.ancho_ventana.setValidator(QIntValidator(0, 10000000))
        self.fmin2.setValidator(QIntValidator(0, 10000000))
        self.fmax2.setValidator(QIntValidator(0, 10000000))
        self.integrador.setValidator(QIntValidator(0, 10000000))
        #los layout permiten organizar widgets en un contenedor
        #esta clase permite añadir widget uno encima del otro (vertical)
        layout = QVBoxLayout()
        #se añade el organizador al campo grafico
        self.campo_grafico.setLayout(layout)
        #se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_grafico, width=5, height=4, dpi=100)
        #se añade el campo de graficos
        layout.addWidget(self.__sc)
         
        layout2 = QVBoxLayout()
        #se añade el organizador al campo grafico
        self.campo_grafico2.setLayout(layout2)
        #se crea un objeto para manejo de graficos
        self.__sc2 = MyGraphCanvas(self.campo_grafico2, width=5, height=4, dpi=100)
        #se añade el campo de graficos
        layout2.addWidget(self.__sc2)
        
        #se organizan las señales 
        self.boton_cargar.clicked.connect(self.cargar_senal)
        self.boton_adelante.clicked.connect(self.adelante_senal)
        self.boton_atras.clicked.connect(self.atrasar_senal)
        self.boton_aumentar.clicked.connect(self.aumentar_senal)
        self.boton_disminuir.clicked.connect(self.disminuir_senal)
        self.cargar_key.clicked.connect(self.ingreso_key)
        self.metodo_welch.clicked.connect(self.elegir_metodo)
        self.metodo_multitaper.clicked.connect(self.elegir_metodo)
        self.metodo_wavelet.clicked.connect(self.elegir_metodo)
        self.cargar_welch.clicked.connect(self.determinar_welch)
        self.cargar_multi.clicked.connect(self.determinar_multi)
        self.cargar_tiempo.clicked.connect(self.graficar_tiempo)
        self.cargar_wavelet.clicked.connect(self.determinar_wavelet)

        
        #Se deshabilitan los botones
        self.cargar_tiempo.setEnabled(False)
        self.cargar_key.setEnabled(False)
        self.boton_adelante.setEnabled(False)
        self.boton_atras.setEnabled(False)
        self.boton_aumentar.setEnabled(False)
        self.boton_disminuir.setEnabled(False)
        self.metodo_welch.setEnabled(False)
        self.metodo_multitaper.setEnabled(False)
        self.tipo_ventana.setEnabled(False)
        self.cargar_welch.setEnabled(False)
        self.metodo_wavelet.setEnabled(False)
        self.cargar_wavelet.setEnabled(False)
        self.cargar_tiempo.setEnabled(False)
        self.num_seg.setEnabled(False)
        
    
    def asignar_Controlador(self,controlador):
        self.__coordinador=controlador
        
    #Funciones de los botones
    
    def adelante_senal(self):
        self.__x_min=self.__x_min+2000
        self.__x_max=self.__x_max+2000
        tiempo=self.__coordinador.determinarTiempo()
        self.__sc.graficar_gatos(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max),tiempo)
        
    def ingreso_key(self):
        key=str(self.key_text.text())
        fs=float(self.fmuestreo_text.text())
        self.__coordinador.recibirDatosSenal(self.__data,key,fs)
        tiempo=self.__coordinador.determinarTiempo()
        datos = self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max)
        self.__sc.graficar_gatos(datos,tiempo)
        
    def atrasar_senal(self):
        #que se salga de la rutina si no puede atrazar
        if self.__x_min<2000:
            return
        self.__x_min=self.__x_min-2000
        self.__x_max=self.__x_max-2000
        tiempo=self.__coordinador.determinarTiempo()
        self.__sc.graficar_gatos(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max),tiempo)
        
    def aumentar_senal(self):
        #en realidad solo necesito limites cuando tengo que extraerlos, pero si los 
        #extraigo por fuera mi funcion de grafico puede leer los valores
        tiempo=self.__coordinador.determinarTiempo()
        self.__sc.graficar_gatos(self.__coordinador.escalarSenal(self.__x_min,self.__x_max,2),tiempo)
        
    def disminuir_senal(self):
        tiempo=self.__coordinador.determinarTiempo()
        self.__sc.graficar_gatos(self.__coordinador.escalarSenal(self.__x_min,self.__x_max,0.5),tiempo)
        
    def elegir_metodo(self):
        if self.metodo_welch.isChecked()==True:
            self.tipo_ventana.setEnabled(True)
            self.cargar_welch.setEnabled(True)
            self.num_seg.setEnabled(False)
            self.cargar_multi.setEnabled(False)
            self.cargar_wavelet.setEnabled(False)
        
        elif self.metodo_multitaper.isChecked()==True:
            self.num_seg.setEnabled(True)
            self.cargar_multi.setEnabled(True)
            self.tipo_ventana.setEnabled(False)
            self.cargar_welch.setEnabled(False)
            self.cargar_wavelet.setEnabled(False)

        else:
            self.cargar_wavelet.setEnabled(False)
            self.num_seg.setEnabled(False)
            self.tipo_ventana.setEnabled(False)
            self.cargar_welch.setEnabled(False)
            self.cargar_multi.setEnabled(False)
            self.num_seg.setEnabled(False)
            self.cargar_wavelet.setEnabled(True)
            
    def determinar_welch(self):
        ventana=self.tipo_ventana.currentText()
        longitud=float(self.longitud_ventana.text())
        frec1=float(self.fmin1.text())
        frec2=float(self.fmax1.text())
        solapamiento=float(self.solapamiento.text())
        f,welch=self.__coordinador.period_welch(ventana,longitud,solapamiento)
        self.__sc2.graficar_metodo(welch,f,frec1,frec2)
    
    def determinar_multi(self):
        T=float(self.longitud_ventana2.text())
        W=float(self.ancho_ventana.text())
        frec1=float(self.fmin2.text())
        frec2=float(self.fmax2.text())
        print(type(frec1))
        P=float(self.integrador.text())
        num_seg=int(self.num_seg.currentText())
        f,multi=self.__coordinador.multitaper(frec1,frec2,W,T,P,num_seg)
        self.__sc2.graficar_metodo(multi,f,frec1,frec2)
        
    def determinar_wavelet(self):
        frec1=float(self.fmin3.text())
        frec2=float(self.fmax3.text())
        time, freqs, power=self.__coordinador.wavelet(frec1,frec2)
        self.__sc2.graficar_espectro(time, freqs, power, frec1, frec2)
    
    def graficar_tiempo(self): 
        #'''
       # Esta funcion permite obtener un segmento cualquiera de la se�al de entrada
       # y de la senal filtrada. Recibe los valores de tiempo minio y maximo.
        #'''
        
        time_min = int(self.tiempo_min.text())
        time_max = int(self.tiempo_max.text())
        
        #canal = int(self.canal_filtro.text())
        senal=self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max)
        #nivel = int(self.nivel_filtrado.currentIndex())
        #forma = int(self.forma_filtrado.currentIndex())
        #umbral = int(self.tipo_umbral.currentIndex())

        self.__x_min = time_min
        self.__x_max = time_max
        
    #Carga la senal 
    def cargar_senal(self):
        #se abre el cuadro de dialogo para cargar
        #* son archivos .mat
        archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Abrir señal","","Todos los archivos (*);;Archivos mat (*.mat)*")
        if archivo_cargado != "":
            print(archivo_cargado)
            #la senal carga exitosamente entonces habilito los botones
            self.__data = sio.loadmat(archivo_cargado)
            #volver continuos los datos
            ##data = data["data"]
            #volver continuos los datos
            ##sensores,puntos,ensayos=data.shape
            ##senal_continua=np.reshape(data,(sensores,puntos*ensayos),order="F")
            #el coordinador recibe y guarda la senal en su propio .py, por eso no 
            #necesito una variable que lo guarde en el .py interfaz
            self.__x_min=0
            self.__x_max=2000        
            self.cargar_tiempo.setEnabled(True)
            self.cargar_key.setEnabled(True)
            self.boton_adelante.setEnabled(True)
            self.boton_atras.setEnabled(True)
            self.boton_aumentar.setEnabled(True)
            self.boton_disminuir.setEnabled(True)
            self.metodo_welch.setEnabled(True)
            self.metodo_multitaper.setEnabled(True)
            self.metodo_wavelet.setEnabled(True)
            self.campo_grafico2.setEnabled(True)
            self.cargar_tiempo.setEnabled(True)
            
        

        