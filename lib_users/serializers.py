from rest_framework import serializers

from lib_users.models import LibUsers, Lent


class LibUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibUsers
        fields = ('name', 'uid', 'id', 'avatar', 'date_of_birth')


class LentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lent
        fields = ('id', 'lent_on', 'duration', 'due_on', 'lib_user', 'book')


class LentListSerializer(LentSerializer):
    class Meta(LentSerializer.Meta):
        depth = 2
