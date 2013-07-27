from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from events.models import FacebookEvent, PersonalEvent

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given username, first_name, last_name and password.
        """
        user = self.create_user(username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
        db_index=True,
    )

    email = models.EmailField(verbose_name="email address", max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    thumbnail_profile_pic = models.TextField(null=True, blank=True)
    profile_pic = models.TextField(null=True, blank=True)
    personal_events = models.ManyToManyField(FacebookEvent, through=PersonalEvent)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
