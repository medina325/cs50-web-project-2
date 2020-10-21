from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="createlisting"),
    path("newListing", views.new_listing_view, name="newlisting"),
    path("placingBid", views.place_bid, name="placingbid"),
    path("listingPage/<int:l_id>", views.listing_view, name="listingpage"),
    path("addRemoveWatchlist", views.add_remove_watchlist, name="add_remove_watchlist"),
    path("watchList", views.watchlist_view, name="watchlist"),
    path("<slug:category_name>", views.category_listings_view, name="categorylistings"),
]
