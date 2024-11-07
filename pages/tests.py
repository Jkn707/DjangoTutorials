from django.test import TestCase
from django.urls import reverse
from pages.models import Product

# Create your tests here.
class ShowPageTestCase(TestCase):

    def setUp(self):
        # Create a sample Product object for testing
        self.product = Product.objects.create(name='Test Product', price=100)

    def test_num_queries(self):
        # Assuming only one query is executed to fetch the Product object
        with self.assertNumQueries(1):
            response = self.client.get(reverse('show', args=[self.product.id]))
            self.assertEqual(response.status_code, 200)