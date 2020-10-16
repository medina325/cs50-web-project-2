from django.contrib.auth.models import AbstractUser
from django.db import models

# Include more things 
class User(AbstractUser):
    pass
    #https://docs.djangoproject.com/en/3.1/topics/auth/default/
class Listing(models.Model):
    listingID = models.AutoField(primary_key=True, serialize=False, verbose_name="listID")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="myListing", null=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    title = models.CharField(max_length=30)
    description = models.TextField()
    creation_date = models.DateField(auto_now=True)
    img_url = models.URLField()
    active = models.BooleanField(default=True)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, related_name="bidsMadeOnMe", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="myBids", null=True)

    price = models.FloatField()
    creation_date = models.DateField(auto_now=True, null=True)
    
class Comment(models.Model):
    creation_date = models.DateField(auto_now=True, null=True)
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, related_name="commentsMadeOnMe", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="myComments", null=True)
