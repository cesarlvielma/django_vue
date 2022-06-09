from rest_framework import serializers
from users.models import User, Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        address = Address.objects.create(**validated_data.pop('address'))
        instance = User.objects.create(**validated_data, address=address)
        return instance

    def to_representation(self, instance):
        user = super(UserSerializer, self).to_representation(instance)
        user['address'] = AddressSerializer(instance.address).data
        return user


