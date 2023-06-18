from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def indexView(request):
    return render(request,'index.html')
@login_required()

def dashboardView(request):
    return render(request,'index2.html')

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form':form})

import base64
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from PIL import Image
from io import BytesIO
from tensorflow.keras.preprocessing.image import img_to_array

@csrf_exempt
def predict(request):
    print('BEFORE POST')
    if request.method == 'POST':
        
        try:
            # Retrieve the base64-encoded image from the request
            data = request.POST.get('image')
            print('AFTER POST')
            # Convert the base64-encoded image to a PIL Image object
            image = Image.open(BytesIO(base64.b64decode(data)))

            # Preprocess the image (resize, normalize, etc.)
            image = image.resize((64, 64))  # Resize the image to match the target_size
            image = img_to_array(image)  # Convert PIL Image to numpy array
            image = image / 255.0  # Normalize the pixel values

            # Load the pre-trained model
            model = load_model('E:\Django2\histopath cancer detecion django\2265histopath_model.h5')

            # Convert the image to a numpy array
            image_array = np.array([image])

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
