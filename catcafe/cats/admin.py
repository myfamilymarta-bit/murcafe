from django.contrib import admin
from .models import Cat, Staff, StaffReview, MenuItem, ContactMessage

admin.site.register(Cat)
admin.site.register(MenuItem)
admin.site.register(StaffReview)
admin.site.register(Staff)
admin.site.register(ContactMessage)
