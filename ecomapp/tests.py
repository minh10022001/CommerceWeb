from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import *

user = User.objects.all()
print(user)
print("abc")