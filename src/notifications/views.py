from logging import getLogger

from django.db import connections
from django.db.models import Count, Q
from django.db.utils import OperationalError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from notifications.models import Customer, Message, Mailing
from notifications.utils import ActionSerializerViewSetMixin
from notifications import actions
from notifications import serializers


logger = getLogger('django')


class HealthViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    pagination_class = None

    @action(methods=['GET'], detail=False, url_path='alive')
    def alive(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='ready')
    def ready(self, request, *args, **kwargs):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            c.close()
            return Response(status=status.HTTP_200_OK)


class ConstantsViewSet(viewsets.GenericViewSet):
    constants_list = [
        Message.Status,
    ]

    def list(self, request, *args, **kwargs):
        constants_dict = {
            "CustomerTimezone": dict((x, y) for x, y in Customer.TIMEZONES)
        }
        for constant in self.constants_list:
            attrs_dict = {
                c.name: {'id': c.value, 'label': c.label} for c in constant
            }
            constants_dict.update(
                {constant.__qualname__.replace('.', ''): attrs_dict})

        return Response(constants_dict, status=status.HTTP_200_OK)


class CustomerViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.CustomerSerializer
    filterset_fields = ('timezone',)
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Customer.objects.all()


class CustomerViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.CustomerSerializer
    filterset_fields = ('timezone',)
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Customer.objects.all()

    def create(self, request, *args, **kwargs):
        logger.info(f'create client phone={request.data["phone"]}')
        return super().create(request, *args, **kwargs)

    def update(self, request, pk: int = None, *args, **kwargs):
        logger.info(f'update client with client_id={pk}')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, pk: int = None, *args, **kwargs):
        logger.info(f'destroy client with client_id={pk}')
        actions.RemoveCustomer()(customer_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MailingViewSet(ActionSerializerViewSetMixin,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_classes = {
        ('list', 'retrieve'): serializers.ListMailingSerializer,
        ('create', 'update', 'partial_update'): serializers.MailingSerializer,
        'messages': serializers.ListMessageSerializer
    }

    def get_queryset(self):
        return Mailing.objects.annotate(
            pending=Count('messages', filter=Q(
                messages__status=Message.Status.PENDING)),
            success=Count('messages', filter=Q(
                messages__status=Message.Status.SUCCESS)),
            failure=Count('messages', filter=Q(
                messages__status=Message.Status.FAILURE)),
        ).all()

    @action(methods=['GET'], detail=True)
    def messages(self, request, pk=None, *args, **kwargs):
        messages = Message.objects.select_related('customer').filter(mailing_id=pk)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mailing = serializer.save()
        actions.SendMessages()(mailing_id=mailing.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
