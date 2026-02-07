import os
import smtplib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, EmailMessage
import os
from pathlib import Path


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
      "subject": "Follow up about meeting",
      "details": "We discussed partnership and next steps...",
      "tone": "friendly"   # optional, default "professional"
    }
    """
    data = request.data
    recipient = data.get("recipient_email", "")
    subject = data.get("subject", "")
    details = data.get("details", "")
    company = data.get("company", "")
    heard_from = data.get("heard_from", "")
    tone = "professional"
    
    sender_name = "Muddasir Nisar"


    if not subject and not details:
        return Response({"error": "Provide subject or details"}, status=status.HTTP_400_BAD_REQUEST)

 
    """
        Generates an email using the Gemini API based on a given prompt.
    """
    full_prompt = f"""
    Write a ready to send cover letter in a {tone} tone from {sender_name} to {recipient} for the job {subject} { 'at ' + company if company else ''}. {'I heard about this job from ' + heard_from + '.' if heard_from else ''}
    The core message is: "{details}"
    The output should be a complete email including salutation, body, and closing. 
    Also add this "you can find more details in attached resume". Exclude subject line
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
    # recipient = data.get("recipient_email", "")
    recipient = "muddasirmd2@gmail.com"
    subject = data.get("subject", "")
    body = data.get("email", "")

    if not recipient or not subject or not body:
        return Response({"error": "Provide recipient, subject, and email"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        
        # send_mail(
        #     subject=subject,
        #     message=body,
        #     from_email="mnisar@teresol.com",
        #     recipient_list=[recipient],
        #     fail_silently=False,
        # )

        from_email= os.getenv("FROM_EMAIL")
        
        to_email=[recipient]

        email = EmailMessage(
            subject,
            body,
            from_email,
            to_email
        )

        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = BASE_DIR / 'media' / 'test.pdf'

        # /app/job_applier/media/test.pdf
        email.attach_file(str(file_path))
        email.send()

        return Response({"message": "Email sent successfully."})
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
