from django.shortcuts import render
from .forms import ContactForm, SingUpForm
from django.core.mail import send_mail
from django.conf import settings
from .models import SingUp
# Create your views here.

def home(request):
	title = "welcome"
	if request.user.is_authenticated():
		title = "My title %s" %(request.user)

	#print request
	#if request.method == "POST":
		#print request.POST
	form = SingUpForm(request.POST or None)#None desaparecer las validaciones
	if form.is_valid():
		instance = form.save(commit=False)# con el commit=False se devolvera un objeto que aun no se ha guardado, en este caso se debe de llamar el metodo save posteriormente
		full_name = form.cleaned_data.get("full_name")#se obtiene un valor enviado del formulario
		#print instance.timestamp
		if not full_name:
			instance.full_name = "Justin"
		instance.save()
		#print instance
		#print instance.email
		#print instance.timestamp
		context = {
			"title": "Success",
			"form": form,
		}		
		return render(request, "home.html", context)

	queryset = SingUp.objects.all().order_by('-timestamp').filter(full_name__icontains="Justin")
	context = {
		"title": title,
		"form": form,
		"queryset":queryset,
	}
	return render(request, "home.html", context)

def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		#instance = form.save(commit=False)
		#print form.cleaned_data
		#for key in form.cleaned_data:
			#print key
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		full_name = form.cleaned_data.get("full_name")

		subject = 'Correo Django'
		form_mail = settings.EMAIL_HOST_USER
		to_mail = form_mail
		contact_message = "%s: %s via %s"%(full_name, message, email)

		send_mail(subject, contact_message, form_mail,[to_mail], fail_silently=False)#see the errors of email

	context = {
		"form": form,
	}
	return render(request, "forms.html", context)