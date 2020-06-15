from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from accounts.models import Recruiter, CustomUser, Student

class Event(models.Model):
    """Model representing a event."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    main_recruiter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank = True)
    # additional_recruiters = models.ManyToManyField(Recruiter,related_name = 'otherRecruiters')
    # company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null = True, blank = True)
    end_time = models.TimeField(null = True, blank = True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the event')
    join_zoom_url = models.CharField(max_length=1000)
    start_zoom_url = models.CharField(max_length=1000)

    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    
    # typE = models.ManyToManyField(Type, help_text='Select a type for the event')
    absolute_url = models.CharField(max_length=400, blank=True, editable=False)

    rsvp_list = models.ManyToManyField(CustomUser, related_name = 'rsvp_list')

    rsvp_capacity = models.IntegerField(default=0)
    space_open = models.IntegerField(default=-1)


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.title}, {self.date}, {self.main_recruiter}' 
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this event."""  
        return reverse('event-detail', args=[str(self.id)])
