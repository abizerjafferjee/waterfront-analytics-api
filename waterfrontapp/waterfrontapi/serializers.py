from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from . import models

class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password':{'write_only': True}}
    
    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed items."""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile':{'read_only':True}}

class ContactFormSerializer(serializers.ModelSerializer):
    """A serializer for contact form."""

    class Meta:
        model = models.ContactForm
        fields = ('id', 'name', 'email', 'company', 'role')

    def create(self, validated_data):
        instance = super(ContactFormSerializer, self).create(validated_data)

        subject = 'Waterfront Analytics has a new lead'
        body = 'Name: {0}\nEmail: {1}\nCompany: {2}\nRole: {3}'.format(
            validated_data['name'],
            validated_data['email'],
            validated_data['company'],
            validated_data['role'],
        )

        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]
        )

        email.send()

        return instance

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """A serializer for blog posts."""

    tags = TagListSerializerField()

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'slug', 'description', 'url', 'tags', 'created_at', 'updated_at')
