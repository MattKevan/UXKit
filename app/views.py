from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.base import ContentFile
import requests
from django.urls import reverse
from openai import OpenAI

from .models import Persona, ChatMessage
from .forms import PersonaForm

@login_required
def app_home(request):
	personas = Persona.objects.filter(user=request.user)
	return render(request, 'app/home.html', {'personas': personas})


@login_required
def create_persona(request):
    personas = Persona.objects.filter(user=request.user)
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.user = request.user

            # ... rest of your code for DALL-E and saving the image ...

            persona.save()

            return redirect('persona_detail', unique_hash=persona.unique_hash)
        else:
            # If the form is not valid, re-render the page with form errors
            return render(request, 'app/create_persona.html', {'form': form, 'personas': personas})

    # For a GET request, render an empty form
    form = PersonaForm()
    return render(request, 'app/create_persona.html', {'form': form, 'personas': personas})

    
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

			return redirect('persona_detail', unique_hash=persona.unique_hash)
		else:
			# If the form is not valid, re-render the page with form errors
			return render(request, 'app/edit_persona.html', {'form': form, 'personas': personas})

	# For a GET request, render the form with persona instance
	form = PersonaForm(instance=persona)
	return render(request, 'app/edit_persona.html', {'form': form, 'personas': personas, 'persona':persona})


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


@login_required
def persona_profile(request, persona_hash):
	persona = get_object_or_404(Persona, unique_hash=persona_hash, user=request.user)	
	personas = Persona.objects.filter(user=request.user)
	return render(request, 'app/persona_profile.html', {'personas': personas, 'persona': persona})

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
		#lang = request.POST['lang']


		client = OpenAI()
		chat_context = f"Your name is { persona.name }. You are { persona.gender } and { persona.age } years old. Your biography is { persona.bio}. Your needs are { persona.needs }. Your frustrations are { persona.frustrations }. Your goals are { persona.goals } You must always reply in the first person as this person, using their tone of voice. Do not break from this character. You are a real person not an AI assistant."
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
