from detection import detect_all
import base64
import io
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ingredient_extractor.vision import extract_ingredients_from_image
from process_product.client import server_client
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
        new_file = UploadFile(file=request.FILES['image'])
        new_file.save()
        file_path = new_file.file.path
        name = new_file.file.name
        response = detect_all(name, True)
        os.remove(file_path)
        file_path = new_file.file.path

        return JsonResponse(response)


@csrf_exempt
def ingredientExtract(request):
    if request.method == 'POST':
        new_file = UploadFile(file=request.FILES['image'])
        new_file.save()
        # Delete the file from the server

        # extract_ingredients_from_image(request.FILES['image'])
        name = new_file.file.name
        file_path = new_file.file.path
        with io.open(file_path, 'rb') as img:

            file_data = img.read()
            file_base64 = base64.b64encode(file_data).decode('utf-8')

            # Convert the file to base64

            response = extract_ingredients_from_image(file_base64)
            dict = {"ingredients": response}

            os.remove(file_path)

            return JsonResponse(dict)


@csrf_exempt
def process_new_product(request):
    if request.method == 'POST':
        csv_filename = "api/Dataset analysis.csv"
        all_nutrients = []
        all_nutrients_mapping = {}
        unit_mapping = {}
        print("===", request)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = body["data"]
        nutrients = {"macros": {}, "vitamins": {}, "minerals": {}}
        with open(csv_filename) as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row["name"].strip().lower()
                all_nutrients.append(name)
                all_nutrients_mapping[name] = {
                    "name": name,
                    "new_name": row["new_name"].strip(),
                    "category": row["category"].strip(),
                    # "new_unit": row["new_unit"],
                }
                unit_mapping[row["new_name"].strip()] = {
                    "category": row["category"].strip(),
                    # "new_unit": row["new_unit"],
                }
        print(all_nutrients_mapping)
        for record in data["nutrients"]:
            result = all_nutrients_mapping.get(
                record["name"].lower())
            print("11",result)
            key = record["name"].strip()

            if result is not None:
                value = record["amount"]

                print("222",value)
                if(record["unitName"].strip()=="%" and Dv_values.get(result["new_name"])):
                    value = Dv_values.get(result["new_name"]).get("amount")*value/100
                    nutrients[result["category"]][result["new_name"]] = {
                            "value": value,
                            "unit":  Dv_values.get(result["new_name"]).get("unit")
                        }
                    # print("<<<<<",Dv_values.get(result["new_name"]).get("unit"))
                else:
                 nutrients[result["category"]][result["new_name"]] = {
                            "value": value,
                            "unit": record["unitName"]
                        }
              
        print("-----", nutrients)
        top_three = get_top_three(
                    nutrients["vitamins"] | nutrients["minerals"])
        # generate a random 6-digit number between 100000 and 999999 (inclusive)
        random_number = random.randint(100000, 999999)

        print("-9|",random_number)
        new_data = {

            "dataType": "Branded",
                        "description": data["description"],
                        "brandOwner": data["brandOwner"],
                        "gtinUpc": data["gtinUpc"],
                        "nutrients": str(json.dumps(nutrients)),
                        "brandName": data["brandName"],
                        "addedBy":data["uid"],

                        "topThree": top_three,
                        "descriptionLength": len(data["description"]),
                        "fdcId":data["uid"]+"-"+str(random_number)
        }
        if "servingSize" in data:
            new_data["servingSize"] = data["servingSize"]
        if "servingSizeUnit" in data:
            new_data["servingSizeUnit"] = data["servingSizeUnit"]
        if "packageWeight" in data:
            new_data["packageWeight"] = data["packageWeight"]
        if "ingredients" in data:
            new_data["allergyInformation"] = check_allergies(data["ingredients"])
            new_data["ingredients"] = data["ingredients"]
        print("===", new_data)
        print(server_client.collections['WaitlistProducts'].documents.create(new_data))

        dict = {"message": "success","data":new_data}
        return JsonResponse(dict)
