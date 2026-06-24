import csv

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import HttpResponse
from django.urls import path

from .models import (Internship, Job, Service, Product, ProductImage,
                     JobApplication, BlogPost, BlogImage, CustomUser,
                     QuestionAndAnswer, Banner)

# Unregister the default Group and User models from the admin
admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'email', 'phone', 'short_message', 'created_at')
    list_filter = ('job_title',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['export_selected_csv']
    change_list_template = 'admin/src/jobapplication/change_list.html'

    @admin.display(description='Message')
    def short_message(self, obj):
        return obj.message[:60] + '…' if len(obj.message) > 60 else obj.message

    def _write_csv(self, queryset, filename='job_applications'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Job Title', 'Email', 'Phone', 'Message', 'Applied On'])
        for obj in queryset:
            writer.writerow([
                obj.name,
                obj.job_title,
                obj.email,
                obj.phone,
                obj.message,
                obj.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        return response

    @admin.action(description='Download selected applications as CSV')
    def export_selected_csv(self, _request, queryset):
        return self._write_csv(queryset)

    def get_urls(self):
        urls = super().get_urls()
        extra = [
            path(
                'export-filtered/',
                self.admin_site.admin_view(self.export_filtered_csv),
                name='src_jobapplication_export_filtered',
            ),
        ]
        return extra + urls

    def export_filtered_csv(self, request):
        queryset = JobApplication.objects.all().order_by('-created_at')

        job_title = request.GET.get('job_title')
        if job_title:
            queryset = queryset.filter(job_title=job_title)

        search = request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(job_title__icontains=search)
            )

        label = job_title or 'all'
        filename = f'job_applications_{label}'.replace(' ', '_').lower()
        return self._write_csv(queryset, filename)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        qs = request.GET.urlencode()
        extra_context['export_filtered_url'] = f'export-filtered/?{qs}' if qs else 'export-filtered/'
        return super().changelist_view(request, extra_context=extra_context)


# Register your models
admin.site.register(Internship)
admin.site.register(Job)
admin.site.register(Service)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(BlogPost)
admin.site.register(BlogImage)
admin.site.register(CustomUser)
admin.site.register(QuestionAndAnswer)
admin.site.register(Banner)




