import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

API_KEY = "YOUR_HUGGINGFACE_API_KEY"

def home(request):
    return render(request, "index.html")


@csrf_exempt
def ask_ai(request):

    if request.method == "POST":

        data = json.loads(request.body)
        message = data.get("message")

        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        payload = {
            "inputs": message
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        result = response.json()

        reply = result[0]["generated_text"]

        return JsonResponse({"reply": reply})
