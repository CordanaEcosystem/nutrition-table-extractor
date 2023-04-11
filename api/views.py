import base64
import io
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ingredient_extractor.vision import extract_ingredients_from_image
from .models import *
from .forms import UploadFileForm
import cv2
import json
import sys
import os
from PIL import Image
sys.path.append(os.path.join(os.getcwd(), 'nutrition_extractor'))
sys.path.append(os.path.join(os.getcwd(), 'nutrition_extractor/data'))
from detection import detect_all
@csrf_exempt

def nutritionExtract(request):
	if request.method == 'POST':
		new_file = UploadFile(file = request.FILES['image'])
		new_file.save()
		name = new_file.file.name
		response = detect_all(name, False)
		os.remove(file_path)
		file_path=new_file.file.path
		
		return JsonResponse(response)
@csrf_exempt	
def ingredientExtract(request):
	if request.method == 'POST':
		new_file = UploadFile(file = request.FILES['image'])
		new_file.save()
		# Delete the file from the server
       
		# extract_ingredients_from_image(request.FILES['image'])
		name = new_file.file.name
		file_path=new_file.file.path
		with io.open(file_path, 'rb') as img:
            
		
			file_data =img.read()
			file_base64 = base64.b64encode(file_data).decode('utf-8')
			
            # Convert the file to base64
           
            
		
        
			response = extract_ingredients_from_image(file_base64)
			dict={"ingredients":response}
			
			os.remove(file_path)
		
			return JsonResponse(dict)

