from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment 
# from django.db import models

def index(request):
    return render(request, "auctions/index.html")


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
                    title=request.POST["title"], 
                    description=request.POST["desc"], 
                    # https://stackoverflow.com/questions/12176585/handling-dates-over-request-get
                    creation_date=models.DateTimeField(auto_now_add=True), 
                    img_url=request.POST["image_url"]
                    )
        l.save()

        b = Bid(l, 
                user, 
                request.POST["initial_bid"], 
                models.DateTimeField(auto_now_add=True)
                )
        b.save()

    return render(request, "auctions/index.html")

@login_required
def new_listing_view(request):
    return render(request, "auctions/new_listing.html")
