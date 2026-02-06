from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import ContactForm
from apps.core.utils import send_telegram_notification

class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.status = 'new'
            contact.save()

            send_telegram_notification(
                name=contact.name,
                email=contact.email,
                message=contact.message
            )
            
            messages.success(request, 'Thank you! Your message has been sent successfully. I will get back to you soon.')
            return redirect('home')
        else:
            context = self.get_context_data()
            context['contact_form'] = form
            messages.error(request, 'Oops! Please correct the errors below.')
            return self.render_to_response(context)
