from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url
from .forms import UserProfileForm, CreateListingForm, CreateBidForm
from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html")


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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
            user = request.user
            listing = Listing(author=user, title=title, description=description, min_bid=min_bid)
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
        if button == "Bid":
            form = CreateBidForm(request.POST)
            if form.is_valid():
                print("valid")
                amount = form.cleaned_data.get('amount')
                return redirect('listing', id=id)
            else:
                print("invalid")
                return render_listing(request,id,form)
    print("get")
    return render_listing(request, id, CreateBidForm(initial={'listing':listing, 'bidder':request.user}))
    

def render_listing(request, id, form):
    listing = Listing.objects.get(id=id)
    bids = listing.bids.all()
    last_bid = listing.highest_bid()
    return render(request,"auctions/listing.html", {
        "listing":listing,
        "title": listing.title,
        "author": listing.author,
        "user": request.user,
        "last_bid": last_bid,
        "bid_form": form
    })
