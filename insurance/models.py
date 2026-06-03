from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.name
    

class Policy(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('LAPSED', 'Lapsed'),
        ('UNDER_REVIEW', 'Under Review'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='policies'
    )

    policy_type = models.CharField(max_length=100)

    premium_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    def __str__(self):
        return f"{self.policy_type} - {self.status}"
    

class Claim(models.Model):

    PRIORITY_CHOICES = [
        ('NORMAL', 'Normal'),
        ('HIGH_PRIORITY', 'High Priority'),
    ]

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='NORMAL'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim {self.id} - {self.priority}"
    
    
class ActionRequest(models.Model):
    idempotency_key = models.CharField(
        max_length=255,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.idempotency_key