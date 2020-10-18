from django.contrib.auth.models import AbstractUser
from django.db import models

# Include more things 
class User(AbstractUser):
    pass
    #https://docs.djangoproject.com/en/3.1/topics/auth/default/

class Category(models.Model):
    name = models.TextField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    listingID = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="listID")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="myListing", null=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings_on_this_category", null=True, blank=True)

    title = models.CharField(max_length=30)
    description = models.TextField()
    creation_date = models.DateField(auto_now=True)
    img_url = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, related_name="bidsMadeOnMe", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="myBids", null=True)

    price = models.FloatField()
    creation_date = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f"Bid={self.price}"

class Comment(models.Model):
    creation_date = models.DateField(auto_now=True, null=True)
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, related_name="commentsMadeOnMe", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="myComments", null=True)
