import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import random

nombrearchivo ="ECG/27"

record = wfdb.rdrecord(nombrearchivo)
signal = record.p_signal[:,0]  
fs = record.fs  
numerodatos = len(signal) 
limitartiempo=int(10*fs)

time = [i / fs for i in range(numerodatos)]  
signal = signal[:limitartiempo]
time = time[:limitartiempo]

#DIBUJAR SEÑAL
plt.figure(figsize=(12,4))
plt.plot(time, signal, color="orange")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal Biomédica ECG bases de datos physionet")
plt.legend()
plt.grid()
plt.show()

#DIBUJAR HISTOGRAMA
plt.figure(figsize=(8, 4))
plt.hist(signal, bins=50, color='orange', alpha=0.7, edgecolor='black', density=True)
plt.xlabel("Amplitud de la señal")
plt.ylabel("Frecuencia normalizada")
plt.title("Histograma de la señal (10s)")
plt.grid()
plt.show()

suma = 0
for i in range(len(signal)):
    suma += signal[i]
media = suma /len(signal)
print(f"la media de la señal es: {media:.3f}")

#VECTOR DE LOGITUD
vector=0
for _ in signal:
    vector += 1
print(f"la longitud del vector es: {vector}")

#DESVIACION ESTANDAR
desviacion=0
for i in range(len(signal)):
    desviacion += (signal[i] - media) ** 2
desviacion_estandar = (desviacion/len(signal))**0.5
print (f"la desviacion estandar es: {desviacion_estandar:.3f}")

#COEFICIENTE DE VARIACION
coeficiente = desviacion_estandar/media if media !=0 else float ("nan")
print (f"El coeficiente es: {coeficiente:.3f}")

#CAMPANA DE GAUSS
gaus = gaussian_kde(signal)
fx = np.linspace(min(signal), max(signal), 1000)
val = gaus (fx)
plt.figure(figsize=(10,5))
plt.plot (fx, val, color="red", label="")
plt.xlabel("Amplitud de la señal")
plt.ylabel("Densidad de la probabilidad")
plt.title("Funcion gausiana de probabilidad de 20s")
plt.grid()
plt.show()

def potencia(signal2):
    cuadrados = 0
    for i in range (len(signal2)):
        cuadrados += signal2[i] ** 2
    return cuadrados/len(signal2)

ruido_gauss = [random.gauss(0,0.1)for _ in range(len(signal))]
gauss_signal = [signal[i]+ ruido_gauss[i] for i in range(len(signal))]

plt.figure(figsize=(12,4))
plt.plot(time, gauss_signal, color="violet")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal con ruido de gauss")
plt.legend()
plt.grid()
plt.show()


ruido_impulso = [random.uniform(-1,1) if random.random() < 0.05 else 0 for _ in range (len(signal))]
impulso_signal = [signal [i] + ruido_impulso[i] for i in range (len(signal))]

plt.figure(figsize=(12,4))
plt.plot(time, impulso_signal, color="blue")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal con ruido de impulso")
plt.legend()
plt.grid()
plt.show()

ruido_artefacto = signal[:]
for _ in range (10):
    j = random.randint(0, len(signal)-1)
    ruido_artefacto[j] += random.uniform(-2,2)
artefacto_signal = ruido_artefacto

plt.figure(figsize=(12,4))
plt.plot(time, artefacto_signal, color="black")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal con ruido de artefacto")
plt.legend()
plt.grid()
plt.show()

cal_potencia = potencia(signal)
pot_gauss = potencia(ruido_gauss)
pot_impulso = potencia(ruido_impulso)
pot_artefacto = potencia([artefacto_signal[i] - signal[i] for i in range(len(signal))])

SNR_gauss = 10 * (cal_potencia / pot_gauss)
SNR_impulso = 10 * (cal_potencia / pot_impulso)
SNR_artefacto = 10 * (cal_potencia / pot_artefacto)

print(f"SNR Gauss: {SNR_gauss:.3f}")
print(f"SNR Impulso: {SNR_impulso:.3f}")
print(f"SNR Artefacto: {SNR_artefacto:.3f}")

plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(signal, label="Señal Original", color="black")
plt.title("Señal Original")
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(gauss_signal, label="Ruido Gaussiano", color="red")
plt.title("Señal con Ruido Gaussiano")
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(impulso_signal, label="Ruido Impulsivo", color="blue")
plt.title("Señal con Ruido Impulsivo")
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(artefacto_signal, label="Ruido de Artefacto", color="green")
plt.title("Señal con Ruido de Artefacto")
plt.legend()

plt.tight_layout()
plt.show()

