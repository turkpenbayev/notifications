from django.contrib import admin
from django.db.models import Count, Q

from notifications.models import Mailing, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_at', 'end_at', 'pending', 'success', 'failure')

    def pending(self, obj):
        return obj.pending
    pending.admin_order_field  = 'pending'

    def success(self, obj):
        return obj.success
    success.admin_order_field  = 'success'

    def failure(self, obj):
        return obj.failure
    failure.admin_order_field  = 'failure'

    def get_queryset(self, request):
        return Mailing.objects.annotate(
            pending=Count('messages', filter=Q(
                messages__status=Message.Status.PENDING)),
            success=Count('messages', filter=Q(
                messages__status=Message.Status.SUCCESS)),
            failure=Count('messages', filter=Q(
                messages__status=Message.Status.FAILURE)),
        ).all()
