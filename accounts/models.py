from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


def choiceValidator():
	return MinValueValidator(1,message='You have to choose an option')

class FitnessGoal(models.Model):
	name = models.CharField(max_length=200, help_text="Enter a FitnessGoal (e.g. strength, weight lose, ...)")

	def __str__(self):
		"""String for representing the Model object (in Admin site etc.)"""
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	class YesNo(models.IntegerChoices):
		EMPTY = 0, ''
		NO  = 1, "no"
		YES = 2, "yes"

	class TRAINING_DAYS_PER_WEEK(models.IntegerChoices):
		EMPTY 		= 0, ''
		HARD  		= 1, "5 days weekly"
		MODERATE 	= 2, "3-5 days weekly"
		NO 			= 3, "I don\'t train at all"
	
	class NUTRITION(models.IntegerChoices):
		EMPTY 		= 0, ''
		NATURAL		= 1, "Mostly Natural Food"
		PROCESSED 	= 2, "Mostly Processed Food"
		
	"""
	1) Do you exercise? 
	Options: Yes No
	"""
	doesExcercise = models.PositiveSmallIntegerField(
		choices = YesNo.choices,
		default = YesNo.EMPTY,
		verbose_name="Do you exercise?",
		help_text = 'Do you exercise?',
		validators=[choiceValidator()],
	)
	
	"""
	2) How often do you train?
	    Options: More than 5 days weekly, 3-5 days weekly, 1-2 days weekly, I don't train at all
	"""
	weeklyTraining = models.PositiveSmallIntegerField(
		choices=TRAINING_DAYS_PER_WEEK.choices,
		default=TRAINING_DAYS_PER_WEEK.EMPTY,
		verbose_name="Training Interval",
		help_text='How often do you train?',
		validators=[choiceValidator()],
	)

	"""
3)  Click ALL that apply
    My main fitness goals are?
    Options: Endurance
                 Maintain Healthy Weight
                 Strength
                 Gain Muscle
                 Lose Fat
                 Just Overall Wellness
	"""
	fitnessGoals = models.ManyToManyField(
		FitnessGoal,
		help_text="Click ALL that apply! My main fitness goals are?")

	"""
	4) Click the option that best describes your nutrition plan
	   Options: Mostly Natural Food 
	                Mostly Processed Food
	"""
	nutritionPlan = models.PositiveSmallIntegerField(
		choices=NUTRITION.choices,
		default = NUTRITION.EMPTY,
		verbose_name="My Nutrition",
		help_text='Click the option that best describes your nutrition plan',
		validators=[choiceValidator()],
	)
	
	"""
	5) How much sleep do you get?
    Options: 8+ hours
                 5-7 hours
                 4 or less hours
	"""
	sleep = models.SmallIntegerField(
		default=7,
		validators=[MinValueValidator(1),MaxValueValidator(12)],

		verbose_name="Sleep",
		help_text='How much sleep do you get?')

	"""
	6) On a scale of 1 to 10, describe your stress level, with 1 being the least stressed and 10 being highly stressed?
	"""
	stressLevel = models.SmallIntegerField(
		default=5,
		validators=[MinValueValidator(1),MaxValueValidator(10)],

		verbose_name="Stresslevel",
		help_text='On a scale of 1 to 10, describe your stress level, with 1 being the least stressed and 10 being highly stressed?',		
	)

	def __str__(self):
		return self.user.username

	@property
	def complete(self):
		try:
			self.full_clean()
			return True
		except:
			return False

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	profile, created = Profile.objects.get_or_create(user=instance)
	profile.save()
