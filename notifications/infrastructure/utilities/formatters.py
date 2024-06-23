def formatter_message(plantilla, customer_name, support_email, support_phone):
    return plantilla.format(customer_name=customer_name, support_email=support_email, support_phone=support_phone)
