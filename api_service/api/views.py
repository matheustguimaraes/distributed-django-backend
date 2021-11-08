# encoding: utf-8
import json

import requests
from dateutil import parser as dp
from rest_framework import generics, status, viewsets
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
        request_url = f'http://localhost:8000/stock?q={stock_code}'

        response = requests.get(request_url)

        if not request.user.is_authenticated:
            error_msg = {'error': 'Please Authenticate to continue.'}
            return Response(error_msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if response.status_code == 400:
            # json.loads is used to avoid parsing data to JSON twice
            return Response(json.loads(response.text), status=status.HTTP_400_BAD_REQUEST)

        # todo: check different status code (server error and more)

        # todo: move logic to serializers
        stock_quotes = json.loads(response.text)
        quotes_lowercase_key = {key.lower(): value for key, value in stock_quotes.items()}
        date_field_parse_format = f"{quotes_lowercase_key['date']} {quotes_lowercase_key['time']}"

        # date = parse_datetime(date_field_parse_format)
        quotes_lowercase_key['date'] = dp.parse(date_field_parse_format)
        quotes_lowercase_key['user'] = request.user.id

        user_history_serializer = UserRequestHistorySerializer(data=quotes_lowercase_key)
        if user_history_serializer.is_valid():
            user_history_serializer.save()

        return Response(json.loads(response.text), status=status.HTTP_200_OK)


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    # TODO: Filter the queryset so that we get the records for the user making the request.


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    def get(self, request, *args, **kwargs):
        return Response()
