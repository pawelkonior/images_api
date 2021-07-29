from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from expiration_links.models import ExpirationLink
from images.models import Image


class ExpirationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpirationLink
        fields = ('url', 'expiration_date')


class ExpirationLinkGeneratorSerializer(serializers.Serializer):
    url = serializers.URLField()
    expiration_time = serializers.IntegerField()

    def validate_url(self, value):
        user = self.context['user']
        link = '/'.join(value.rsplit('/', 2)[-2:])
        image_url = Image.objects.filter(url=link, author=user)

        if not image_url:
            raise serializers.ValidationError("We can not find link to original image!")
        return value

#
# {
# "expiration_time": 30,
# "url":"http://0.0.0.0:8000/media/images/Screenshot_from_2021-07-20_21-13-53.png"
# }

