import json
import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from django.db.models import Q

from auth_custom.types import UserType
from auth_custom.models import CustomUser
from core.schema_helper import get_donate_on_by_info

from .models import Card
from .models import Paypal
from .models import SystemPayment
from .models import PaymentMethods
from .models import Donation
from .models import DonationGoal
from .models import DonationPlan


class CardType(DjangoObjectType):
    class Meta:
        model = Card
        fields = ("id", "card_number", "cardholder_name", "expires_month", "expires_year", "bank_name", "created_at",
                  "updated_at", "is_active")


class PaypalType(DjangoObjectType):
    class Meta:
        model = Paypal
        fields = ("id", "first_name", "last_name", "business", "address_line_1", "address_line_2", "city", "postcode",
                  "mobile_number", "email_address", "created_at", "updated_at", "is_active")


class SystemPaymentType(DjangoObjectType):
    class Meta:
        model = SystemPayment
        fields = ("id", "apple_pay_info", "google_pay_info", "created_at", "updated_at", "is_active",)


class PaymentMethodsType(DjangoObjectType):
    id = graphene.ID()
    card = graphene.Field(CardType)
    paypal = graphene.Field(PaypalType)
    system_payment = graphene.Field(SystemPaymentType)
    primary_method = graphene.String()
    monthly_donate = graphene.String()

    class Meta:
        model = PaymentMethods

    def resolve_card(self, info):
        return self.card

    def resolve_paypal(self, info):
        return self.paypal

    def resolve_system_payment(self, info):
        return self.system_payment


class DonationType(DjangoObjectType):
    class Meta:
        model = Donation


class DonationGoalType(DjangoObjectType):
    class Meta:
        model = DonationGoal


class DonationPlanType(DjangoObjectType):
    class Meta:
        model = DonationPlan


class TopType(ObjectType):
    user = graphene.Field(UserType)
    amount = graphene.Field(graphene.Float)

    class Meta:
        model = Donation


class DonationHistoryType(ObjectType):
    total = graphene.Float()
    top = graphene.List(TopType)

    def resolve_top(self, info):
        enum_key = get_donate_on_by_info(info)

        top_response_list = []
        donation_for_current_donate_on = Donation.objects.filter(donate_on=enum_key).order_by('-amount')

        for donation_object in donation_for_current_donate_on:
            donation_object = Donation.objects.filter(donate_on=enum_key).exclude(
                user_id__in=[top_response.user for top_response in top_response_list]).order_by('-amount').first()
            if donation_object:
                top_response_list.append(TopType(user=donation_object.user_id, amount=donation_object.amount))
            if len(top_response_list) > 4:
                break
        return top_response_list

    def resolve_total(self, info, **args):
        enum_key = get_donate_on_by_info(info)

        donation_objects = Donation.objects.filter(donate_on=enum_key)
        users = [donation.user_id for donation in donation_objects]
        return len(set(users))
