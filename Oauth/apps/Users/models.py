from django.db import models
import re
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    ##validation for registeration information
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if len(postData['email']) < 1:
            errors['emaillen'] = "Email is required."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['emailvalid'] = "Email is not valid."
        elif User.objects.filter(email=postData['email']):
            errors['emailtaken'] = "Email was already registered."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords do not match."
        return errors

    #validaton for login especially for the bcrypt passord so users don't login without pw
    def loginvalidator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Please input an email."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['email'] = "Email is not valid."
        elif not User.objects.filter(email=postData['email']):
            errors['email'] = "This email is not registered in our database."
        if len(postData['password']) < 1:
            errors['password'] = "Please input a password."
        elif len(postData['password']) < 8:
            errors['password'] = "Invalid login."
        elif bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()) == False:
            errors['password'] = "Invalid login."
        return errors

class User(models.Model):
    ##required registration information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
