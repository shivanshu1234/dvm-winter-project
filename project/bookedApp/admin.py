from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile, Report
from django.http import HttpResponseRedirect

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Report)

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'email']
    ordering = ['username']
    actions = ['generate_excel_sheet']

    def generate_excel_sheet(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/bookedApp/GenerateExcelSheet/%s" % ('-'.join(selected)))

    generate_excel_sheet.short_description = "Get data of selected users in an excel sheet."

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
    