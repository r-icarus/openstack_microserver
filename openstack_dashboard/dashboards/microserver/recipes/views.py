from horizon import views


class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'microserver/recipes/index.html'

    def get_data(self, request, context, *args, **kwargs):    	
        # Add data to the context here...
        context["recipe_types"] = ["Blog","Mail Server", "Wiki", "Project Management"]
        return context


class CreateView(views.APIView):
	# A very simple class-based view...
    template_name = 'microserver/recipes/create_service.html'

    def get_data(self, request, context, *args, **kwargs):    	        
        return context
