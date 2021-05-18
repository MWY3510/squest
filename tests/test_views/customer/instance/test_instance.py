from django.urls import reverse

from service_catalog.models import Support, Message, SupportMessage
from service_catalog.models.instance import InstanceState
from service_catalog.models.support import SupportState
from tests.base_test_request import BaseTestRequest


class TestCustomerInstanceViews(BaseTestRequest):

    def setUp(self):
        super(TestCustomerInstanceViews, self).setUp()
        self.client.login(username=self.standard_user, password=self.common_password)

    def test_get_instance_list(self):
        url = reverse('customer_instance_list')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(len(response.context["instances"]), 1)

    def test_get_instance_details(self):
        args = {
            "instance_id": self.test_instance.id
        }
        url = reverse('customer_instance_details', kwargs=args)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTrue("instance" in response.context)
        self.assertEquals(self.test_instance.name, response.context["instance"].name)

    def test_non_owner_user_cannot_get_details(self):
        self.client.login(username=self.standard_user_2, password=self.common_password)
        args = {
            "instance_id": self.test_instance.id
        }
        url = reverse('customer_instance_details', kwargs=args)
        response = self.client.get(url)
        self.assertEquals(403, response.status_code)

    def test_create_new_support_on_instance(self):
        args = {
            "instance_id": self.test_instance.id
        }
        url = reverse('customer_instance_new_support', kwargs=args)
        data = {
            "title": "test_support",
            "content": "test_support_content"
        }
        number_support_before = Support.objects.all().count()
        response = self.client.post(url, data=data)
        self.assertEquals(302, response.status_code)
        self.assertEquals(number_support_before + 1, Support.objects.all().count())

    def test_cannot_create_new_support_on_non_owned_instance(self):
        self.client.login(username=self.standard_user_2, password=self.common_password)
        args = {
            "instance_id": self.test_instance.id
        }
        url = reverse('customer_instance_new_support', kwargs=args)
        data = {
            "title": "test_support",
            "content": "test_support_content"
        }
        response = self.client.post(url, data=data)
        self.assertEquals(403, response.status_code)

    def test_get_customer_instance_support_details(self):
        args = {
            "instance_id": self.test_instance.id,
            "support_id": self.support_test.id
        }
        url = reverse('customer_instance_support_details', kwargs=args)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTrue("support" in response.context)
        self.assertEquals(self.support_test.title, response.context["support"].title)

    def test_close_instance_support(self):
        args = {
            "instance_id": self.test_instance.id,
            "support_id": self.support_test.id
        }
        url = reverse('customer_instance_support_details', kwargs=args)
        data = {
            "btn_close": True
        }
        response = self.client.post(url, data=data)
        self.assertEquals(302, response.status_code)
        self.support_test.refresh_from_db()
        self.assertEquals(self.support_test.state, SupportState.CLOSED)

    def test_reopen_instance_support(self):
        self.support_test.state = SupportState.CLOSED
        self.support_test.save()
        args = {
            "instance_id": self.test_instance.id,
            "support_id": self.support_test.id
        }
        url = reverse('customer_instance_support_details', kwargs=args)
        data = {
            "btn_re_open": True
        }
        response = self.client.post(url, data=data)
        self.assertEquals(302, response.status_code)
        self.support_test.refresh_from_db()
        self.assertEquals(self.support_test.state, SupportState.OPENED)

    def test_reopen__already_opened_instance_support(self):
        args = {
            "instance_id": self.test_instance.id,
            "support_id": self.support_test.id
        }
        url = reverse('customer_instance_support_details', kwargs=args)
        data = {
            "btn_re_open": True
        }
        response = self.client.post(url, data=data)
        self.assertEquals(403, response.status_code)
        self.support_test.refresh_from_db()
        self.assertEquals(self.support_test.state, SupportState.OPENED)

    def test_add_message_to_existing_support(self):
        args = {
            "instance_id": self.test_instance.id,
            "support_id": self.support_test.id
        }
        url = reverse('customer_instance_support_details', kwargs=args)
        data = {
            "content": "new message"
        }
        number_message_before = SupportMessage.objects.filter(support=self.support_test).count()
        response = self.client.post(url, data=data)
        self.assertEquals(302, response.status_code)
        self.assertEquals(number_message_before + 1,
                          SupportMessage.objects.filter(support=self.support_test).count())

    def test_archive_instance(self):
        self.test_instance.state = InstanceState.DELETED
        self.test_instance.save()
        args = {
            "instance_id": self.test_instance.id
        }
        url = reverse('customer_instance_archive', kwargs=args)
        response = self.client.post(url)
        self.assertEquals(302, response.status_code)
        self.test_instance.refresh_from_db()
        self.assertEquals(self.test_instance.state, InstanceState.ARCHIVED)

    def test_cannot_archive_non_deleted_instance(self):
        self.test_instance.state = InstanceState.AVAILABLE
        args = {
            "instance_id": self.test_instance.id
        }
        url = reverse('customer_instance_archive', kwargs=args)
        response = self.client.post(url)
        self.assertEquals(403, response.status_code)
        self.test_instance.refresh_from_db()
        self.assertEquals(self.test_instance.state, InstanceState.PENDING)