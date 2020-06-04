from django.db import models
from accounts.models import CustomUser


class Career_Fair(models.Model):
    """Model representing a career_fair."""
    university = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null = True, blank = True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.university}, {self.date}, {self.time}' 
        
class Career_Booth(models.Model):
	""" Model representing a booth in a career fair"""
	company = models.CharField(max_length=200)
	recruiter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank = True)
	INTERVIEW_DURATION = (
	(4,'Four minutes'),
	(5,'Five minutes'),
	(6,'Six minutes'),
	(7,'Seven minutes'),
	(8,'Eight minutes'),
	(9,'Nine minutes'),
	(10,'Ten minutes'),
	)

	interview_duration = models.CharField(
	max_length=1,
	choices=INTERVIEW_DURATION,
	blank=False,
	default=4,
	help_text='How long do you want every interaction to be? (per student)',
	)
	REST_DURATION = (
	(1,'One minutes'),
	(2,'Two minutes'),
	(3,'Three minutes'),
	(4,'Four minutes'),
	)

	rest_duration = models.CharField(
	max_length=1,
	choices=REST_DURATION,
	blank=False,
	default=2,
	help_text='How long do you need to rest between interactions?',
	)
	time_start = models.TimeField(null = True, blank = True)
	time_end = models.TimeField(null = True, blank = True)
	university = models.CharField(max_length=100)
	career_fair = models.ForeignKey(Career_Fair, on_delete=models.SET_NULL, null=True, blank = True)
	# View detail button would display above information as well as other information they want to include
