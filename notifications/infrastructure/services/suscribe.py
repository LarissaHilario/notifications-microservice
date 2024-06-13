from service_notification import sns_client

response = sns_client.subscribe(
    TopicArn = "arn:aws:sns:us-east-2:471112887179:Notifications",
    Protocol = "email",
    #Prueba
    Endpoint = "213476@ids.upchiapas.edu.mx",
    ReturnSubscriptionArn = True

)

print(response)

