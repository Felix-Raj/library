from rest_framework import serializers

from lib_users.models import LibUsers, Lent


class LibUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibUsers
        fields = ('name', 'uid', 'id', 'avatar')


class LentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lent
        fields = ('lib_user', 'book', 'lent_on', 'due_on', 'duration')

    # todo 5/19/18 felixraj : add necessary validations if needed
    # todo 5/23/18 felixraj : validate weather book is actually available for lent
    # http://www.django-rest-framework.org/api-guide/serializers/#validation


class LentListSerializer(LentSerializer):
    class Meta(LentSerializer.Meta):
        depth = 2
