from django.contrib import admin
from django import forms
from events.models import Event

# Register your models here.
class EventsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'id': "richtext_field"}))

    class Meta:
        model = Event
        fields = "__all__"

class EventsAdmin(admin.ModelAdmin):
    form = EventsAdminForm

admin.site.register(Event, EventsAdmin)