import json
import os

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Conversation, ChatMessage

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


@login_required
def home(request):

    conversations = Conversation.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "index.html", {
        "conversations": conversations
    })


@login_required
def create_conversation(request):

    convo = Conversation.objects.create(user=request.user)

    return JsonResponse({"id": convo.id})


@csrf_exempt
@login_required
def ask_ai(request):

    data = json.loads(request.body)

    message = data.get("message")
    convo_id = data.get("conversation_id")

    conversation = get_object_or_404(Conversation, id=convo_id, user=request.user)

    # Save user message
    user_msg = ChatMessage.objects.create(
        conversation=conversation,
        role="user",
        message=message
    )

    try:
        response = model.generate_content(message)
        reply = response.text
    except Exception as e:
        reply = str(e)

    # Save bot message
    ChatMessage.objects.create(
        conversation=conversation,
        role="assistant",
        message=reply
    )

    # Auto title
    if not conversation.title:
        conversation.title = message[:40]
        conversation.save()

    return JsonResponse({
        "reply": reply,
        "msg_id": user_msg.id
    })


@login_required
def load_messages(request, convo_id):

    conversation = get_object_or_404(Conversation, id=convo_id, user=request.user)

    messages = conversation.messages.order_by("created_at")

    data = []

    for m in messages:
        data.append({
            "id": m.id,
            "role": m.role,
            "message": m.message
        })

    return JsonResponse(data, safe=False)


@login_required
def delete_conversation(request, convo_id):

    convo = get_object_or_404(Conversation, id=convo_id, user=request.user)
    convo.delete()

    return JsonResponse({"status": "deleted"})


@csrf_exempt
@login_required
def edit_message(request, msg_id):

    data = json.loads(request.body)
    new_text = data.get("message")

    msg = get_object_or_404(ChatMessage, id=msg_id, conversation__user=request.user)

    msg.message = new_text
    msg.edited = True
    msg.save()

    return JsonResponse({"status": "updated"})