from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.base import ContentFile
import requests, json
from django.urls import reverse
from openai import OpenAI

from .models import Persona, ChatMessage, Project, LeanUXCanvas
from .forms import PersonaForm, ProjectForm, LeanUXCanvasForm

# App home

@login_required
def app_home(request):
	personas = Persona.objects.filter(user=request.user)
	return render(request, 'app/home.html', {'personas': personas})

# Projects

# Projects overview
@login_required
def projects(request):
	projects = Project.objects.filter(user=request.user)
	return render(request, 'app/projects/projects.html', {'projects': projects})

# Create project

@login_required
def project_create(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		
		if form.is_valid():
			project = form.save(commit=False)
			project.user = request.user
			project.save()
			return redirect('project_read', project_hash=project.unique_hash)

	else:
		form = ProjectForm()
		return render(request, 'app/projects/create_project.html', {'form': form})
	
	return render(request, 'app/projects/create_project.html', {'form': form})

# View individial project

@login_required
def project_read(request, project_hash):
	project = get_object_or_404(Project, unique_hash=project_hash, user=request.user)
	canvases = LeanUXCanvas.objects.filter(user=request.user, project=project)
	return render(request, 'app/projects/project_detail.html', {'project': project, 'canvases':canvases})

# Delete project
@login_required
def project_delete(request, project_hash):
	if request.method == 'POST':
		project = get_object_or_404(Project, unique_hash=project_hash, user=request.user)
		project.delete()
		return redirect('projects')  # Redirect to the projects list view
	else:
		return redirect('projects')


# Lean UX Canvas

# Lean ux canvas create 
@login_required
def lean_ux_canvas_create(request, project_hash):
	project = get_object_or_404(Project, unique_hash=project_hash, user=request.user)
	if request.method == 'POST':
		form = LeanUXCanvasForm(request.POST)
		
		if form.is_valid():
			problem = form.cleaned_data['problem']
			name = form.cleaned_data['name']
			client = OpenAI()
			prompt = (
				f"Create a Lean UX Canvas in JSON format based on this business problem: '{problem}'. "
					"The response should be structured as follows:\n"
					"{\n"
					"	'PrimaryOutcome': 'A brief description (max 255 characters)',\n"
					"	'SecondaryOutcomes': ['List of outcomes'],\n"
					"	'PrimaryUsers': 'List of primary users',\n"
					"	'SecondaryUsers': ['List of secondary users'],\n"
					"	'UserOutcomes': ['List of user outcomes'],\n"
					"	'UserProblems': ['List of user problems'],\n"
					"	'SolutionIdeas': ['List of solution ideas'],\n"
					"	'Hypotheses': ['List of hypotheses'],\n"
					"	'Assumptions': ['List of assumptions'],\n"
					"	'Experiment': {\n"
					"		'WhatToTest': ['What to test'],\n"
					"		'Method': ['List of methods'],\n"
					"	'SuccessMetrics': ['List of success metrics']\n"
					"	},\n"
					"	'MVPActions': ['List of MVP actions'],\n"
					"	'LearningMetricsTracking': ['List of learning and metrics tracking']\n"
					"}"
			)
			try:
				chatgpt_response = client.chat.completions.create(
					messages=[
						{
							"role": "user",
							"content": prompt,
						}
					],
					model="gpt-3.5-turbo",
				)

				# Parse the response correctly
				data = json.loads(chatgpt_response.choices[0].message.content)

				# Parsing the JSON response
				primary_outcome = data["PrimaryOutcome"]
				secondary_outcomes = json.dumps(data["SecondaryOutcomes"])
				primary_users = data["PrimaryUsers"]
				secondary_users = json.dumps(data["SecondaryUsers"])
				user_outcomes = json.dumps(data["UserOutcomes"])
				user_problems = json.dumps(data["UserProblems"])
				solution_ideas = json.dumps(data["SolutionIdeas"])
				hypotheses = json.dumps(data["Hypotheses"])  # Assuming you want to store this as a JSON string
				assumptions = json.dumps(data["Assumptions"])
				experiment_what_to_test = data["Experiment"]["WhatToTest"]
				experiment_method = data["Experiment"]["Method"]
				experiment_success_metrics = json.dumps(data["Experiment"]["SuccessMetrics"])
				mvp_actions = json.dumps(data["MVPActions"])
				learning_metrics_tracking = json.dumps(data["LearningMetricsTracking"])

				print(primary_outcome)
				# Creating a new LeanUXCanvas instance
				lean_ux_canvas = LeanUXCanvas(
					user = request.user,
					project = project,
					problem=problem,  # Save the business problem
					name=name,
					primary_outcome=primary_outcome,
					secondary_outcomes=secondary_outcomes,
					primary_users=primary_users,
					secondary_users=secondary_users,
					user_outcomes=user_outcomes,
					user_problems=user_problems,
					solution_ideas=solution_ideas,
					hypotheses=hypotheses,
					assumptions=assumptions,
					experiment_what_to_test=experiment_what_to_test,
					experiment_method=experiment_method,
					experiment_success_metrics=experiment_success_metrics,
					mvp_actions=mvp_actions,
					learning_metrics_tracking=learning_metrics_tracking
				)

				print(primary_outcome)
				lean_ux_canvas.save() 

			except Exception as e:
				print(f"Error: {e}")
				return render(request, 'app/projects/project_detail.html', {'project': project})

			return redirect('lean_ux_canvas_read', lean_ux_canvas_hash=lean_ux_canvas.unique_hash)

	else:
		form = LeanUXCanvasForm()
		return render(request, 'app/lean_ux_canvas/lean_ux_canvas_create.html', {'form': form})
	
	return render(request, 'app/lean_ux_canvas/lean_ux_canvas_create.html', {'form': form})

# Lean ux canvas read

@login_required
def lean_ux_canvas_read(request, lean_ux_canvas_hash):
    lean_ux_canvas = get_object_or_404(LeanUXCanvas, unique_hash=lean_ux_canvas_hash, user=request.user)

    # Deserialize JSON fields
    lean_ux_canvas.secondary_outcomes = json.loads(lean_ux_canvas.secondary_outcomes)
    lean_ux_canvas.secondary_users = json.loads(lean_ux_canvas.secondary_users)
    lean_ux_canvas.user_outcomes = json.loads(lean_ux_canvas.user_outcomes)
    lean_ux_canvas.user_problems = json.loads(lean_ux_canvas.user_problems)
    lean_ux_canvas.solution_ideas = json.loads(lean_ux_canvas.solution_ideas)
    lean_ux_canvas.hypotheses = json.loads(lean_ux_canvas.hypotheses)
    lean_ux_canvas.assumptions = json.loads(lean_ux_canvas.assumptions)
    lean_ux_canvas.experiment_success_metrics = json.loads(lean_ux_canvas.experiment_success_metrics)
    lean_ux_canvas.mvp_actions = json.loads(lean_ux_canvas.mvp_actions)
    lean_ux_canvas.learning_metrics_tracking = json.loads(lean_ux_canvas.learning_metrics_tracking)

    context = {'lean_ux_canvas': lean_ux_canvas}

    return render(request, 'app/lean_ux_canvas/read.html', context)

# Lean ux canvas delete

@login_required
def lean_ux_canvas_delete(request, lean_ux_canvas_hash):
	if request.method == 'POST':
		lean_ux_canvas = get_object_or_404(LeanUXCanvas, unique_hash=lean_ux_canvas_hash, user=request.user)
		lean_ux_canvas.delete()
		return redirect('project_read', project_hash=project_hash)
	else:
		return redirect('app_home')



# Personas

# Create persona 
@login_required
def create_persona(request):
	personas = Persona.objects.filter(user=request.user)
	if request.method == 'POST':
		form = PersonaForm(request.POST)
		if form.is_valid():
			persona = form.save(commit=False)
			persona.user = request.user

			# Format the prompt for DALL-E
			prompt = f"A modern stock photo portrait photograph of {persona.name}, {persona.bio}, {persona.gender}, age {persona.age}"
			client = OpenAI()
			# Make an API request to OpenAI (DALL-E)
			response = client.images.generate(
				model="dall-e-3",
				prompt=prompt,
				size="1024x1024",
				quality="standard",
				n=1,
			)
			image_url = response.data[0].url

			# Download the image from the URL
			response = requests.get(image_url)
			if response.status_code == 200:
				# Replace the existing image
				persona.profile_picture.save(f'{persona.name}_profile.png', ContentFile(response.content), save=True)

			persona.save()
			
			return redirect('persona_detail', persona_hash=persona.unique_hash)
		else:
			# If the form is not valid, re-render the page with form errors
			return render(request, 'app/create_persona.html', {'form': form, 'personas': personas})

	# For a GET request, render an empty form
	form = PersonaForm()
	return render(request, 'app/create_persona.html', {'form': form, 'personas': personas})

# Edit persona 
# 	
@login_required
def edit_persona(request, persona_hash):
	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)
	personas = Persona.objects.filter(user=request.user)

	if request.method == 'POST':
		form = PersonaForm(request.POST, instance=persona)
		if form.is_valid():
			persona = form.save(commit=False)

			# Format the prompt for DALL-E
			prompt = f"A modern stock photo portrait photograph of {persona.name}, {persona.bio}, {persona.gender}, age {persona.age}"
			client = OpenAI()
			# Make an API request to OpenAI (DALL-E)
			response = client.images.generate(
				model="dall-e-3",
				prompt=prompt,
				size="1024x1024",
				quality="standard",
				n=1,
			)
			image_url = response.data[0].url

			# Download the image from the URL
			response = requests.get(image_url)
			if response.status_code == 200:
				# Replace the existing image
				persona.profile_picture.save(f'{persona.name}_profile.png', ContentFile(response.content), save=True)

			persona.save()

			return redirect('persona_detail', persona_hash=persona.unique_hash)
		else:
			# If the form is not valid, re-render the page with form errors
			return render(request, 'app/edit_persona.html', {'form': form, 'personas': personas})

	# For a GET request, render the form with persona instance
	form = PersonaForm(instance=persona)
	return render(request, 'app/edit_persona.html', {'form': form, 'personas': personas, 'persona':persona})

# Delete persona 

@login_required
def delete_persona(request, persona_hash):
	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)

	if request.method == 'POST':
		persona.delete()
		# Get the URL of the previous page
		previous_page = request.META.get('HTTP_REFERER')

		# Check if the previous page was the detail page of the deleted persona
		if previous_page and f'/persona/{persona_hash}/' not in previous_page:
			return HttpResponseRedirect(previous_page)
		else:
			return redirect('app_home')

	return redirect('app_home')

# Persona profile

@login_required
def persona_profile(request, persona_hash):
	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)	
	personas = Persona.objects.filter(user=request.user)
	return render(request, 'app/persona_profile.html', {'personas': personas, 'persona': persona})

# Persona chat

@login_required
def persona_detail(request, persona_hash):

	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)
	personas = Persona.objects.filter(user=request.user)

	# Check if the current user is the owner of the persona
	if persona.user != request.user:
		# Option 1: Redirect to another page (e.g., home page)
		return redirect('app_home')

	# Fetch chat messages for this persona
	chat_messages = ChatMessage.objects.filter(persona=persona).order_by('created_at')

	if request.method == "POST":
		user_message = request.POST['user_message']

		client = OpenAI()
		chat_context = f"Your name is { persona.name }. You are { persona.gender } and { persona.age } years old. Your biography is { persona.bio} You are this person and must always reply in the first person, using their tone of voice. Do not break from this or reveal you are not a human. You are a human not an assistant."
		system_prompt = f"{chat_context}\nUser: {user_message}\nAI:"
		try:
			chatgpt_response = client.chat.completions.create(
				messages=[
					{
						"role": "user",
						"content": system_prompt,
					}
				],
				model="gpt-3.5-turbo",
			)

			chatgpt_response = chatgpt_response.choices[0].message.content
			print(user_message)
			print(chatgpt_response)
			
			record = ChatMessage(
				user=request.user, 
				user_message=user_message, 
				chatgpt_response=chatgpt_response, 
				persona=persona
			)
			record.save()
			
			return render(request, 'app/persona_detail.html', {'personas': personas, 'persona': persona, 'user_message':user_message, 'chatgpt_response':chatgpt_response, 'chat_messages': chat_messages})

		except Exception as e:
			 return render(request, 'app/persona_detail.html', {'personas': personas, 'persona': persona, 'user_message':e, 'chatgpt_response':chatgpt_response, 'chat_messages': chat_messages})
	

	return render(request, 'app/persona_detail.html', {'personas': personas, 'persona': persona, 'chat_messages': chat_messages})
