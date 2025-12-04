from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Listing(models.Model):
    titre = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    groupe = models.CharField(max_length=255, blank=True, null=True)
    membre = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='photocards/')
    consent_given = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.titre or "sans titre"


class Selling(models.Model):  # vente entre utilisateurs
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)  # relier à une photocard du dictionnaire
    seller = models.ForeignKey(User, on_delete=models.CASCADE)      # qui vend
    price = models.DecimalField(max_digits=10, decimal_places=2)    # prix obligatoire
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listing.title} vendu par {self.seller.username}"
    
    from django.db import models

from django.db import models
from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    consent_given = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Anonyme'} - {self.message[:30]}"
    
class Photocard(models.Model):
    image = models.ImageField(upload_to='photocards/')
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)