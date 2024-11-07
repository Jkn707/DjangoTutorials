from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()

'''
INSERT INTO pages_comment (product_id, description) VALUES (1, 'This is a fantastic product!');
INSERT INTO pages_comment (product_id, description) VALUES (1, 'Not bad, but could be improved.');
INSERT INTO pages_comment (product_id, description) VALUES (1, 'Excellent value for money.');
'''