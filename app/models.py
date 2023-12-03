from django.db import models
from django.conf import settings
import uuid

# Project model

class Project(models.Model):
	# Project fields
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=400)
	unique_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

	def __str__(self):
		return self.name

# UX canvas model

class LeanUXCanvas(models.Model):
	# Project fields
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	unique_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)

	problem = models.CharField(max_length=500)

	# Business Outcomes
	primary_outcome = models.CharField(max_length=255)
	secondary_outcomes = models.TextField()  # This could be a list, so you might want to serialize it when saving
	# Users and Customers
	primary_users = models.TextField()  # This could also be a list
	secondary_users = models.TextField()  # This could also be a list
	# User Outcomes
	user_outcomes = models.TextField()  # Another list
	# User Problems
	user_problems = models.TextField()  # Another list
	# Solutions
	solution_ideas = models.TextField()  # And another list
	# Hypotheses
	hypotheses = models.TextField()
	# Assumptions
	assumptions = models.TextField()
	# Experiment
	experiment_what_to_test = models.TextField()
	experiment_method = models.TextField()
	experiment_success_metrics = models.TextField()  # List
	# Minimum Viable Product (MVP)
	mvp_actions = models.TextField()  # List
	# Learning and Metrics
	learning_metrics_tracking = models.TextField()

	def __str__(self):
		return self.name

# Persona model

class Persona(models.Model):
	# Gender choices
	MAN = 'Male'
	WOMAN = 'Female'
	NON_BINARY = 'Non-binary'
	GENDER_CHOICES = [
		(MAN, 'Male'),
		(WOMAN, 'Female'),
		(NON_BINARY, 'Non-binary'),
	]

	# User relationship - Personas are linked to the currently logged-in user
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	# Fields for the Persona model
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
	age = models.CharField(max_length=50)
	bio = models.CharField(max_length=250)
	needs = models.CharField(max_length=250, null=True)
	frustrations = models.CharField(max_length=250, null=True)
	goals = models.CharField(max_length=250, null=True)
	unique_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

	def __str__(self):
		return self.name


class ChatMessage(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	user_message = models.TextField()
	chatgpt_response = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Chat with {self.persona.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
