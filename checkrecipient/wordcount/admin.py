from django.contrib import admin

# Register your models here.
from .models import Email, Recipient, Word

admin.site.register(Email)
admin.site.register(Word)
admin.site.register(Recipient)
