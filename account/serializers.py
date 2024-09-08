from rest_framework.serializers import ModelSerializer

from account.models import User


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
