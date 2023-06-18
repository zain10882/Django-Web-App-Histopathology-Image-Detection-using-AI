
import base64
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from PIL import Image
from io import BytesIO


from tensorflow.keras.utils import img_to_array 
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def dashboard(request):
    return render(request, 'index2.html')



@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            # Retrieve the base64-encoded image from the request
            data = request.POST.get('image')
            print('Base64-encoded string:', data)

            if data is None:
                return JsonResponse({'error': 'Invalid base64-encoded string'})


            #Pad the base64-encoded string if necessary
            padding = len(data) % 4
            if padding > 0:
                data += '=' * (4 - padding)

            print('Padded base64-encoded string:', data)

            # Convert the base64-encoded image to a PIL Image object
            image = Image.open(BytesIO(base64.urlsafe_b64decode(data)))
            # image = Image.open(BytesIO(base64.b64decode(data)))

            # Preprocess the image (resize, normalize, etc.)
            image = image.resize((64, 64))  # Resize the image to match the target_size
            image = img_to_array(image)  # Convert PIL Image to numpy array
            image = image / 255.0  # Normalize the pixel values

            # Load the pre-trained model
            model = load_model('E:\Django2\histopath cancer detecion django\2265histopath_model.h5')

            # Convert the image to a numpy array
            image_array = np.array([image])
            image_array = print()

            # Make a prediction using the model
            prediction = model.predict(image_array)[0]

            # Determine the predicted class
            if prediction < 0.5:
                output = 'benign'
            else:
                output = 'malignant'

            # Return the prediction result as JSON response
            return JsonResponse({'result': output})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})