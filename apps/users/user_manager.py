from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, phone=None, email=None, password=None, **extra_fields):

        user = self.model(
            phone=phone,
            email=email,
            **extra_fields,
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            phone=phone,
            password=password,
            **extra_fields,
        )
        