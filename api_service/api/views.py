# encoding: utf-8
import json

import requests
from dateutil import parser as dp
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer


class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """

    # todo: use authentication_classes
    # authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')

        if stock_code is None:
            return Response({'error': 'Stock symbol was not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        request_url = f'http://localhost:8000/stock?q={stock_code}'
        response = requests.get(request_url)

        if not request.user.is_authenticated:
            error_msg = {'error': 'JWT Authentication credentials were not provided.'}
            return Response(error_msg, status=status.HTTP_403_FORBIDDEN)

        if response.status_code == 400:
            # json.loads is used to avoid parsing data to JSON twice
            return Response(json.loads(response.text), status=status.HTTP_400_BAD_REQUEST)

        # todo: check different status code (server error and more)

        # todo: move logic to serializers
        stock_quotes = json.loads(response.text)
        stock_quotes = {key.lower(): value for key, value in stock_quotes.items()}
        date_field_format = f"{stock_quotes['date']} {stock_quotes['time']}"

        # date = parse_datetime(date_field_format)
        stock_quotes['date'] = dp.parse(date_field_format)
        stock_quotes['user'] = request.user.id

        user_history = UserRequestHistorySerializer(data=stock_quotes)
        if user_history.is_valid(raise_exception=True):
            user_history.save()

        return Response(user_history.data)


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserRequestHistorySerializer

    def get_queryset(self, *args, **kwargs):
        """
        Get queryset by authenticated user
        """
        user = self.request.user
        return UserRequestHistory.objects.filter(user=user)


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        """
        Returns the top five most requested stocks
        """
        user = request.user
        stocks_by_time_requested = UserRequestHistory.objects.filter(user=user).values('symbol').annotate(
            times_requested=Count('symbol')).order_by('-times_requested')[:5]
        return Response(stocks_by_time_requested)
