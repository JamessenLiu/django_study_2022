from django.contrib import admin
from apps.users.models import Users
from django.contrib.auth.models import User, Group

# admin.site.register(Users)
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    # fields = ['first_name', 'last_name', 'email', 'gender']
    exclude = ['created_at', 'updated_at']
    list_display = ['id', 'first_name', 'last_name', 'email', 'gender']
    search_fields = ['first_name']
    list_filter = ['gender']
    actions = ['change_name']

    def change_name(self, request, queryset):
        for item in queryset:
            item.first_name = 'sb'
            item.save()
