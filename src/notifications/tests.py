from rest_framework.test import APITestCase
from rest_framework.routers import reverse
from notifications.models import *
from notifications.serializers import *


class LowonganListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            phone='77777777777',
            phone_code='+7',
            tag="tag1 tag2",
            timezone = "Asia/Almaty"
        )

        self.customer_url = reverse("customers-list")
        self.customer_detail_url = reverse(
            "customers-detail", kwargs={ "pk": self.customer.pk})

    def test_customers_list(self):
        """
        Test to customer list
        """
        response = self.client.get(self.customer_url)
        self.assertEqual(200, response.status_code)


    def test_customers_detail(self):
        """
        Test to customer detail
        """
        response = self.client.get(self.customer_detail_url)
        self.assertEqual(200, response.status_code)

        customer_serializer_data = CustomerSerializer(instance=self.customer).data
        response_data = response.json()
        self.assertEqual(customer_serializer_data, response_data)

    def test_customers_create(self):
        """
        Test to customer create
        """
        data = {
            'phone': '77777777777',
            'phone_code': '+7',
            'tag': "tag1 tag2",
            'timezone': "Asia/Almaty"
        }
        response = self.client.post(self.customer_url, data=data)
        self.assertEqual(400, response.status_code)

        data['phone'] = '77777777778'
        response = self.client.post(self.customer_url, data=data)
        self.assertEqual(201, response.status_code)
        customer_created = Customer.objects.filter(pk=response.json()['id']).exists()
        self.assertTrue(customer_created)


    def test_customers_update(self):
        """
        Test to customer update
        """
        data = {
            'phone': '77777777778',
        }
        response = self.client.patch(self.customer_detail_url, data=data)
        self.assertEqual(200, response.status_code)
        customer = Customer.objects.get(pk=self.customer.pk)
        self.assertEqual(customer.phone, data['phone'])


    def test_customers_delete(self):
        """
        Test to customer delete
        """
        response = self.client.delete(self.customer_detail_url)
        self.assertEqual(204, response.status_code)
        customer = Customer.objects.filter(pk=self.customer.pk).exists()
        self.assertFalse(customer)
