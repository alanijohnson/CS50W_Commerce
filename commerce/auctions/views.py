from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import is_safe_url
from .forms import UserProfileForm, CreateListingForm, CreateBidForm, CreateCommentForm
from .models import User, Listing, Bid, Comment


def index(request):
    active_listings = Listing.objects.filter(is_open=True).order_by('-date_posted')
    active_listings_dict = {listing: (len(listing.bids.all()),listing.highest_bid()) for listing in active_listings}
    return render(request, "auctions/index.html",{
        "active_listings": active_listings_dict
    })


def login_view(request):
    print(f"{request.path}")
    next_url = request.GET.get('next')
    print(f"{next_url}")
    if not valid_next_url(next_url, request.get_host()):
        next_url = "/"
    
    if request.method == "POST":
        next_url = request.POST.get("next")
        print(f"{next_url}")
        if not valid_next_url(next_url, request.get_host()):
            next_url = "/"
            
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {
            "next_url":next_url
                      })

# method to validate the login redirect URL
def valid_next_url(next, allowed_hosts):
    # next may be None because the page may have been reached directly
    if next is None:
        return False
    # return whether or not the url is safe to access
    return is_safe_url(
        url=next, allowed_hosts=allowed_hosts
    )

def logout_view(request):
    next_url = request.GET.get('next')
    if not valid_next_url(next_url, request.get_host()):
        next_url = 'index'
    logout(request)
    return redirect(next_url)


def register(request):
    if request.method == "POST":
        
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
        
        else:
                return render(request, "auctions/register.html", {
                "message": "Failed to create Account."
            })
        
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
            profile.user = user
            profile.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        profile_form = UserProfileForm
        return render(request, "auctions/register.html",{
            "profile_form": profile_form
        })
        
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
               
        if form.is_valid():
            # get the user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            min_bid = form.cleaned_data["min_bid"]
            category = form.cleaned_data["category"]
            user = request.user
            listing = Listing(author=user, title=title, description=description, min_bid=min_bid, category=category)
            listing.save()
            
            return redirect('listing', listing.id)
        
        else:
            return render(request,"auctions/create_listing.html",{
                'form': form
            })
    else:
        return render(request,"auctions/create_listing.html",{
            'form': CreateListingForm()
        })
        

def listing(request, id):
    listing = Listing.objects.get(id=id)
    # form posted from listing page
    if request.method == "POST":
        # multiple buttons on page. Determine which was clicked
        button = request.POST.get("button")
        bid_form = CreateBidForm(request.POST)
        comment_form = CreateCommentForm(request.POST)
        if button == "Bid":
            if bid_form.is_valid():
                amount = bid_form.cleaned_data.get('amount')
                bid = Bid(amount=amount, bidder=request.user)
                bid.save()
                listing.bids.add(bid)
                return redirect('listing', id=id)
                
        elif button == "Close Listing":
            listing.is_open = False
            listing.date_closed = timezone.now()
            listing.save()
            print(f"Closed Listing: Listing {listing.is_open}")
            return render_listing(request,id,None, None)
            
        elif button == "Submit Comment":
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                comment = Comment(content=content, author=request.user, listing=listing)
                comment.save()
                return redirect('listing',id=id)
                
        elif button == "Add to Watchlist":
            request.user.profile.watchlist.add(listing)
            #request.user.profile.save()
            return redirect('listing', id=id)
            
        elif button == "Remove from Watchlist":
            print("Remove Listing")
            request.user.profile.watchlist.remove(listing)
            request.user.profile.save()
            return redirect('listing', id=id)
                
        # return if button was clicked but no forms were valid
        return render_listing(request, id, bid_form, comment_form)
    
    comment_form = None
    if listing.is_open == True:
        comment_form = CreateCommentForm(initial={'listing':listing, 'author':request.user})
    return render_listing(request, id, CreateBidForm(initial={'listing':listing, 'bidder':request.user}), comment_form)
    
    

def render_listing(request, id, bid_form, comment_form):
    listing = Listing.objects.get(id=id)
    bids = listing.bids.all()
    highest_bid = listing.highest_bid()
    user_watchlist = None
    if request.user.is_authenticated:
            user_watchlist = request.user.profile.watchlist.all()
            
    return render(request,"auctions/listing.html", {
        "listing":listing,
        "title": listing.title,
        "author": listing.author,
        "user": request.user,
        "last_bid": highest_bid,
        "bid_form": bid_form,
        "bids": bids,
        "comment_form": comment_form,
        "comments":listing.get_comments(),
        "user_watchlist":user_watchlist
    })

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('index')
        
    watchlist = user.profile.watchlist.all()
    watchlist_dict = {listing: (len(listing.bids.all()), listing.highest_bid()) for listing in watchlist}
    active_listings = Listing.objects.filter(author=user.id, is_open=True).order_by('-date_posted')
    active_listings_dict = {listing: (len(listing.bids.all()),listing.highest_bid) for listing in active_listings}
    closed_listings = Listing.objects.filter(author=user.id, is_open=False).order_by('-date_posted')
    closed_listings_dict = {listing: listing.highest_bid() for listing in closed_listings}
    
    print(f"{watchlist_dict}")
    print(f"{listing in watchlist}")
    
    
    return render(request, "auctions/profile.html",{
        "current_user": request.user,
        "profile_user": user,
        "active_listings": active_listings_dict,
        "closed_listings": closed_listings_dict,
        "watchlist": watchlist_dict
    })
