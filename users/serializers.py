from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('employeeId', 'firstName', 'lastName', 'email', 'role')

        
# {
# "employeeId":"1204",
# "firstName":"Dummy",
# "lastName":"User",
# "email":"Dummy@example.com",
# "role":"Developer"
# }