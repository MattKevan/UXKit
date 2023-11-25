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

def create_persona(request):
	if request.method == 'POST':
		form = PersonaForm(request.POST)
		if form.is_valid():
			persona = form.save(commit=False)
			persona.user = request.user

			# Format the prompt for DALL-E
			prompt = f"A modern stock photo portrait photograph of {persona.name}, {persona.bio}, {persona.get_gender_display()}, age {persona.age}"
			client = OpenAI()
			# Make an API request to OpenAI (DALL-E)
			# Assuming `client` is your configured OpenAI client
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
				# Assuming the image is a PNG
				persona.profile_picture.save(f'{persona.name}_profile.png', ContentFile(response.content), save=True)

			persona.save()

			# Redirect to the newly created persona's detail page
			return redirect('persona_detail', persona_id=persona.id)

	# Fallback for a GET request or invalid form
	return redirect('app_home')


@login_required
def delete_persona(request, persona_id):
	persona = get_object_or_404(Persona, id=persona_id, user=request.user)

	if request.method == 'POST':
		persona.delete()
		# Get the URL of the previous page
		previous_page = request.META.get('HTTP_REFERER')

		# Check if the previous page was the detail page of the deleted persona
		if previous_page and f'/persona/{persona_id}/' not in previous_page:
			return HttpResponseRedirect(previous_page)
		else:
			return redirect('app_home')

	return redirect('app_home')


@login_required
def persona_detail(request, persona_id):

	persona = get_object_or_404(Persona, id=persona_id, user=request.user)
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
		chat_context = f"Your name is { persona.name }. You are { persona.gender } and { persona.age } years old. Your biography is { persona.bio} Answer the user's questions as this person. Do not break character or reveal you are a chatbot."
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
