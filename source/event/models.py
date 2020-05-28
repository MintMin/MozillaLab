from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from accounts.models import Recruiter, CustomUser, Student

# Create your models here.

# class Type(models.Model):
#     """Model representing a event type."""
#     # name = models.CharField(max_length=50, help_text='Enter a event type (e.g. Infosession)')
#     EVENT_TYPE = (
#         ('Infosession'),
#         ('i','infosession+Interview'),
#         ('Interview Only'),
#         # ('r', 'Reserved'), 
#     )

#     name = models.CharField(
#         max_length=1,
#         choices=EVENT_TYPE,
#         blank=True,
#         default='i',
#         help_text='The type of event',
#     )

#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name


# class Recruiter(models.Model):
#     """Model representing an author."""
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
    

#     class Meta:
#         ordering = ['last_name', 'first_name']

#     def get_absolute_url(self):
#         """Returns the url to access a particular author instance."""
#         return reverse('author-detail', args=[str(self.id)])

#     def __str__(self):
#         """String for representing the Model object."""
#         return f'{self.last_name}, {self.first_name}'

# class Company(models.Model):
#     """Model representing an author."""
#     company_name = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)

#     class Meta:
#         ordering = ['company_name', 'country','city']

#     def get_absolute_url(self):
#         """Returns the url to access a particular author instance."""
#         return reverse('author-detail', args=[str(self.id)])

#     def __str__(self):
#         """String for representing the Model object."""
#         return f'{self.company_name}, {self.city},{self.country}'    


class Event(models.Model):
    """Model representing a event."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    main_recruiter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank = True)
    # additional_recruiters = models.ManyToManyField(Recruiter,related_name = 'otherRecruiters')
    # company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null = True, blank = True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the event')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    
    # typE = models.ManyToManyField(Type, help_text='Select a type for the event')
    absolute_url = models.CharField(max_length=400, blank=True, editable=False)

    rsvp_list = models.ManyToManyField(CustomUser, related_name = 'rsvp_list')

    EVENT_TYPE_CHOICES = (
        ('i','Infosession'),
        ('a','infosession+Interview'),
        ('b','Interview Only'),
        # ('r', 'Reserved'), 
    )

    Event_type = models.CharField(
        max_length=1,
        choices=EVENT_TYPE_CHOICES,
        blank=False,
        default='i',
        help_text='Select a type for the event',
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.title}, {self.date}, {self.main_recruiter}' 
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this event."""  
        return reverse('event-detail', args=[str(self.id)])