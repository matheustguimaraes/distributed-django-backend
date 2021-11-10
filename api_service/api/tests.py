from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer


class APIServiceAPIViewTestCase(APITestCase):
    """
    Test api_service endpoints.
    endpoints: /stock, /history, /stats, /auth/token
    """

    def setUp(self):
        """
        Create normal user, superuser and API clients for each user
        """
        # create user
        self.user_username = "user_test"
        self.user_email = "usertest@gmail.com"
        self.user_password = "password_password_password"
        self.user = User.objects.create_user(self.user_username, self.user_email, self.user_password)
        self.usr_req_hist = UserRequestHistory.objects.create(
            date='2021-11-09T20:19:18Z',
            symbol='AAPL.us',
            open="150.200",
            high="151.428",
            low="150.070",
            name="APPLE",
            close="150.750",
            user=self.user)

        # create super user
        self.admin_username = "admin"
        self.admin_email = "superusertest@gmail.com"
        self.admin_password = "admin"
        self.admin = User.objects.create_superuser(self.admin_username, self.admin_email, self.admin_password)

        # create APIClient() for both user and superuser
        self.user_client = self._get_client(self.user_username, self.user_password)
        self.admin_client = self._get_client(self.admin_username, self.admin_password)

    def _get_client(self, username, password):
        """
        Return APIClient with user JWT Authentication credentials
        """
        client = APIClient()
        url = reverse('token_obtain_pair')

        # get user JWT credentials
        response = client.post(url, {'username': username, 'password': password})
        # check if JWT credentials are correct
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # set credentials
        jwt_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        return client

    def test_jwt_authentication(self):
        """Check if JWT endpoint authenticate with wrong credentials"""
        client = APIClient()
        url = reverse('token_obtain_pair')

        # correct credentials
        resp_auth = client.post(url, {'username': self.user_username, 'password': self.user_password})
        self.assertEqual(status.HTTP_200_OK, resp_auth.status_code)
        # wrong credentials
        resp_no_auth = client.post(url, {'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp_no_auth.status_code)

    def test_endpoints_no_auth(self):
        """Test endpoints response without JWT authentication"""
        client = APIClient()
        history_endpoint = reverse('history')
        stock_endpoint = reverse('stock')
        stats_endpoint = reverse('stats')

        stock_response = client.get(stock_endpoint)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, stock_response.status_code)

        history_response = client.get(history_endpoint)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, history_response.status_code)

        stats_response = client.get(stats_endpoint)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, stats_response.status_code)

    def test_get_history_user(self):
        """Test /history endpoint returns HTTP 200 with user without admin privileges"""
        response = self.user_client.get(reverse('history'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_history_superuser(self):
        """Test /history endpoint returns HTTP 200 with superuser"""
        response = self.admin_client.get(reverse('history'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_stats_user(self):
        """Test /stats endpoint returns HTTP 403 with user without admin privileges"""
        response = self.user_client.get(reverse('stats'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_stats_superuser(self):
        """Test /stats endpoint returns HTTP 200 with superuser"""
        response = self.admin_client.get(reverse('stats'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_user_request_history_user(self):
        """Test if /stock endpoint returns UserRequestHistory serializer"""
        response = self.user_client.get(reverse('stock'), {'q': 'aapl.us'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # check by serializer length
        serializer = UserRequestHistorySerializer(instance=self.usr_req_hist).data
        self.assertTrue(len(response.json()) == len(serializer))
