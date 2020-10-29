from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import re

from .models import *
from django.db import models

def index(request):
    return render(request, "auctions/index.html", {
        "Header": "Active Listings",
        "listing_list": Listing.objects.filter(active=True) 
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# -----------------------------------------------------------------------------------------------------------------
@login_required
def create_listing(request):
    if request.method == "POST":
        user = request.user
        l = Listing(created_by=user, 
                    category=Category.objects.get(name=request.POST["category_chosen"]),
                    title=request.POST["title"], 
                    description=request.POST["desc"], 
                    # https://stackoverflow.com/questions/12176585/handling-dates-over-request-get 
                    img_url=request.POST["image_url"],
                    current_bid=request.POST["initial_bid"]
                    )
        l.save()

        b = Bid(listing=l,
                user=user, 
                price=request.POST["initial_bid"]
                )
        b.save()

    return render(request, "auctions/index.html", {
        "Header": "Active Listings",
        "listing_list": Listing.objects.filter(active=True)
    })

@login_required
def new_listing_view(request):
    return render(request, "auctions/new_listing.html", {
        "Header": "Create a new listing",
        "category_list": Category.objects.all()
    })

@login_required
def place_bid(request):
    if request.method == "POST":
        user = request.user
        new_bid = request.POST["new_bid"]
        l_id = pk=request.POST["id"]
        l = Listing.objects.get(pk=l_id)
        l.current_bid = new_bid
        l.save()
        
        b = Bid(listing=l,
                user=user,
                price=request.POST["new_bid"]
                )
        b.save()

    return HttpResponseRedirect(reverse("listingpage", args=(l.listingID,)))

def listing_view(request, l_id):
    l = Listing.objects.get(pk=l_id)

    # Get all listings on this category except for the listing that is being shown
    listings_on_this_category = l.category.listings_on_this_category.exclude(pk=l_id)
    
    if request.user.is_authenticated:
        return render(request, "auctions/listing_page.html", {
            "listing": l,
            "watchlist": request.user.watchlist.filter(pk=l_id).exists(),
            "listings_on_this_category": listings_on_this_category,
            "same_category_flag": listings_on_this_category.exists(),
            "commentary_list": l.comments_made_on_me.all()
        })
    else:
        return render(request, "auctions/listing_page.html", {
            "listing": l,
            "listings_on_this_category": listings_on_this_category,
            "same_category_flag": listings_on_this_category.exists(),
            "commentary_list": l.comments_made_on_me.all()
        })       

@login_required
def activate_listing(request):
    if request.method == "POST":
        l_id = request.POST["id"]
        listing = Listing.objects.get(pk=l_id)

        listing.active = True
        listing.save()
        return HttpResponseRedirect(reverse("listingpage", args=(listing.listingID,)))

@login_required
def deactivate_listing(request):
    if request.method == "POST":
        l_id = request.POST["id"]
        listing = Listing.objects.get(pk=l_id)

        higher_bid_price = 0
        for bid in listing.bids_made_on_me.all():
            if bid.price > higher_bid_price:
                higher_bid_price = bid.price
                higher_bid = bid
        
        # Note that if no one placed a bid, the listing is still gonna be closed (which is going to be verified in the listing_page template)
        if higher_bid.user != listing.created_by:
            listing.winner = higher_bid.user
            # if listing is on the winner's watchlist then it's gonna get removed from it
            if (watchlist:=listing.winner.watchlist).filter(pk=l_id).exists():
                watchlist.remove(listing)
        
        listing.active = False
        listing.save()
        
    return HttpResponseRedirect(reverse("listingpage", args=(listing.listingID,)))

@login_required
def add_remove_watchlist(request):
    if request.method == "POST":
        user = request.user
        l_id = request.POST["id"]
        l = Listing.objects.get(pk=l_id)
        
        if int(request.POST["watch"]):
            l.watchers.add(user)
        else:
            l.watchers.remove(user)
            
        return HttpResponseRedirect(reverse("listingpage", args=(l.listingID,)))
        
@login_required
def watchlist_view(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "Header": "Watchlist",
        "listing_list": user.watchlist.all()
    })

@login_required
def won_listings_view(request):
    return render(request, "auctions/index.html", {
        "Header": "Won Listings",
        "listing_list": request.user.won_listings.all()
    })

@login_required
def place_comment(request):
    if request.method == "POST":
        l = Listing.objects.get(pk=request.POST["id"])

        comment = Comment(content=request.POST["comment"],
                          listing=l,
                          user = request.user)
        comment.save()

        return HttpResponseRedirect(reverse("listingpage", args=(l.listingID,)))

@login_required
def my_listings_view(request):
    return render(request, "auctions/index.html", {
        "Header": "My Listings",
        "listing_list": request.user.my_listings.all()
    })

def category_listings_view(request, category_name):
    c = Category.objects.get(name=category_name)
    return render(request, "auctions/index.html", {
        "Header": c.name + "'s Listings",
        "listing_list": c.listings_on_this_category.filter(active=True)
    })

def search(request):
    if request.method == "POST":
        searchQuery = request.POST["search"]
        
        listing_list = []
        # Search results among the active listings
        if (active_listings:=Listing.objects.filter(active=True)).exists():
            for l in active_listings:
                if re.match(searchQuery, l.title) is not None:
                    listing_list.append(Listing.objects.get(pk=l.listingID))
        else:
            return render(request, "auctions/index.html", {
                "Header": "There are no more active listings :(",
                "listing_list": listing_list
            })
        
        # If the listing list is not empty then matches were found
        if len(listing_list) != 0:
            return render(request, "auctions/index.html", {
                        "Header": "Results Found",
                        "listing_list": listing_list
                    })
        else:
            return render(request, "auctions/index.html",{
                "Header": "No results found",
                "listing_list": listing_list
            })