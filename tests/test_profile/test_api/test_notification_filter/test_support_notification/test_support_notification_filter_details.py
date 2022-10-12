from rest_framework import status
from rest_framework.reverse import reverse

from tests.test_profile.base_test_profile import BaseTestProfile
from tests.utils import check_data_in_dict


class TestApiSupportNotificationFilterDetails(BaseTestProfile):

    def setUp(self):
        super(TestApiSupportNotificationFilterDetails, self).setUp()
        self.kwargs = {
            'pk': self.support_notification_filter_test.id
        }
        self.get_notification_filter_details_url = reverse('api_support_notification_filter_details', kwargs=self.kwargs)
        self.expected_data = {
            'id': self.support_notification_filter_test.id,
            'name': self.support_notification_filter_test.name,
            'profile': self.support_notification_filter_test.profile.id,
            'services': list(self.support_notification_filter_test.services.all()),
            'instance_states': self.support_notification_filter_test.instance_states,
            'when': self.support_notification_filter_test.when,
        }
        self.expected_data_list = [self.expected_data]

    def test_admin_get_notification_filter_detail(self):
        response = self.client.get(self.get_notification_filter_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_list = [response.data]
        check_data_in_dict(self, self.expected_data_list, data_list)

    def test_admin_cannot_get_notification_filter_detail_of_another_user(self):
        self.client.force_login(self.superuser_2)
        response = self.client.get(self.get_notification_filter_details_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_cannot_get_notification_filter_detail(self):
        self.client.force_login(user=self.standard_user)
        response = self.client.get(self.get_notification_filter_details_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_get_request_details_when_logout(self):
        self.client.logout()
        response = self.client.get(self.get_notification_filter_details_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)