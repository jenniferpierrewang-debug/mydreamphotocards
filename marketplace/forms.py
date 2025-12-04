from django import forms
from .models import Listing, Selling
from django.utils.translation import gettext_lazy as _

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['titre', 'groupe', 'membre', 'image', 'description', 'consent_given']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': _('Titre de la photocard')}),
            'groupe': forms.TextInput(attrs={'placeholder': _('Groupe')}),
            'membre': forms.TextInput(attrs={'placeholder': _('Membre')}),
            'description': forms.Textarea(attrs={'placeholder': _('Description courte')}),
        }
        labels = {
            'titre': 'Titre / Title',
            'groupe': 'Groupe/Group',
            'membre': 'Membre/Member',
            'consent_given': "Je certifie être le propriétaire ou avoir les droits nécessaires pour publier cette image/"
            "I certify that I own or have the necessary rights to publish this image."
        
    
        }


class SellingForm(forms.ModelForm):
    class Meta:
        model = Selling
        fields = ['listing', 'price']
        widgets = {
            'listing': forms.Select(),
            'price': forms.NumberInput(attrs={'placeholder': 'Prix (€)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Affiche uniquement les listings approuvés
        self.fields['listing'].queryset = Listing.objects.filter(is_approved=True)
        