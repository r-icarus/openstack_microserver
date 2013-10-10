from horizon import views
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from openstack_dashboard.dashboards.microserver.recipes import forms

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'microserver/recipes/index.html'

    def get_data(self, request, context, *args, **kwargs):    	
        context["recipe_types"] = ["Blog","Mail Server", "Wiki", "Project Management"]
        return context


class CreateView(views.APIView):
    template_name = 'microserver/recipes/create.html'

    def get_data(self, request, context, *args, **kwargs):     
        create_form = forms.RecipeForm()
        context["form"] = create_form   	        
        return context

    def post(self, request, *args, **kwargs ):
        context = self.get_context_data(**kwargs)    
        create_form = forms.RecipeForm(request.POST)
        if create_form.is_valid():
            return HttpResponseRedirect(reverse("horizon:microserver:hypervisors:index")) # Redirect after POST
        else:
            create_form = forms.RecipeForm()
            context["form"] = create_form
            return self.render_to_response(context)


class UpdateView(views.APIView):
    template_name = 'microserver/recipes/update.html'

    def get_data(self, request, context, *args, **kwargs): 
        context['form'] = forms.RecipeForm()             
        return context

    def post(self, request, *args, **kwargs ):
        context = self.get_context_data(**kwargs)    
        create_form = forms.RecipeForm(request.POST)
        if create_form.is_valid():
            return HttpResponseRedirect(reverse("horizon:microserver:hypervisors:index")) # Redirect after POST
        else:
            create_form = forms.RecipeForm()
            context["form"] = create_form
            return self.render_to_response(context)