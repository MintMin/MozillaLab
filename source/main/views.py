from django.views.generic import TemplateView

class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


from django.shortcuts import render
from search.models import Event
from django.views.generic import ListView

# def index(request):
#     """View function for home page of site."""

#     # Generate counts of some of the main objects
#     events = Event.objects.all()
#     # num_instances = BookInstance.objects.all().count()
    
#     # Available books (status = 'a')
#     # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
#     # # The 'all()' is implied by default.    
#     # num_authors = Author.objects.count()
    
#     context = {
#         'events': events,
        
#     }

    
#     # Render the HTML template index.html with the data in the context variable
#     return render(request, 'index.html', context=context)


class EventList(ListView):
        model = Event
        context_object_name = 'event_list'   # your own name for the list as a template variable
        queryset = Event.objects.all()  # Get 5 books containing the title war
        template_name = 'main/index.html'  # Specify your own template name/location
