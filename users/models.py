from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models import TextChoices
from phonenumber_field.modelfields import PhoneNumberField


# ----------------------------------------------------------------------------------------------------------------------
# Create custom manager
class UserManager(BaseUserManager):
    """
    Custom user manager
    """

    def create_user(self, email, first_name, last_name, phone, password=None, role='user'):
        """
        Creates and saves a user with the given information

        :param role:
        :param email: The email address
        :param first_name: The first name of the user
        :param last_name: The last name of the user
        :param phone: The phone number of the user
        :param password: The password of the user
        :return: User
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        """
        Creates and saves a superuser with the given information

        :param email: The email address
        :param first_name: The first name of the user
        :param last_name: The last name of the user
        :param phone: The phone number of the user
        :param password: The password of the user
        :return: User
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role='admin'
        )

        user.save(using=self._db)
        return user


# ----------------------------------------------------------------------------------------------------------------------
# Create user model
class User(AbstractBaseUser):
    """
    Custom user model
    """

    class Roles(TextChoices):
        """
        Enumeration of user roles
        """
        ADMIN = 'admin', 'Администратор'
        USER = 'user', 'Пользователь'

    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='avatars/', null=True)
    is_active = models.BooleanField(default=True)
    last_name = models.CharField(max_length=64)
    phone = PhoneNumberField(max_length=128)
    role = models.CharField(max_length=5, choices=Roles.choices, default=Roles.USER)

    class Meta:
        """
        Meta information for user model
        """
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.first_name} {self.last_name}'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager()

    @property
    def is_admin(self) -> bool:
        """
        Returns True if the user is an administrator, False otherwise
        """
        return self.role == User.Roles.ADMIN

    @property
    def is_user(self) -> bool:
        """
        Returns True if the user is a regular user, False otherwise
        """
        return self.role == User.Roles.USER

    @property
    def is_superuser(self) -> bool:
        """
        Returns True if the user is a superuser, False otherwise
        """
        return self.is_admin

    @property
    def is_staff(self) -> bool:
        """
        Returns True if the user is a member of staff, False otherwise
        """
        return self.is_admin

    def has_perm(self, perm, obj=None) -> bool:
        """
        Returns True if the user has the specified permission, False otherwise
        """
        return self.is_admin

    def has_module_perms(self, app_label) -> bool:
        """
        Returns True if the user has permissions to view the app with the given label, False otherwise
        """
        return self.is_admin
