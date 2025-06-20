from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Feed
from .serializers import FeedSerializer


class Feeds(APIView):
    # 전체 게시글 데이터 조회
    def get(self, request):
        feeds = Feed.objects.all()

        # 객체 -> JSON (Serialize)
        serializer = FeedSerializer(feeds, many=True)

        return Response(serializer.data)

class FeedDetail(APIView):
    def get_object(self, feed_id):
        try:
            return Feed.objects.get(id=feed_id)
        except Feed.DoesNotExist:
            raise NotFound

    def get(self, request, feed_id):
        feed = self.get_object(feed_id)
        # feed (object) => json => serializer

        serializer = FeedSerializer(feed)
        print(serializer)

        return Response(serializer.data)