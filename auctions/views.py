from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from django.db import models

def index(request):
    return render(request, "auctions/index.html", {
        "listing_list": Listing.objects.all() 
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
        user = User.objects.get(username=request.user.username)
        l = Listing(created_by=user, 
                    category=request.POST["category_chosen"],
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
        "listing_list": Listing.objects.all()
    })

@login_required
def new_listing_view(request):
    return render(request, "auctions/new_listing.html", {
        "category_list": Category.objects.all()
    })

@login_required
def place_bid(request):
    if request.method == "POST":
        user = request.user
        new_bid = request.POST["new_bid"]
        l = Listing.objects.get(pk=request.POST["id"])
        l.current_bid = new_bid
        l.save()
        
        b = Bid(listing=l,
                user=user,
                price=request.POST["new_bid"]
                )
        b.save()

    return render(request, "auctions/place_bid.html", {
        "listing": Listing.objects.get(pk=l.listingID)
    })

@login_required
def place_bid_view(request, listingID):
    if request.user.watchlist.get(listingID=listingID) is not None:
        flag = True
    else:
        flag = False

    return render(request, "auctions/place_bid.html", {
        "watch_flag": flag,
        "listing": Listing.objects.get(pk=listingID)
    })
    
@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        user = request.user
        l = Listing.objects.get(pk=request.POST["id"])
        l.watchers.add(user)
        return render(request, "auctions/place_bid.html", {
            "flag": True,
            "listing": l
        })

@login_required
def remove_from_watchlist(request):
    if request.method == "POST":
        user = request.user
        l = Listing.objects.get(pk=request.POST["id"])
        l.watchers.remove(user)
        return render(request, "auctions/place_bid.html", {
            "flag": False,
            "listing": l
        })

@login_required
def watchlist_view(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "Header": "Watchlist",
        "listing_list": user.watchlist.all()
    })

@login_required
def category_listings_view(request, category_name):
    c = Category.objects.get(name=category_name)
    return render(request, "auctions/index.html", {
        "Header": c.name + "'s Listings",
        "listing_list": c.listings_on_this_category.all()
    })
