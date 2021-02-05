from decimal import *
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Max
from django.utils import timezone
from .managers import UserManager

# add can buy and can sell
class User(AbstractUser):
    # define fields
    email = models.EmailField('email address', null=True, unique=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now())
    is_admin = models.BooleanField(default=False)
    
    # define required fields
    REQUIRED_FIELDS = ['email']
    
    # set user manager
    objects = UserManager()
    
    def __str__(self):
        return f"{self.username}: {self.profile.first_name} {self.profile.last_name}"

class UserProfile(models.Model):
    # user
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True, related_name='profile')
    # first name
    first_name = models.CharField('first name', unique=False, max_length = 64, null=False)
    # last name
    last_name = models.CharField('last name', unique=False, max_length=64, null=False)
    # watchlist
    # country field
    #https://simpleisbetterthancomplex.com/tutorial/2017/09/26/how-to-create-django-data-migrations.html
    def __str__(self):
        return f"{self.user.username}: {self.first_name} {self.last_name}"


class Listing(models.Model):
    # Eventually upgrade model to use https://github.com/django-money/django-money
    #author - 1 listing; 1 author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #winning bid - bid ID, null if no winner, 1 listing, 1 winning bid
    #image_url
    #title
    title = models.CharField('Listing Title', max_length=64, null=False, default="")
    #description
    description = models.TextField('Listing Description', null=False, default="")
    #date_posted
    date_posted = models.DateTimeField('Date Posted', default=timezone.now(), null=False)
    #date_edited
    #date_edited = models.DateTimeField('Date Edited', default=timezone.now(), null=False)
    #is_open - status
    is_open = models.BooleanField('Open',default=True, null=False)
    #closed date - date closed
    date_closed = models.DateTimeField('Date Closed', default=None, null=True)
    #date_closed = models.DateTimeField('Date Posted', default=None, null=False)
    #min bid - Float value 2 decimals (max bid is 1 million $)
    min_bid = models.DecimalField('Minimum Bid', default=0.00, max_digits=9, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
    #category - 1 listing 1 category
    #tags - 1 listing; many tags
    
    def highest_bid(self):
        bids = self.bids.all()
        if len(bids) != 0:
            amount = bids.aggregate(Max('amount'))
            return bids.get(amount=amount)
        else:
            return None

class Bid(models.Model):
    
    #Listing - Many bids, Many listing
    listing = models.ManyToManyField(Listing, related_name='bids')
    #bidder - 1 bidder per bid
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bids')
    #amount - Float 2 decimals
    amount = models.DecimalField('Bid Amount', max_digits=9, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
    #date bid - DateTime
    date_bid = models.DateTimeField('Date Bid', default=timezone.now(), null=False)
    
    
class Comment():
    #Listing - listing where comments are posted; 1 Listing; Many Comments
    #RootComment - is it threaded - 1 comment; 1 root;
    #Author - User - 1 comment; 1 user
    #content - character
    #date posted / edited
    pass

class Category(models.Model):
    # list of categories with IDs
    name = models.CharField('Category Name', max_length=30, unique=True)
    # sub categories
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    # tags for listing
    name = models.CharField('Tag Name', max_length=30, unique=True)
    

# in order to be able to buy or sell you must have an average rating > 2.5. Anything below and the permissions change for the user. User will have to create a new profile
class Ratings():
    # rated
    # type (sell, buy)
    # ID bid or listing
    # rater
    # rating 1 - 5
    pass
