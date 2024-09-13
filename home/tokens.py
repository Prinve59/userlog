from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class Tokengenerator(PasswordResetTokenGenerator):
    def hash(self,user,timestamp):
        return(
            text_type(user.pk)+text_type(timestamp)
        )

generate_token=Tokengenerator()