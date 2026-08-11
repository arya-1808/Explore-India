from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Chat
from .ai import get_ai_response

import json


@login_required
def chat_page(request):
    return render(
        request,
        'admin/manage_chat.html'
    )


@csrf_exempt
def send_message(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            user_id = data.get("user_id")
            message = data.get("message")

            if not user_id or not message:
                return JsonResponse({
                    "status": "error",
                    "message": "User ID and message are required"
                }, status=400)

            # Get user
            user = User.objects.get(
                id=user_id
            )

            # Get AI response
            ai_reply = get_ai_response(message)

            # Save chat
            chat = Chat.objects.create(
                user=user,
                message=message,
                ai_reply=ai_reply,
                status="Answered"
            )

            return JsonResponse({
                "status": "success",
                "user_message": chat.message,
                "ai_reply": chat.ai_reply
            })

        except User.DoesNotExist:

            return JsonResponse({
                "status": "error",
                "message": "User not found"
            }, status=404)

        except json.JSONDecodeError:

            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON"
            }, status=400)

        except Exception as e:

            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "status": "error",
        "message": "POST request required"
    }, status=405)