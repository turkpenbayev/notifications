import json
from dataclasses import asdict

from rest_framework import serializers

from notifications.models import Customer, Message, Mailing
from notifications.validators import PhoneNumberValidator


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'phone', 'phone_code', 'tag', 'timezone')
        read_only_fields = ('id',)


class ListMessageSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Message
        fields = ('id', 'created_at', 'status', 'customer')
        read_only_fields = fields


class ListMailingSerializer(serializers.ModelSerializer):
    pending = serializers.IntegerField()
    success = serializers.IntegerField()
    failure = serializers.IntegerField()
    filters = serializers.SerializerMethodField()

    class Meta:
        model = Mailing
        fields = ('id', 'start_at', 'end_at', 'text',
                  'filters', 'pending', 'success', 'failure')
        read_only_fields = fields

    def get_filters(self, obj):
        return asdict(obj.filters)


class MailingFilterSerializer(serializers.Serializer):
    phone_code = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class MailingSerializer(serializers.ModelSerializer):
    filters = MailingFilterSerializer()

    class Meta:
        model = Mailing
        fields = ('id', 'start_at', 'end_at', 'text', 'filters',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        filters = validated_data.pop('filters')
        filters['tags'] = list(set(filters['tags']))
        validated_data['filter_by'] = json.dumps(filters)
        instance = super().create(validated_data)
        return instance

    def update(self, instance: Mailing, validated_data):
        filters = validated_data.pop('filters', None)
        if filters is not None:
            tags = filters.get('tags', None)
            filters['tags'] = list(set(tags)) if tags else None
            filters['phone_code'] = filters.get('phone_code', None)
            validated_data['filter_by'] = json.dumps(filters)
        return super().update(instance, validated_data)
