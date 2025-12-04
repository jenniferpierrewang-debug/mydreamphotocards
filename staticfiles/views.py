from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from collections import OrderedDict
from django.utils import translation

from .models import Listing, Selling, Feedback
from .forms import ListingForm, SellingForm


# ----------------- LISTINGS -----------------
def listing_list_fr(request):
    query = request.GET.get('q', '')
    selected_group = request.GET.get('groupe', '')

    listings = Listing.objects.filter(is_approved=True)

    if query:
        listings = listings.filter(
            Q(titre__icontains=query) |
            Q(groupe__icontains=query) |
            Q(membre__icontains=query)
        )

    if selected_group:
        listings = listings.filter(groupe__iexact=selected_group)

    groups = sorted(['BOYNEXTDOOR','SEVENTEEN','TXT','ENHYPEN','STRAY KIDS','XDH','AESPA','NCT','CORTIS','TWICE','MEOV','BLACKPINK','THE BOYZ'])
    grouped_listings = OrderedDict()
    for group_name in groups:
        grouped_listings[group_name] = listings.filter(groupe__iexact=group_name)

    sellings = Selling.objects.filter(is_active=True)
    feedbacks = Feedback.objects.filter(is_approved=True, consent_given=True).order_by('-created_at')

    return render(request, 'marketplace/listings.html', {
        'listings': listings,
        'selected_group': selected_group,
        'groups': groups,
        'sellings': sellings,
        'grouped_listings': grouped_listings,
        'feedbacks': feedbacks,
    })


def listing_list_en(request):
    query = request.GET.get('q', '')
    selected_group = request.GET.get('groupe', '')

    listings = Listing.objects.filter(is_approved=True)

    if query:
        listings = listings.filter(
            Q(titre__icontains=query) |
            Q(groupe__icontains=query) |
            Q(membre__icontains=query)
        )

    if selected_group:
        listings = listings.filter(groupe__iexact=selected_group)

    groups =['BOYNEXTDOOR','SEVENTEEN','TXT','ENHYPEN','STRAY KIDS','XDH','AESPA']
    
    grouped_listings = OrderedDict()
    for group_name in groups:
        grouped_listings[group_name] = listings.filter(groupe__iexact=group_name)

    sellings = Selling.objects.filter(is_active=True)
    feedbacks = Feedback.objects.filter(is_approved=True, consent_given=True).order_by('-created_at')

    return render(request, 'marketplace/en/listings_list_en.html', {
        'listings': listings,
        'selected_group': selected_group,
        'groups': groups,
        'sellings': sellings,
        'grouped_listings': grouped_listings,
        'feedbacks': feedbacks,
    })



# ----------------- AJOUTER UNE LISTING -----------------
from django.shortcuts import render, redirect
from django.utils import translation
from django.contrib import messages
from .forms import ListingForm

def add_listing_fr(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.is_approved = False
            listing.save()
            messages.success(request, "Votre photocard a été bien envoyée. L’admin va la vérifier et la valider si cela respecte les conditions.")
            
            # Redirection selon la langue
            current_lang = translation.get_language()
            if current_lang == 'en':
                return redirect('index_en')
            else:
                return redirect('listings')
    else:
        form = ListingForm()

    return render(request, 'marketplace/add_listing.html', {'form': form})

def add_listing_en(request):
    submitted = False
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.is_approved = False
            listing.save()
            submitted = True
            form = ListingForm()
    else:
        form = ListingForm()
    return render(request, 'marketplace/en/add_listing.html', {'form': form, 'submitted': submitted})


# ----------------- VENTES -----------------
@login_required
def selling_list(request):
    sellings = Selling.objects.filter(is_active=True)
    return render(request, 'marketplace/selling.html', {'sellings': sellings})


@login_required
def add_selling(request):
    if request.method == 'POST':
        form = SellingForm(request.POST)
        if form.is_valid():
            selling = form.save(commit=False)
            selling.seller = request.user
            selling.save()
            return redirect('selling_list')
    else:
        form = SellingForm()
    return render(request, 'marketplace/add_selling.html', {'form': form})


# ----------------- FEEDBACK -----------------
def send_feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        consent = request.POST.get('consent') == 'on'
        message_text = request.POST.get('message')

        Feedback.objects.create(
            name=name,
            message=message_text,
            consent_given=consent
        )
        messages.success(request, "Merci pour votre retour ! Votre message a bien été enregistré 💌")

    current_lang = translation.get_language()
    if current_lang == 'en':
        return redirect('index_en')
    else:
        return redirect('listings')


# ----------------- AUTRES PAGES -----------------
def mentions_legales(request):
    return render(request, 'marketplace/fr/mentions_legales.html')

def moi(request):
    return render(request, 'marketplace/moi.html')
def about_me(request):
    return render(request, 'marketplace/en/about_me.html')

from django.shortcuts import render, redirect

from .models import Photocard

def get_client_ip(request):
    """Récupère l'IP du client pour garder une preuve du consentement"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def privacy_policy(request):
    return render(request, 'marketplace/fr/privacy_policy.html', {
        'last_update': '03/12/2025',  # tu peux mettre la date du jour
        'contact_email': 'contact@tonsite.com'
    })
