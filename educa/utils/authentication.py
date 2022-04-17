from ast import keyword
from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'