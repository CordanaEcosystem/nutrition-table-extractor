
from detection import detect_all
import base64
import io
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ingredient_extractor.vision import extract_ingredients_from_image

from .allergies import check_allergies,get_top_three,Dv_values
from .models import *
from .forms import UploadFileForm
import cv2
import json
import sys
import os
import csv
from PIL import Image
import random



sys.path.append(os.path.join(os.getcwd(), 'nutrition_extractor'))
sys.path.append(os.path.join(os.getcwd(), 'nutrition_extractor/data'))


@csrf_exempt
def nutritionExtract(request):
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({"error": "No 'image' file provided."}, status=400)

            new_file = UploadFile(file=request.FILES['image'])
            new_file.save()
            file_path = new_file.file.path
            name = new_file.file.name
            response = detect_all(name, False)
            os.remove(file_path)
            new_file.delete()


            return JsonResponse(response)

        except FileNotFoundError as e:
            return JsonResponse({"error": f"FileNotFoundError: {e}"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def health(request):
    
        try:
            response={"status":"ok"}

            return JsonResponse(response)

        except FileNotFoundError as e:
            return JsonResponse({"error": f"FileNotFoundError: {e}"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



