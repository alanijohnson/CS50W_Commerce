from django.contrib.auth.base_user import BaseUserManager

# manager for the Custom User class
class UserManager(BaseUserManager):
    # Custum user model manager where additional fields are supplied.
    # username remains the same authentication method
    
    def create_user(self,username, password, email, **extra_fields):
        if not email:
            raise ValueError('The email must be set.')
        if not password:
            raise ValueError('Users must have password')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username, password, email, **extra_fields):
        user = self.create_user(username, password, email, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user

