from django import forms

RECIPE_TYPES = (
    ('mailchimp', 'MailChimp'),
    ('worpress', 'Wordpress'),
    ('sotolitomail', 'SotolitoMail'),
    ('landingpage', 'LandingPage'),
)

class RecipeForm(forms.Form):
    name = forms.CharField(max_length="50",label="Name ")
    recipe_type = forms.ChoiceField(choices=RECIPE_TYPES,label="Type " )
