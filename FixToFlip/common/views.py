from django.shortcuts import render
from django.core.mail import send_mail

from FixToFlip import settings
from FixToFlip.common.forms import ContactUsForm


# Create your views here.
def index(request):
    return render(request, 'common/index.html')


def about_us(request):
    return render(request, 'common/about-us.html')


def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            form_data = {
                'name': name,
                'email': email,
                'message': message,
            }
            message = '''
                    From:\n\t\t{}\n
                    Message:\n\t\t{}\n
                    Email:\n\t\t{}\n
                    '''.format(form_data['name'], form_data['message'], form_data['email'])
            send_mail('Fix To Flip Contact Form!', message, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])

            return render(request, 'common/contact.html', {'success': True})
    else:
        form = ContactUsForm()
    return render(request, 'common/contact.html', {'form': form})


def faq(request):
    return render(request, 'common/faq.html')


