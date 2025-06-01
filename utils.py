import numpy as np
import math

def calcular_angulo(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    angulo = np.arccos(np.clip(np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc)), -1.0, 1.0))
    return np.degrees(angulo)

def angulo_entre(p1, centro, p2):
    def angulo_vetor(v):
        return math.degrees(math.atan2(v[1], v[0]))
    v1 = np.array(p1) - np.array(centro)
    v2 = np.array(p2) - np.array(centro)
    angulo1 = angulo_vetor(v1)
    angulo2 = angulo_vetor(v2)
    angulo_inicio = angulo1 % 360
    angulo_varredura = (angulo2 - angulo1) % 360
    return angulo_inicio, angulo_varredura