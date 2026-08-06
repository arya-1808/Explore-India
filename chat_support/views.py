from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Chat
from .ai import get_ai_response
import json


@csrf_exempt
def send_message(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user_id = data.get("user_id")
        message = data.get("message")

        user = User.objects.get(id=user_id)

        # Get AI Response
        ai_reply = get_ai_response(message)

        # Save chat
        chat = Chat.objects.create(
            user=user,
            message=message,
            reply=ai_reply
        )

        return JsonResponse({
            "status": "success",
            "user_message": chat.message,
            "ai_reply": chat.reply
        })

    return JsonResponse({
        "status": "error",
        "message": "POST request required"
    })