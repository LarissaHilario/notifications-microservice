from enum import Enum


class Queue(Enum):
    QUEUE_NEW_USER = {
        "queue": "new_user_notification",
        "exchange": "notification_90_minutes",
        "routing_key": "newuser.notification"
    }
    QUEUE_ARRIVE_PACKAGE = {
        "queue": "arrive_package_notification",
        "exchange": "notification_90_minutes",
        "routing_key": "package.arrive.notification"
    }
    QUEUE_PAYMENT_PACKAGE = {
        "queue": "payment_package_receive_notification",
        "exchange": "notification_90_minutes",
        "routing_key": "package.payment.notification"
    }
    QUEUE_PAYMENT_MEMBER_PACKAGE = {
            "queue": "payment_member_receive_notification",
            "exchange": "notification_90_minutes",
            "routing_key": "payment.member.notification"
    }
    QUEUE_GET_INFO_USER_REQ = {
            "queue": "get_user_info_notification_req",
            "exchange": "notification_90_minutes",
            "routing_key": "get_user_info_req.notification"
    }
    QUEUE_GET_INFO_USER_RES = {
            "queue": "get_user_info_notification_res",
            "exchange": "notification_90_minutes",
            "routing_key": "get_user_info_res.notification"
    }
