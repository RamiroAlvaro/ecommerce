from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ContactForm


class IndexView(TemplateView):

    template_name = 'index.html'


def contact(request):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
        form = ContactForm()
    context = {
        'form': form,
        'success': success,
    }
    return render(request, 'contact.html', context)



