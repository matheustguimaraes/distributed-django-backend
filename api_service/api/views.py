# encoding: utf-8

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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns the list of entries saved in the database.
        The latest entries are shown first
        """
        stock_code = request.query_params.get('q')

        if stock_code is None:
            error_msg = {'error': 'Stock symbol was not provided.'}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        # use docker container name to request /stock endpoint
        request_url = f'http://stock:8000/stock?q={stock_code}'
        response = requests.get(request_url)

        if response.status_code == 401:
            error_msg = {'error': 'JWT Authentication credentials were not provided.'}
            return Response(error_msg, status=status.HTTP_401_UNAUTHORIZED)

        if response.status_code == 400:
            error_msg = {'error': 'Request has incorrect stock symbol.'}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        if response.status_code != 200:
            return Response(response, status=response.status_code)

        # convert keys (Open, Close, High, Low) to lowercase
        json_response = {key.lower(): value for key, value in response.json().items()}
        date_field_format = f'{json_response["date"]} {json_response["time"]}'
        # parse `date` to django.db.models.DateTimeField() format
        json_response['date'] = dp.parse(date_field_format)

        # save user request history
        usr_req_history = UserRequestHistorySerializer(data=json_response)
        if usr_req_history.is_valid(raise_exception=True):
            usr_req_history.save(user=request.user)

        return Response(usr_req_history.data)


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserRequestHistorySerializer

    def get_queryset(self, *args, **kwargs):
        """
        Get queryset by authenticated user
        """
        user = self.request.user
        return UserRequestHistory.objects.filter(user=user).order_by('-date')


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        Returns the top five most requested stocks
        """
        user = request.user
        stocks_by_time_requested = UserRequestHistory.objects.filter(user=user).values('symbol').annotate(
            times_requested=Count('symbol')).order_by('-times_requested')[:5]
        return Response(stocks_by_time_requested)
