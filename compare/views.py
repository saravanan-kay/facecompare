# compare/views.py
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .utils import verify_with_deepface, verify_with_face_recognition

def compare_page(request):
    return render(request, 'compare.html')

def api_compare(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    img1 = request.FILES.get('image1')
    img2 = request.FILES.get('image2')
    if not img1 or not img2:
        return JsonResponse({'error': 'both files required'}, status=400)

    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    name1 = fs.save(img1.name, img1)
    name2 = fs.save(img2.name, img2)
    path1 = fs.path(name1)
    path2 = fs.path(name2)

    try:
        # Choose verification method:
        # primary = DeepFace
        result = verify_with_deepface(path1, path2, model_name='ArcFace', enforce_detection=True)

        # If DeepFace failed due to no face detection, try a fallback to less strict:
        if result.get('error') and 'face' in result['error'].lower():
            # try again with enforce_detection False
            result = verify_with_deepface(path1, path2, model_name='ArcFace', enforce_detection=False)

        # If deepface totally failed, fallback to face_recognition if installed
        if result.get('error'):
            try:
                fallback = verify_with_face_recognition(path1, path2, tolerance=0.6)
                result['fallback'] = fallback
            except Exception as e:
                result['fallback_error'] = str(e)

        # Attach URLs so frontend can show images
        result['image1_url'] = fs.url(name1)
        result['image2_url'] = fs.url(name2)

        return JsonResponse(result)
    finally:
        # delete temporary files (optional)
        try:
            os.remove(path1)
            os.remove(path2)
        except Exception:
            pass
