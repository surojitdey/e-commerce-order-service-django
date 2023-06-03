from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
  class Status(models.TextChoices):
    PENDING = 'PENDING'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'

  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
  status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return self.user

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=False, related_name='items')
  name = models.CharField(max_length=100, blank=False, null=False)
  quantity = models.PositiveIntegerField(blank=False, null=False)
  price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

  def __str__(self):
    return self.order
