# Laboratorio-Señales
En esta practica se analizaron señales simuladas y reales recolectadas en bases de datos, calculando sus parámetros estadísticos por medio de Python, capturando la señal y evaluando la relación señal-ruido.

## **A. Descargar una señal de un ECG**

En esta primera parte del laboratorio descargamos una señal de un ECG en la base de datos de Physionet. Ya luego de descargar esta señal la importamos a Google colab para su visualizacion y un buen analisis de este.

Las librerias que se utilizaron en esta practica fueron:
```python
import numpy as np
import matplotlib.pyplot as plt
#!pip install wfdb   #Instalacion en colab
import wfdb
#pip install wfdb #Instalacion en python instalado
import pandas as pd
```
numpy: Librería para cálculos numéricos y manejo de arreglos (vectores y matrices).

matplotlib.pyplot: Sirve para generar gráficos y visualizar datos.

wfdb: Librería especializada para leer y manipular señales biomédicas del formato PhysioNet, como ECG.

pandas: Manejo de datos en forma de tablas (aunque aquí solo se importa, no se usa mucho).

## **1. Descarga e importacion de la señal**

Se selecciono una señal en la base de datos, lo suficientemente larga para poder hacer todos los calculos estadisticos necesarios de esta señal, esta señal se descargo en formato wfdb.\
Antes de poder importar la imagen se tuvo que descargar la base de datos de mitdb y creamos un objeto record usando la medicion mitdb/100.

```python
wfdb.dl_database('mitdb', dl_dir='mitdb', records=['100']) 
record = wfdb.rdrecord('mitdb/100', sampto=60*360) 
```
wfdb.dl_database: descarga registros desde PhysioNet.

'mitdb': es el nombre de la base de datos (MIT-BIH Arrhythmia Database).

dl_dir='mitdb': indica la carpeta donde se guardará.

records=['100'] significa que solo se descarga el registro número 100 (cada registro es un paciente).

Para poder importar, imprimir y mostrar la señal descargada se utilizo el siguiente codigo.

```python
signals = record.p_signal # Transformamos record al array signals
MliiSignal = signals[:,0] # Escogemos solo la señal de la columna 0

fs = 360 #Definimos fs (Frecuencia de muestreo)
nSamples  = 360*60 # Calculamos la cantidad de muestras para 60 segundos
t = [] #Creamos array vacio

for i in range(nSamples):
  tiempo = i * (1 / fs) #Multiplicamos i * Periodo de muestreo
  t.append(tiempo) #agregamos a t

print(len(t))

plt.title("Derivación segunda modificada")
plt.xlabel("Tiempos (s)")
plt.ylabel("Voltaje (mV)")
plt.plot(t[0:1000],MliiSignal[0:1000])
```

<img width="723" height="572" alt="image" src="https://github.com/user-attachments/assets/dee946f3-1e69-486e-8adb-ca8ea6a61485" />\
Figura 1. Señal de ECG visualizada en google colab

## **2. Calculos de variables estadisticos**
### **Media**

La media aritmética de una señal es su valor promedio a lo largo del tiempo. en un ECG bien centrado, la media debería estar cerca de cero si no hay drift o desplazamiento de línea base.\
Para poder sacar la media de la señal se tomo como guia la siguiente formula:

<img width="167" height="81" alt="image" src="https://github.com/user-attachments/assets/19d7aef3-1a2e-4d70-ba32-f191a72d8238" />\
Figura 2. Calculo de la media de la señal

```python
# Tenemos MliiSignal y t

acumulador = 0

for i in MliiSignal:
  acumulador = acumulador + i

media = acumulador/nSamples

print("Media:", media)
```
La media de esta señal es: -0.33634791666666564

### **Desviavion Estandar**

La desviacion estandar es la raíz cuadrada de la varianza, expresa la dispersión en las mismas unidades que la señal (milivoltios), lo que la hace más interpretable.
Valores más altos indican mayor variabilidad de voltaje en el ECG, lo que puede deberse a picos pronunciados o ruido.

<img width="259" height="93" alt="image" src="https://github.com/user-attachments/assets/f0e2a4ad-0041-4bdf-a48b-168c263044b6" />\
Figura 3. Desviacion estandar 

```python
# Tenemos MliiSignal y t

acumulador = 0

for i in MliiSignal:
  acumulador = acumulador + (i - media)**2

varianza = acumulador/(nSamples - 1)
sd = varianza**(0.5)

print("Desviación Estandar:", sd)
``` 
la desviacion estandar de la señal es: 0.17561972579326307

### **Coeficiente de variacion**

El coeficiente de variacion es una media que relaciona la dispersion relativa con la media, se expresa como el cocientre entre la desviacion estandar y la media que tomamos anterior mente.

<img width="187" height="120" alt="image" src="https://github.com/user-attachments/assets/baa9121c-76b7-4d4a-97e1-281c5289ded6" />\
Figura 4. Coeficiente de variacion

```python
Cv= sd/(media)
print("Coeficiente de variación:",Cv)
```
El coeficiente de variacion dio como resultado: -0.5221370999818301

### **Histograma**

En el Histograma se representa la distribucion de amplitudes de la señal tomada de un ECG. En el eje X indicamos los valores de amplitud en milivoltios (mV) y en el eje Y se muestra la frecuencia de aparicion de cada rango de amplitud tomada.

Para poder tomarlo se dividio la señal en 35 partes iguales, lo que nos permitio observar con mayor detalle como se distrubuyen las amplitudes.

Se puede observar que la mayor concentracion de datos se encuentran alrededor del valor de -0.4mV y -0.3mV, lo que nos indica que la mayor parte tiende a oscilar en este rango, por otro lado tambien podemos notar que la frecuencia maxima que se toma es de 5000 ocurrencias en este intervalo, lo que nos dice que este valor de amplitud es predominante en la señal.

El histograma en ECG puede servir para:

+Ver si la señal está centrada en cero (línea base estable).\
+Detectar saturaciones o desplazamientos.\
+Analizar el rango dinámico de la señal.\

El codigo que utilizamos para poder crear este Histograma fue:

```python
plt.hist(MliiSignal,bins=35)
plt.title("Histograma de variación MLII")
plt.xlabel("Amplitud en (mV)")
plt.ylabel("Frecuencia de aparición")
plt.grid(True)
```

<img width="725" height="567" alt="image" src="https://github.com/user-attachments/assets/f25747d8-9096-440c-898c-5f112ab7e5ab" />\
Figura 5. Histograma de variacion

### **Funcion de probabilidad**

Esta funcion de probabilidad describe como se distribuye los valores de una variable continua, indicando la probabilidad relativa de que un valor de la señal se encuentre en un rango especifico.

Se pudo obtener esta funcion de probabilidad por el siguiente codigo:

```python
plt.hist(MliiSignal, bins=50, density=True, label='Histograma normalizado')
plt.title('Estimación de la PDF con histograma')
plt.xlabel('Valor de la señal')
plt.ylabel('Densidad')
plt.legend()
plt.grid()
plt.show()
```

<img width="693" height="569" alt="image" src="https://github.com/user-attachments/assets/272a36ef-0fb6-420d-ac53-6c863789267f" />\
Figura 6. Estimacion de la PDF mediante histograma

### **Courtis**

Es una medida estadistica que indica el grado de concentracion de los valores de una distribucion en la media.\
En este calculo se utilizo la formula de courtis excesiva:\
<img width="408" height="145" alt="image" src="https://github.com/user-attachments/assets/8c1a61b4-0ebb-4a7e-84fa-cbd847eda662" /> \
Figura 7. Formula de courtis excesiva\
Donde:
+ X_i Valores de la señal
+ X Media
+ s Desviacion estandar
+ N Numero total de muestras

Este valor se puede interpretar como:
+ g>0 Distribucion leptocutica
+ g=0 Distrubucion normal
+ g<0 Distribucion platicurtica

 Para poder lograr este valor utilizamos el siguiente codigo:
 ```python
acumulador = 0

for i in MliiSignal:
  acumulador = acumulador + (i - media)**4

g2= acumulador/(nSamples*sd**4)-3
print("Curtosis:",g2)
print("Leptocúrtica")
```
El valor de curtosis fue: 26.565687328943497, indicando una distribucion leptocurtica, lo que nos dice que la señal tiene un pico central muy pronunciado.



