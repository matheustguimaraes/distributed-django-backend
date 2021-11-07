# encoding: utf-8
import csv
from io import StringIO

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class StockView(APIView):
    """
    Receives stock requests from the API service.
    """

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        request_url = f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv'

        csv_response = requests.get(request_url)
        # Stooq API returns CSV formatted response with e=csv, so we convert the response to JSON format
        json_response = next(csv.DictReader(StringIO(csv_response.text)))

        if json_response['Close'] == 'N/D':
            json_response['error'] = 'Request has incorrect stock symbol.'
            return Response(json_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(json_response, status=status.HTTP_200_OK)
