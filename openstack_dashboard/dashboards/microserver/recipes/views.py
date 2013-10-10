from horizon import views
from openstack_dashboard.dashboards.microserver.recipes import forms

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'microserver/recipes/index.html'

    def get_data(self, request, context, *args, **kwargs):    	
        # Add data to the context here...
        context["recipe_types"] = ["Blog","Mail Server", "Wiki", "Project Management"]
        return context


class CreateView(views.APIView):
    template_name = 'microserver/recipes/create.html'

    def get_data(self, request, context, *args, **kwargs): 
        create_form = forms.RecipeForm()
        context["form"] = create_form   	        
        return context

class UpdateView(views.APIView):
    template_name = 'microserver/recipes/update.html'

    def get_data(self, request, context, *args, **kwargs):              
        return context







