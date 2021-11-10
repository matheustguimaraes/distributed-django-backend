from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class StockServiceAPIViewTestCase(APITestCase):
    """Test stock_service endpoint"""
    def setUp(self):
        self.client = APIClient()

    def test_get_stock(self):
        """Test GET /stock endpoint"""
        response = self.client.get(reverse('stock'), {'q': 'aapl.us'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_stock_without_query_params(self):
        """Test GET /stock endpoint without query parameters"""
        response = self.client.get(reverse('stock'))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_stock_with_wrong_stock_ticket(self):
        """Test GET /stock endpoint with wrong stock ticket"""
        response = self.client.get(reverse('stock'), {'q': 'abcd.ef'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
