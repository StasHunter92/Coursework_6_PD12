from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Comment
from users.models import User
from users.serializers import UserSerializer


# ----------------------------------------------------------------------------------------------------------------------
# Advertisement serializers
class AdvertisementListSerializer(serializers.ModelSerializer):
    """
    List serializer for ViewSet
    """

    class Meta:
        model: Advertisement = Advertisement
        fields: list[str] = ['pk', 'image', 'title', 'price', 'description']


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    """
    Detail serializer for ViewSet
    """
    phone = serializers.SerializerMethodField()
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()

    class Meta:
        model: Advertisement = Advertisement
        fields: list[str] = ['pk', 'image', 'title', 'price', 'phone', 'description',
                             'author_first_name', 'author_last_name', 'author_id']

    def get_phone(self, obj) -> str:
        """
        Returns the phone number associated with the author

        :param obj: An Advertisement object
        :return: A string formatted phone number
        """
        return str(obj.author.phone)

    def get_author_first_name(self, obj) -> str:
        """
        Returns the first name associated with the author

        :param obj: An Advertisement object
        :return: A string formatted first name
        """
        return obj.author.first_name

    def get_author_last_name(self, obj) -> str:
        """
        Returns the last name associated with the author

        :param obj: An Advertisement object
        :return: A string formatted last name
        """
        return obj.author.last_name


class AdvertisementCreateSerializer(AdvertisementDetailSerializer):
    """
    Create serializer for ViewSet
    """
    author = serializers.SlugRelatedField(
        write_only=True,
        slug_field='id',
        queryset=User.objects.all())
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model: Advertisement = Advertisement
        fields: list[str] = ['pk', 'image', 'title', 'price', 'phone', 'description',
                             'author_first_name', 'author_last_name', 'author_id', 'author']

    def is_valid(self, raise_exception=False) -> bool:
        """
        Validate data

        :return: True if valid else False
        """
        self.initial_data['author'] = self.context['request'].user.id

        return super().is_valid(raise_exception=raise_exception)


class AdvertisementUpdateSerializer(AdvertisementListSerializer):
    """
    Update serializer for ViewSet
    """

    class Meta:
        model = Advertisement
        fields = ['pk', 'image', 'title', 'price', 'phone', 'description', 'author_first_name', 'author_last_name',
                  'author_id']


# ----------------------------------------------------------------------------------------------------------------------
# Comment serializers
class CommentSerializer(serializers.ModelSerializer):
    """
    Main serializer for ViewSet
    """
    author_image = serializers.SerializerMethodField()
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()

    class Meta:
        model: Comment = Comment
        fields: list[str] = ['pk', 'text', 'author_id', 'created_at',
                             'author_first_name', 'author_last_name', 'ad_id', 'author_image']

    def get_author_image(self, obj) -> str:
        """
        Returns the image associated with the author

        :param obj: A Comment object
        :return: A string formatted image path
        """
        request = self.context.get('request')
        serializer = UserSerializer(instance=obj.author, context={'request': request})
        return serializer.data.get('image')

    def get_author_first_name(self, obj) -> str:
        """
        Returns the first name associated with the author

        :param obj: A Comment object
        :return: A string formatted first name
        """
        return obj.author.first_name

    def get_author_last_name(self, obj) -> str:
        """
        Returns the last name associated with the author

        :param obj: A Comment object
        :return: A string formatted last name
        """
        return obj.author.last_name


class CommentCreateSerializer(CommentSerializer):
    """
    Create serializer for ViewSet
    """

    class Meta:
        model: Comment = Comment
        fields: list[str] = ['pk', 'text', 'author_id', 'created_at',
                             'author_first_name', 'author_last_name', 'ad_id', 'author_image']
        read_only_fields: list[str] = ['author_image', 'author_first_name', 'author_last_name']

    def create(self, validated_data):
        """
        Create a new comment
        """
        ad_id = self.context['request'].parser_context['kwargs']['ad_id']
        author = self.context['request'].user

        try:
            _ = Advertisement.objects.get(id=ad_id)
        except Advertisement.DoesNotExist:
            raise ValidationError({'detail': 'Неизвестное объявление'})

        validated_data['author'] = author
        validated_data['ad_id'] = ad_id

        comment = super().create(validated_data)

        return comment
