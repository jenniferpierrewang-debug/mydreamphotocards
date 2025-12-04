from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import Listing, Feedback


# ----------------- ADMIN LISTING -----------------
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('titre', 'groupe', 'membre', 'is_approved', 'approve_button', 'reject_button','consent_given')
    list_filter = ('is_approved', 'groupe','consent_given')
    search_fields = ('titre', 'membre', 'groupe')

    def approve_button(self, obj):
        if not obj.is_approved:
            return format_html(
                '<a class="button" href="{}">Approve</a>',
                f'/admin/marketplace/listing/{obj.id}/approve/'
            )
        return "Approved"
    approve_button.short_description = 'Approve'

    def reject_button(self, obj):
        if obj.is_approved:
            return format_html(
                '<a class="button" href="{}">Reject</a>',
                f'/admin/marketplace/listing/{obj.id}/reject/'
            )
        return "Not approved"
    reject_button.short_description = 'Reject'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:listing_id>/approve/', self.admin_site.admin_view(self.process_approve), name='listing-approve'),
            path('<int:listing_id>/reject/', self.admin_site.admin_view(self.process_reject), name='listing-reject'),
        ]
        return custom_urls + urls

    def process_approve(self, request, listing_id, *args, **kwargs):
        listing = Listing.objects.get(pk=listing_id)
        listing.is_approved = True
        listing.save()
        self.message_user(request, f"Photocard '{listing.titre}' approuvée !")
        return redirect(request.META.get('HTTP_REFERER'))

    def process_reject(self, request, listing_id, *args, **kwargs):
        listing = Listing.objects.get(pk=listing_id)
        listing.is_approved = False
        listing.save()
        self.message_user(request, f"Photocard '{listing.titre}' rejetée !")
        return redirect(request.META.get('HTTP_REFERER'))


# ----------------- ADMIN FEEDBACK -----------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'consent_given', 'is_approved', 'created_at')
    list_filter = ('consent_given', 'is_approved')
    search_fields = ('name', 'message')

from django.contrib import admin
from .models import Listing, Selling, Photocard, Feedback

