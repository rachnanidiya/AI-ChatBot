import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai


# add your API key here
genai.configure(api_key="AIzaSyBZK0jlkTbGEsQJm53HkoQUMlZWQK7KSVI")

model = genai.GenerativeModel("gemini-2.5-flash")


def home(request):
    return render(request, "index.html")


@csrf_exempt
def ask_ai(request):

    if request.method == "POST":

        data = json.loads(request.body)
        message = data.get("message")

        try:
            response = model.generate_content(message)
            reply = response.text

        except Exception as e:
            reply = str(e)

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid request"})