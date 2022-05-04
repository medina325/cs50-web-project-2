# CS50' Web Programming with Python and Javascript - Project 2 - Commerce

## Summary
- [Description](#description)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Submit Version](#submit-version-result)
    - [Active Listings Page](#active-listings-page)
    - [Create Listing Page](#create-listing-page)
    - [Listing Page](#listing-page)
    - [Watchlist Page](#watchlist-page)
    - [My Listings](#my-listings)
    - [Won Listings](#won-listings)

## Description
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Requirements
Taken from the [project's page](https://cs50.harvard.edu/web/2020/projects/2/commerce/).

- **Models**: Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
- **Create Listing**: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
- **Active Listings Page**: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
- **Listing Page**: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    - If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
    - If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    - If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    - If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
    - Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.
- **Watchlist**: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
- **Categories**: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
- **Django Admin Interface**: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

## How to Run
In order to run the app, run the following commands in the root directory of the application.

```bash
    python -m venv .venv            # you can use another virtual environment if you want (e.g.: virtualenv)
    source .venv/Scripts/activate # or source .venv/bin/activate for Linux users
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```

Now just access http://localhost:8000/.

## Submit Version
Here is what the pages required for this project looks like. Since it was halloween season at the time the project was made,
this is how it stayed. Plus there are some extra pages that I took the liberty to add, such as the "My Listings" and "Won Listings",
and also a different approach for the "Categories" page, that I found it better to be a simple dropdown (that required some javascript that I didn't understand back then).

### Active Listings Page
This is the main page that displays all the **active** listings, that means the already won/closed listings won't appear here.

![active listings page](/examples/active_listings.jpg)

### Create Listing Page
The page to create a listing with some optional inputs like the cover image's url (yes that's why some listings shown here 
have no cover image anymore, because the links are down).

![create listing page](/examples/create_listing.jpg)

### Listing Page
The listing page displays information about the current state of the listing: if it's available or it was won by someone, what's the latest bid, comments, etc.

![listing page](/examples/listing.jpg)

### Watchlist Page
The watchlist shows all listings added to the user's watchlist.

![watchlist page](/examples/watchlist.jpg)

### My Listings
This page displays all listings ever created by the user.

![my listing page](/examples/my_listings.jpg)

### Won Listings
And at last, the won listings page display every listing that was won by the current user.
![won listings page](/examples/won_listings.jpg)
