# compare/utils.py
import os

# Option A: DeepFace (recommended)
def verify_with_deepface(img1_path, img2_path, model_name='ArcFace', enforce_detection=True):
    from deepface import DeepFace
    try:
        result = DeepFace.verify(img1_path, img2_path,
                                 model_name=model_name,
                                 enforce_detection=enforce_detection)
        # result often contains 'verified' (bool) and 'distance' (float)
        return {
            'method': 'deepface',
            'verified': bool(result.get('verified', False)),
            'details': result
        }
    except Exception as e:
        return {'method': 'deepface', 'error': str(e)}

# Option B: face_recognition (dlib)
def verify_with_face_recognition(img1_path, img2_path, tolerance=0.6):
    import face_recognition
    try:
        img1 = face_recognition.load_image_file(img1_path)
        img2 = face_recognition.load_image_file(img2_path)

        enc1 = face_recognition.face_encodings(img1)
        enc2 = face_recognition.face_encodings(img2)

        if len(enc1) == 0 or len(enc2) == 0:
            return {'method': 'face_recognition', 'error': 'no_face_found_in_image'}

        match = face_recognition.compare_faces([enc1[0]], enc2[0], tolerance=tolerance)[0]
        # you can also compute distance:
        from face_recognition.api import face_distance
        dist = face_distance([enc1[0]], enc2[0])[0]
        return {
            'method': 'face_recognition',
            'verified': bool(match),
            'distance': float(dist),
            'tolerance': tolerance
        }
    except Exception as e:
        return {'method': 'face_recognition', 'error': str(e)}
