from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.base import ContentFile
import requests, json
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)
from .models import Persona, ChatMessage, Project, LeanUXCanvas
from .forms import PersonaForm, ProjectForm, LeanUXCanvasForm, LeanUXCanvasEditForm

# App home

@login_required
def app_home(request):
	projects = Project.objects.filter(user=request.user)
	personas = Persona.objects.filter(user=request.user)
	return render(request, 'app/home.html', {'personas': personas, 'projects':projects})

# Projects

# Projects overview
@login_required
def projects(request):
	projects = Project.objects.filter(user=request.user)
	personas = Persona.objects.filter(user=request.user)

	return render(request, 'app/projects/projects.html', {'personas': personas, 'projects': projects})

# Create project
@login_required
def project_create(request):
	personas = Persona.objects.filter(user=request.user)

	if request.method == 'POST':
		form = ProjectForm(request.POST)
		
		if form.is_valid():
			project = form.save(commit=False)
			project.user = request.user
			project.save()
			return redirect('project_read', project_hash=project.unique_hash)

	else:
		form = ProjectForm()
		return render(request, 'app/projects/create_project.html', {'form': form,'personas': personas, })
	
	return render(request, 'app/projects/create_project.html', {'form': form,'personas': personas, })

# View individial project
@login_required
def project_read(request, project_hash):
	projects = Project.objects.filter(user=request.user)
	personas = Persona.objects.filter(user=request.user)
	project = get_object_or_404(Project, unique_hash=project_hash, user=request.user)
	canvases = LeanUXCanvas.objects.filter(user=request.user, project=project)
	return render(request, 'app/projects/project_detail.html', {'personas': personas, 'projects': projects, 'project': project, 'canvases':canvases})

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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from .forms import LeanUXCanvasForm
from .models import Project, LeanUXCanvas
from openai import OpenAI

@login_required
def lean_ux_canvas_create(request, project_hash):
	project = get_object_or_404(Project, unique_hash=project_hash, user=request.user)
	personas = Persona.objects.filter(user=request.user)
	
	if request.method == 'POST':
		form = LeanUXCanvasForm(request.POST)
		if form.is_valid():
			lean_problem = form.cleaned_data['lean_problem']
			name = form.cleaned_data['name']

			prompt = (
				f"Create a Lean UX Canvas in JSON format based on this business problem: '{lean_problem}'.\n"
				"The response should be structured in JSON as follows and include a list of at least four items for each section:\n"
				"{\n"
				"   'BusinessOutcomes': [],\n"
				"   'Users': [],\n"
				"   'UserOutcomes': [],\n"
				"   'Solutions': [],\n"
				"   'Hypotheses': [],\n"
				"   'Assumptions': [],\n"
				"   'Experiments': []\n"
				"}"
			)

			try:
				client = OpenAI()  # Ensure API keys and other parameters are set correctly
				chatgpt_response = client.chat.completions.create(
					messages=[
						{"role": "user", "content": prompt},
					],
					model="gpt-3.5-turbo",
				)

				# Verify and parse the response
				response_content = chatgpt_response.choices[0].message.content
				if response_content:
					data = json.loads(response_content)

					# Process each list into a formatted string
					def list_to_string(lst):
						return '\n'.join(lst) if isinstance(lst, list) else ''

					# Creating a new LeanUXCanvas instance
					lean_ux_canvas = LeanUXCanvas(
						user=request.user,
						project=project,
						name=name,
						lean_problem=lean_problem,
						lean_outcomes=list_to_string(data.get("BusinessOutcomes", [])),
						lean_users=list_to_string(data.get("Users", [])),
						lean_user_outcomes=list_to_string(data.get("UserOutcomes", [])),
						lean_solutions=list_to_string(data.get("Solutions", [])),
						lean_hypotheses=list_to_string(data.get("Hypotheses", [])),
						lean_assumptions=list_to_string(data.get("Assumptions", [])),
						lean_experiments=list_to_string(data.get("Experiments", []))
					)
					lean_ux_canvas.save()

					return redirect('lean_ux_canvas_read', lean_ux_canvas_hash=lean_ux_canvas.unique_hash)
				else:
					raise ValueError("Empty response from OpenAI")

			except Exception as e:
				print(f"Error: {e}")
				return render(request, 'app/projects/project_detail.html', {'project': project, 'error': str(e)})
		else:
			return render(request, 'app/lean_ux_canvas/lean_ux_canvas_create.html', {'form': form, 'project': project, 'personas': personas, })

	else:
		form = LeanUXCanvasForm()
	
	return render(request, 'app/lean_ux_canvas/lean_ux_canvas_create.html', {'form': form, 'project': project, 'personas': personas, })

# Lean ux canvas read

@login_required
def lean_ux_canvas_read(request, lean_ux_canvas_hash):
	projects = Project.objects.filter(user=request.user)
	personas = Persona.objects.filter(user=request.user)
	lean_ux_canvas = get_object_or_404(LeanUXCanvas, unique_hash=lean_ux_canvas_hash, user=request.user)

	project = lean_ux_canvas.project

	# Convert the text fields back to lists for display
	lean_ux_canvas.lean_outcomes = lean_ux_canvas.lean_outcomes.split('\n') if lean_ux_canvas.lean_outcomes else []
	lean_ux_canvas.lean_users = lean_ux_canvas.lean_users.split('\n') if lean_ux_canvas.lean_users else []
	lean_ux_canvas.lean_user_outcomes = lean_ux_canvas.lean_user_outcomes.split('\n') if lean_ux_canvas.lean_user_outcomes else []
	lean_ux_canvas.lean_solutions = lean_ux_canvas.lean_solutions.split('\n') if lean_ux_canvas.lean_solutions else []
	lean_ux_canvas.lean_hypotheses = lean_ux_canvas.lean_hypotheses.split('\n') if lean_ux_canvas.lean_hypotheses else []
	lean_ux_canvas.lean_assumptions = lean_ux_canvas.lean_assumptions.split('\n') if lean_ux_canvas.lean_assumptions else []
	lean_ux_canvas.lean_experiments = lean_ux_canvas.lean_experiments.split('\n') if lean_ux_canvas.lean_experiments else []

	context = {
		'personas': personas, 
		'projects': projects, 
		'lean_ux_canvas': lean_ux_canvas,
		'project': project  # Add the project to the context
		}
	 
	return render(request, 'app/lean_ux_canvas/read.html', context)

# Lean ux canvas edit 
@login_required
def lean_ux_canvas_edit(request, lean_ux_canvas_hash):
	lean_ux_canvas = get_object_or_404(LeanUXCanvas, unique_hash=lean_ux_canvas_hash, user=request.user)
	personas = Persona.objects.filter(user=request.user)

	if request.method == 'POST':
		form = LeanUXCanvasEditForm(request.POST, instance=lean_ux_canvas)
		if form.is_valid():
			form.save()
			return redirect('lean_ux_canvas_read', lean_ux_canvas_hash=lean_ux_canvas.unique_hash)
	else:
		form = LeanUXCanvasEditForm(instance=lean_ux_canvas)

	return render(request, 'app/lean_ux_canvas/lean_ux_canvas_edit.html', {'form': form, 'lean_ux_canvas': lean_ux_canvas, 'personas': personas, })
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
	projects = Project.objects.filter(user=request.user)
	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)
	personas = Persona.objects.filter(user=request.user)

	if persona.user != request.user:
		return redirect('app_home')

	chat_messages = ChatMessage.objects.filter(persona=persona).order_by('created_at')

	context = {
		'projects': projects, 
		'personas': personas, 
		'persona': persona, 
		'chat_messages': chat_messages
	}

	return render(request, 'app/persona_detail.html', context)


@login_required
def send_message(request, persona_hash):
	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)
	personas = Persona.objects.filter(user=request.user)
	if request.method == "POST" and request.headers.get('HX-Request', 'false') == 'true':
		user_message = request.POST.get('user_message')

		client = OpenAI()
		chat_context = f"Your name is { persona.name }. You are { persona.gender } and { persona.age } years old. Your biography is { persona.bio}. Your needs are { persona.needs }. Your frustrations are { persona.frustrations }. Your goals are { persona.goals } You must always reply in the first person as this person, using their tone of voice. Do not break from this character. You are a real person not an AI assistant."
		system_prompt = f"{chat_context}\nUser: {user_message}\nAI:"

		try:
			chatgpt_response = client.chat.completions.create(
				messages=[{"role": "user", "content": system_prompt}],
				model="gpt-3.5-turbo",
			)
			chatgpt_response = chatgpt_response.choices[0].message.content

			record = ChatMessage(
				user=request.user, 
				user_message=user_message, 
				chatgpt_response=chatgpt_response, 
				persona=persona
			)
			record.save()

			# Returning only the new message part
			return render(request, 'app/personas/chat_partial.html', {'message': record, 'persona':persona, 'personas':personas})

		except Exception as e:
			# Handle the exception (you might want to log this or handle it differently)
			logger.error(f"Error in send_message: {str(e)}")
			return HttpResponse(f"An error occurred while processing your message: {str(e)}")

	return HttpResponse("Invalid request.", status=400)