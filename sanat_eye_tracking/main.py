import cv2
import mediapipe as mp
import numpy as np
import time

# Kamera erişimi
cam = cv2.VideoCapture(0)  # Web kamerasından görüntü al
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Video dosyası
video_file = "video.mp4"
video = cv2.VideoCapture(video_file)
# Kamera çözünürlüğünü al
_, frame = cam.read()
frame_h, frame_w, _ = frame.shape

# Blur efekti için kernel boyutu
blur_kernel_size = (101, 101)

def get_eye_center(landmarks, indices, frame_w, frame_h):
    x = sum([landmarks[i].x for i in indices]) / len(indices) * frame_w
    y = sum([landmarks[i].y for i in indices]) / len(indices) * frame_h
    z = sum([landmarks[i].z for i in indices]) / len(indices)  # Z değeri normalize edilmiştir
    return int(x), int(y), z

def calculate_angle(x1, y1, x2, y2):
    # Vektörü oluştur
    dx = x2 - x1
    dy = y2 - y1
    
    # Eğimi hesapla
    angle = np.arctan2(dy, dx) * 180 / np.pi
    return angle

start_time = None  # Resmin gösterilmeye başlandığı zamanı saklar
blur_delay = 0.8  # Resmin bakmayı kestikten sonra kaç saniye net kalacağını belirler
show_image_clear = False  # Resmin net olup olmadığını belirler
cv2.namedWindow('Blurred Video')

while True:
    # Web kamerasından görüntü al
    _, frame_webcam = cam.read()
    frame_webcam = cv2.flip(frame_webcam, 1)
    rgb_frame_webcam = cv2.cvtColor(frame_webcam, cv2.COLOR_BGR2RGB)

    # Video dosyasından görüntü al
    ret, frame_video = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Video sona erdiğinde başa dön
        _, frame_video = video.read()
    
    # Web kamerası karesinde yüz tespit et
    output_webcam = face_mesh.process(rgb_frame_webcam)
    landmark_points_webcam = output_webcam.multi_face_landmarks
    
    # Yüz tespiti varsa işlem yap
    if landmark_points_webcam:
        landmarks_webcam = landmark_points_webcam[0].landmark
        
        # Sağ ve sol göz merkezlerini al
        right_eye_center_x, right_eye_center_y, right_eye_center_z = get_eye_center(landmarks_webcam, range(474, 478), frame_w, frame_h)
        cv2.circle(frame_webcam, (right_eye_center_x, right_eye_center_y), 5, (0, 255, 0), -1)
        
        left_eye_center_x, left_eye_center_y, left_eye_center_z = get_eye_center(landmarks_webcam, range(469, 473), frame_w, frame_h)
        cv2.circle(frame_webcam, (left_eye_center_x, left_eye_center_y), 5, (255, 0, 0), -1)
        
        # Sağ ve sol gözlerin bakış açılarını hesapla
        right_eye_direction_x = right_eye_center_x - int(100 * right_eye_center_z)
        right_eye_direction_y = right_eye_center_y - int(100 * right_eye_center_z)
        cv2.line(frame_webcam, (right_eye_center_x, right_eye_center_y), (right_eye_direction_x, right_eye_direction_y), (0, 255, 0), 2)
        
        left_eye_direction_x = left_eye_center_x - int(100 * left_eye_center_z)
        left_eye_direction_y = left_eye_center_y - int(100 * left_eye_center_z)
        cv2.line(frame_webcam, (left_eye_center_x, left_eye_center_y), (left_eye_direction_x, left_eye_direction_y), (255, 0, 0), 2)

        # Daire merkezi ve yarıçapı
        circle_center = (frame_w // 2, frame_h // 2)
        circle_radius = 100
        cv2.circle(frame_webcam, circle_center, circle_radius, (0, 255, 255), 2)

        # Sağ ve sol gözlerin bakış açılarını kontrol et
        right_eye_angle = calculate_angle(right_eye_center_x, right_eye_center_y, right_eye_direction_x, right_eye_direction_y)
        left_eye_angle = calculate_angle(left_eye_center_x, left_eye_center_y, left_eye_direction_x, left_eye_direction_y)
        
        # Gözlerin daire içinde ve belirli bir açı aralığında olup olmadığını kontrol et
        if np.linalg.norm(np.array([right_eye_center_x, right_eye_center_y]) - np.array(circle_center)) < circle_radius \
                and np.linalg.norm(np.array([left_eye_center_x, left_eye_center_y]) - np.array(circle_center)) < circle_radius \
                and abs(right_eye_angle) <= 45 \
                and abs(left_eye_angle) <= 45:
            cv2.putText(frame_webcam, "Inside", (circle_center[0] - 30, circle_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if start_time is None:
                start_time = time.time()
            show_image_clear = True  # Resmi net göster
        else:
            if show_image_clear:
                start_time = time.time()
            show_image_clear = False  # Resmi bulanık göster

    # Resmi belirli bir süre boyunca göster
    if show_image_clear or (start_time is not None and (time.time() - start_time) < blur_delay):
        blurred_frame_video = frame_video.copy()
    else:
        # Video karesine blur efekti uygula
        blurred_frame_video = cv2.GaussianBlur(frame_video, blur_kernel_size, 0)

    # Web kameradan alınan görüntüyü ekranda göster
    cv2.imshow("Webcam Face Mesh", frame_webcam)
    cv2.imshow("Blurred Video", blurred_frame_video)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
video.release()
cv2.destroyAllWindows()
