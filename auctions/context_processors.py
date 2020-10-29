from auctions.models import Category
# Context processor
def add_categories_to_every_context(request):
    return {
        'categories': Category.objects.all()
    }