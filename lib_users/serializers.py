from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.models import Book
from lib_users.models import LibUsers, Lent


class LibUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibUsers
        fields = ('name', 'uid', 'id', 'avatar', 'date_of_birth', 'father',
                  'mother', 'account_activated', 'user_type')


class LentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lent
        fields = ('id', 'lent_on', 'duration', 'due_on', 'lib_user', 'book')

    def validate(self, data):
        # check weather required number of books are available
        # - should be done on view. Lent and return will use the same
        #   serializer class so validation here is not straight forward
        return data


class LentListSerializer(LentSerializer):
    class Meta(LentSerializer.Meta):
        depth = 2
