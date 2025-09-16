from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email')   # instead of ('username')


#extends the default UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields":("date_of_birth", "profile_photo")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
