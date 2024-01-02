# views.py
import os
import datetime
import base64
from PIL import Image
from io import BytesIO
from mimetypes import guess_extension
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .forms import ImageUploadForm
import json
from members.utils.face_recognition_utils import load_model, recognize_faces
from firebase_admin import credentials, initialize_app, storage
import firebase_admin
from dotenv import load_dotenv
load_dotenv()

@csrf_exempt
@require_POST
def upload_image(request):
    # Decode base64 and save the image
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")
    try:
        data = json.loads(request.body.decode("utf-8"))
        decoded_image = base64.b64decode(data['image_data'])
        # Create a BytesIO object from the decoded image data
        image_file = BytesIO(decoded_image)
        im = Image.open(image_file)
        im.save('result.jpg')
        model_path = './members/model/svm_model.pkl'
        image_path = './result.jpg'
        model = load_model(model_path)
        result = recognize_faces(image_path, model)
        config = {
            "type": os.getenv("type"),
            "project_id": os.getenv("project_id"),
            "private_key_id": os.getenv("private_key_id"),
            "private_key": os.getenv("private_key").replace(r'\n', '\n'),
            "client_email": os.getenv("client_email"),
            "client_id": os.getenv("client_id"),
            "auth_uri": os.getenv("auth_uri"),
            "token_uri": os.getenv("token_uri"),
            "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
            "client_x509_cert_url": os.getenv("client_x509_cert_url"),
            "universe_domain": os.getenv("universe_domain"),
        }
        if not firebase_admin._apps:
          cred = credentials.Certificate(config) 
          initialize_app(cred, {'storageBucket': 'computer-vision-71389.appspot.com'})

        fileImageName = f'images/{current_datetime}_detected_faces_image.jpg'
        fileCSVName = f'csv/{current_datetime}_detected_faces.csv'
        bucketImage = storage.bucket()
        blobImage = bucketImage.blob(fileImageName)
        blobImage.upload_from_filename("./results/detected_faces_image.jpg")
        blobImage.make_public()

        bucketCSV = storage.bucket()
        blobCSV = bucketCSV.blob(fileCSVName)
        blobCSV.upload_from_filename("./results/detected_faces.csv")
        blobCSV.make_public()
        return JsonResponse({'message': 'Image uploaded successfully', 'result': result, 'image_url': blobImage.public_url, 'csv_url': blobCSV.public_url})
        # form = ImageUploadForm({}, {'image': image_file})
        # print("checkpoint 2")
        # if form.is_valid():
        #     print("valid")
        #     form.save()
        #     return JsonResponse({'status': 'success'})
        # else:
        #     print("invalid")
        #     print(form.errors)
        #     return JsonResponse({'status': 'error', 'message': 'Invalid form data'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)})


@csrf_exempt
@require_GET
def test_server(request):
    # data = json.loads(request.body.decode('utf-8'))
    # name = data.get('name')
    print(request.GET.get("name"))
    return JsonResponse({'status': 'success', 'message': 'Server is running'})

from django.http import JsonResponse
from django.shortcuts import render

def custom_404_view(request, exception):
    return JsonResponse({"error": "Path not found"}, status=404)
