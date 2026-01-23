import os
import smtplib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import logging
logging.basicConfig(level=logging.DEBUG)


# Gemini SDK
from google import genai
from google.genai import types

# Initialize client with API key
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@api_view(['POST'])
def generate_email(request):
    """
    Expected JSON:
    {
      "recipient_name": "Alice",
      "purpose": "Follow up about meeting",
      "details": "We discussed partnership and next steps...",
      "tone": "friendly"   # optional, default "professional"
    }
    """
    data = request.data
    recipient = data.get("recipient_name", "")
    purpose = data.get("purpose", "")
    details = data.get("details", "")
    tone = data.get("tone", "professional")
    sender_name = "Smith"

    if not purpose and not details:
        return Response({"error": "Provide purpose or details"}, status=status.HTTP_400_BAD_REQUEST)

 
    """
    Generates an email draft using the Gemini API based on a given prompt.
    """
    full_prompt = f"""
    Write a {tone} email from {sender_name} to {recipient}.
    The core message is: "{details}"
    The output should be a complete email draft including a subject line,
    salutation, body, and closing.
    """

    try:

        response = client.models.generate_content(
            model='gemini-2.5-flash', # A fast and capable model
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                temperature=0.7, # Adjust creativity
            ),
        )
        return Response({"email": response.text})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def send_email(request):

    data = request.data
    recipient = data.get("recipient_name", "")
    subject = data.get("subject", "")
    email = data.get("email", "")

    if not recipient or not subject or not email:
        return Response({"error": "Provide recipient, subject, and email"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        
        send_mail(
            subject=subject,
            message=email,
            from_email="muddasirmd2@gmail.com",
            recipient_list=[recipient],
            fail_silently=False,
        )
        return Response({"message": "Email sent successfully."})
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
