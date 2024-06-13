# publish.py

import boto3
from dotenv import load_dotenv
from os import getenv
from notifications.infrastructure.constants.message_templates import WELCOME_EMAIL, FEEDBACK_REQUEST_EMAIL

load_dotenv()

# Cliente de SNS
sns_client = boto3.client("sns", 
                          aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"), 
                          region_name=getenv("AWS_REGION"))

def format_message(template, **kwargs):
    return template.format(**kwargs)

def publish_message(customer_name, support_email, support_phone, message_type):
    topic_arn = "arn:aws:sns:us-east-2:471112887179:Notifications"
    
    if message_type == "welcome":
        template = WELCOME_EMAIL
        subject = "¡Bienvenido a 90-Minutos!"
    elif message_type == "feedback":
        template = FEEDBACK_REQUEST_EMAIL
        subject = "Nos encantaría saber tu opinión"
    else:
        raise ValueError("Tipo de mensaje no soportado")

    message = format_message(
        template,
        customer_name=customer_name,
        support_email=support_email,
        support_phone=support_phone
    )

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        return response
    except Exception as e:
        print(f"Error al publicar el mensaje: {str(e)}")
        return None

if __name__ == "__main__":
    customer_name = "obtener-name"
    support_email = "obtener-email"

    # Publicar mensajes
    response_welcome = publish_message(customer_name, support_email, support_phone, "welcome")
    print("Respuesta de mensaje de bienvenida:", response_welcome)

    response_feedback = publish_message(customer_name, support_email, support_phone, "feedback")
    print("Respuesta de solicitud de feedback:", response_feedback)
