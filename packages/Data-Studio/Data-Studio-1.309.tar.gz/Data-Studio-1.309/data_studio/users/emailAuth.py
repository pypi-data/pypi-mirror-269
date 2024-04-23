from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            # Directly use the built-in check_password method
            if user.check_password(password):
                # Optional: Log successful password check or perform extra actions
                print("Password check succeeded for user:", username)
                return user
            else:
                # Optional: Log failed password check or perform extra actions
                print("Password check failed for user:", username)
                return None
        except UserModel.DoesNotExist:
            # Optional: Log the case when a user is not found
            print("User not found:", username)
            return None
