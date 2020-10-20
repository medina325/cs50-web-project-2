from django.contrib import admin

from auctions.models import *

# Customizing the Admin Interface 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class ListingAdmin(admin.ModelAdmin):
    list_display = ("created_by", "category", "title", "description", "creation_date", "img_url", "active", "current_bid")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "price", "creation_date")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("creation_date", "content", "listing", "user")

# Register your models here.
# admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)