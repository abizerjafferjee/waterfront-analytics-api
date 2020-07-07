from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from taggit.managers import TaggableManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Helps django work with our customer user model."""

    def create_user(self, email, name, password=None):
        """Creates a new user profile"""

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser."""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a user profile inside our system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a user's full name."""
        return self.name

    def get_short_name(self):
        """Used to get a user's short name"""
        return self.name

    def __str__(self):
        """convert object to string"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update."""

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return model as a string."""

        return self.status_text

class ContactForm(models.Model):
    """Contact form model."""

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        """Return model as a string."""
        return self.email

class Post(models.Model):
    """
    Blog post model.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title