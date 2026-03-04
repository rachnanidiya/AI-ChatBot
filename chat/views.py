import json
import os

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Conversation, ChatMessage

import google.generativeai as genai
from dotenv import load_dotenv


# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def home(request):

    conversations = Conversation.objects.order_by("-created_at")

    return render(request, "index.html", {
        "conversations": conversations
    })


@csrf_exempt
def create_conversation(request):

    convo = Conversation.objects.create(title="New Chat")

    return JsonResponse({
        "id": convo.id
    })


@csrf_exempt
def ask_ai(request):

    data = json.loads(request.body)

    message = data.get("message")
    convo_id = data.get("conversation_id")

    conversation = get_object_or_404(Conversation, id=convo_id)

    # Save user message
    ChatMessage.objects.create(
        conversation=conversation,
        role="user",
        message=message
    )

    try:

        response = model.generate_content(message)

        reply = response.text

    except Exception as e:
        reply = str(e)

    # Save AI reply
    ChatMessage.objects.create(
        conversation=conversation,
        role="assistant",
        message=reply
    )

    # Set title automatically
    if not conversation.title or conversation.title == "New Chat":
        conversation.title = message[:40]
        conversation.save()

    return JsonResponse({
        "reply": reply
    })


def load_messages(request, convo_id):

    conversation = get_object_or_404(Conversation, id=convo_id)

    messages = conversation.messages.order_by("created_at")

    data = []

    for m in messages:
        data.append({
            "role": m.role,
            "message": m.message
        })

    return JsonResponse(data, safe=False)

def create_conversation(request):
    convo = Conversation.objects.create(title="Untitled Chat")
    return JsonResponse({"id": convo.id})