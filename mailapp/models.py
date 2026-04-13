from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class UserRegistration(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    fromMail = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    sendto = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=100, default="Sent")
    prediction_result = models.CharField(max_length=255, blank=True, null=True)  # New field for prediction result

    def __str__(self):
        return self.fromMail


class Drafts(models.Model):
    fromMail = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    sendto = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=100, default="Draft")

    def __str__(self):
        return self.fromMail


class Feedback(models.Model):
    subject = models.CharField(max_length=100)
    feedback = models.CharField(max_length=300)
    uid = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class BlockList(models.Model):
    blocking_user_id = models.CharField(
        max_length=100
    )  # referring to the user who initiated the block
    blocked_user_id = models.CharField(
        max_length=100
    )  # referring to the user who was blocked
    status = models.CharField(max_length=100, default="Blocked")
