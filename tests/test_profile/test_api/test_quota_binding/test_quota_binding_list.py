from rest_framework import status
from rest_framework.reverse import reverse

from profiles.models import QuotaBinding
from tests.test_profile.test_quota.base_test_quota import BaseTestQuota


class TestApiQuotaBindingList(BaseTestQuota):

    def setUp(self):
        super(TestApiQuotaBindingList, self).setUp()
        self.get_quota_list_url = reverse('api_quota_binding_list_create')

    def test_get_all_quota(self):
        response = self.client.get(self.get_quota_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], QuotaBinding.objects.count())

    def test_customer_cannot_get_quota_list(self):
        self.client.force_login(user=self.standard_user)
        response = self.client.get(self.get_quota_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_get_quota_list_when_logout(self):
        self.client.logout()
        response = self.client.get(self.get_quota_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)