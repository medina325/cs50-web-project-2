from django.urls import path

from . import views

urlpatterns = [
    path("searchResults", views.search, name="searchresults"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="createlisting"),
    path("newListing", views.new_listing_view, name="newlisting"),
    path("placingBid", views.place_bid, name="placingbid"),
    path("listingPage/<int:l_id>", views.listing_view, name="listingpage"),
    path("actListing", views.activate_listing, name="actlisting"),
    path("deactListing", views.deactivate_listing, name="deactlisting"),
    path("addRemoveWatchlist", views.add_remove_watchlist, name="add_remove_watchlist"),
    path("watchList", views.watchlist_view, name="watchlist"),
    path("wonListings", views.won_listings_view, name="wonlistings"),
    path("placeComment", views.place_comment, name="placecomment"),
    path("myListings", views.my_listings_view, name="mylistings"),
    path("<str:category_name>", views.category_listings_view, name="categorylistings"),
]
