from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf.urls import handler404
from django.http import HttpResponseRedirect, Http404
from .forms import ShortenerForm
from .models import ShortenedURL  # Assuming you have a model to store the shortened URLs
from urllib.parse import quote
from django.utils.translation import gettext as _


def shorten_url(request):
    form = ShortenerForm()
    errors = None

    if request.method == "POST":
        form = ShortenerForm(request.POST)
        if form.is_valid():
            new_url = form.save()  # Logic to save the new shortened URL
            encoded_long_url = quote(form.cleaned_data['long_url'])  # URL encode the long URL
            messages.success(
                request, 
                _('Your URL has been shortened successfully!\n You can access it at: ') 
                + str(new_url.short_url)
            )

            return redirect('/', new_url=new_url.short_url, long_url=encoded_long_url)
        else:
            errors = form.errors

    recent_urls = ShortenedURL.objects.all().order_by('-created')[:5]
    context = {'form': form, 'errors': errors, 'recent_urls': recent_urls}
    return render(request, 'urlshortener/shortener_form.html', context)

def shorten_list(request):
    # Retrieve all shortened URLs from the database
    shortened_urls = ShortenedURL.objects.all()
    
    # Pass the list to the template
    context = {
        'shortened_urls': shortened_urls,
    }
    return render(request, 'urlshortener/shorten_list.html', context)

def redirect_url_view(request, shortened_part):

    try:
        shortener = ShortenedURL.objects.get(short_url=shortened_part)

        shortener.times_followed += 1        

        shortener.save()
        
        return HttpResponseRedirect(shortener.long_url)
        
    except ShortenedURL.DoesNotExist:
        return render(request, 'urlshortener/404.html', status=404)
    
# Custom 404 view
def custom_404(request, exception):
    return render(request, 'urlshortener/404.html', status=404)


handler404 = 'urlshortener.views.custom_404'