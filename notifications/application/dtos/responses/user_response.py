class UserResponse:
    def __init__(self):
        self.user_info = {}

    def set_email(self, email):
        self.user_info['email'] = email

    def get_email(self):
        return self.user_info['email']

    def set_name(self, name):
        self.user_info['name'] = name

    def get_name(self):
        return self.user_info['name']
