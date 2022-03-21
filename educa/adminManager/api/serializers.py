from rest_framework import serializers
from ..models import User,Profile

class UserBasicSzr(serializers.ModelSerializer):
    pic = serializers.URLField(source='profile.pic.url',read_only=True)
    class Meta:
        model = User
        fields = [
            'id','username','get_full_name','pic'
        ]
        related_field = ['profile']
        read_only_fields = fields
    
    

