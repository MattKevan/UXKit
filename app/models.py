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
	name = models.CharField(max_length=200)

	lean_problem = models.CharField(max_length=500)
	# Business outcomes
	lean_outcomes = models.TextField()
	# Users and customers
	lean_users = models.TextField()
	# User outcomes
	lean_user_outcomes = models.TextField()
	# User solutions
	lean_solutions = models.TextField()
	# Hypotheses
	lean_hypotheses = models.TextField()
	# Assumptions
	lean_assumptions = models.TextField()
	# Experiment
	lean_experiments = models.TextField()

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
