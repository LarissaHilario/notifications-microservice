from service_notification import sns_client
import time
from notifications.infrastructure.constants.message_templates import WELCOME_EMAIL, FEEDBACK_REQUEST_EMAIL

def enviar_correo(topic_arn, email, mensaje, asunto):
    # Suscribirse al correo
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="email",
        Endpoint=email,
        ReturnSubscriptionArn=True
    )

    subscription_arn = response['SubscriptionArn']
    print(f"Suscripción creada: {subscription_arn}")

    time.sleep(50)  # Espera para asegurarse de que la suscripción esté confirmada

    # Publicar el mensaje
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=mensaje,
        Subject=asunto
    )

    print(f"Mensaje publicado: {response}")

    # Comentado para no eliminar la suscripción inmediatamente después de enviar el mensaje
    # sns_client.unsubscribe(
    #     SubscriptionArn=subscription_arn
    # )

    #print(f"Suscripción eliminada: {subscription_arn}")

def formatear_mensaje(plantilla, customer_name, support_email, support_phone):
    return plantilla.format(customer_name=customer_name, support_email=support_email, support_phone=support_phone)

if __name__ == "__main__":
    topic_arn = "arn:aws:sns:us-east-2:471112887179:Notifications"
    email = "kristellperez34@gmail.com"
    customer_name = "Kristell Perez"
    support_email = "support@90minutos.com"
    support_phone = "123-456-7890"
    
    mensaje_bienvenida = formatear_mensaje(WELCOME_EMAIL, customer_name, support_email, support_phone)
    mensaje_feedback = formatear_mensaje(FEEDBACK_REQUEST_EMAIL, customer_name, support_email, support_phone)
    
    asunto_bienvenida = "Bienvenido a 90-Minutos"
    asunto_feedback = "Cuéntanos tu experiencia con 90-Minutos"

    # Enviar correo de bienvenida
    enviar_correo(topic_arn, email, mensaje_bienvenida, asunto_bienvenida)

    # Enviar el mensaje de feedback 
    # enviar_correo(topic_arn, email, mensaje_feedback, asunto_feedback)
