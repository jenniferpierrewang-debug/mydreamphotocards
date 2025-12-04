from django.urls import path
from . import views

urlpatterns = [
    path('fr/', views.listing_list_fr, name='listings'),  # page principale FR
    path('en/', views.listing_list_en, name='index_en'),      # page principale EN
    path('fr/add/', views.add_listing_fr, name='add_listing_fr'),  # formulaire FR
    path('en/add/', views.add_listing_en, name='add_listing_en'),  # formulaire EN
    path('send-feedback/', views.send_feedback, name='send_feedback'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path('moi/', views.moi, name='moi'),
    path('about_me/',views.about_me,name='about_me'), #page about me anglais
    path('privacy/', views.privacy_policy, name='privacy_policy'),

]
