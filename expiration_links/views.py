from datetime import datetime, timedelta
from uuid import uuid4

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from expiration_links.models import ExpirationLink
from expiration_links.serializers import ExpirationLinkGeneratorSerializer


class ExpirationLinksView(viewsets.ViewSet):
    def create(self, request):
        result = ExpirationLinkGeneratorSerializer(data=request.data, context={'user': request.user})
        if result.is_valid():
            token = uuid4()
            expiration_date = datetime.now() + timedelta(seconds=result.data.get('expiration_time'))
            url = result.data.get('url')
            ExpirationLink.objects.create(url=url, token=token, expiration_date=expiration_date)

            expiration_link_parts = url.rsplit('.', 1)
            expiration_link = f'{expiration_link_parts[0]}{token}.{expiration_link_parts[1]}'
            return Response({'link': expiration_link})
        return Response({'msg': 'klops'})
