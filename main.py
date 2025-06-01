import cv2
import numpy as np
import mediapipe as mp
from utils import angulo_entre, calcular_angulo

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
video = cv2.VideoCapture("./video.mp4")

contador_frames = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = pose.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if resultados.pose_landmarks:
        altura, largura, _ = frame.shape
        marcadores = resultados.pose_landmarks.landmark

        quadril = [marcadores[23].x * largura, marcadores[23].y * altura]
        joelho = [marcadores[25].x * largura, marcadores[25].y * altura]
        tornozelo = [marcadores[27].x * largura, marcadores[27].y * altura]

        if not quadril or not joelho or not tornozelo:
            continue

        # referência horizontal na altura do joelho
        pnt_ref_horizontal = [joelho[0] - 100, joelho[1]]

        # pnt de referência vertical (abaixo do quadril, mesma distância até o tornozelo)
        pnt_ref_vertical = [quadril[0], quadril[1] + 100]

        # Calcula ângulo da perna com a vertical
        angulo_perna = calcular_angulo(pnt_ref_vertical, joelho, tornozelo)
        inicio_perna, varredura_perna = angulo_entre(pnt_ref_vertical, joelho, tornozelo)

        # Calcula ângulo de referência com a linha horizontal
        angulo_referencia = calcular_angulo(pnt_ref_vertical, joelho, pnt_ref_horizontal)
        inicio_ref, varredura_ref = angulo_entre(pnt_ref_vertical, joelho, pnt_ref_horizontal)

        centro = tuple(np.int32(joelho))
        eixos = (50, 50)
        
        # ângulo da perna
        cv2.ellipse(frame, centro, eixos, 0, inicio_perna, inicio_perna + varredura_perna, (0, 255, 0), 3)
        # ângulo de referência
        cv2.ellipse(frame, centro, eixos, 0, inicio_ref, inicio_ref + varredura_ref, (255, 0, 0), 2) 

        # graus perna 
        cv2.putText(frame, f'{int(angulo_perna)}°', (centro[0] + 10, centro[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # graus referencia
        cv2.putText(frame, f'{int(angulo_referencia)}°', (centro[0] + 10, centro[1] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    if contador_frames % 5 == 0:
        cv2.imshow("res", frame)

    contador_frames += 1

video.release()
cv2.destroyAllWindows()
