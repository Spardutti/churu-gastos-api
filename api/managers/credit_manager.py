from django.db import models
from django.utils import timezone
from django.db.models import F
from dateutil.relativedelta import relativedelta

class CreditManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        base_queryset = super().get_queryset()

        # 1. Update is_active to True for credits where the month matches and they are not already active
        updated_credits = base_queryset.filter(
            next_payment_date__year=now.year,
            next_payment_date__month=now.month
        )

        # Iterate over the credits to calculate the new next_payment_date
        for credit in updated_credits:
            new_next_payment_date = credit.next_payment_date + relativedelta(months=1)
            if credit.payments_made < credit.number_of_payments:
                credit.is_active = True
                credit.payments_made += 1
                credit.next_payment_date = new_next_payment_date
                credit.save(update_fields=['is_active', 'payments_made', 'next_payment_date'])


        # 2. Update is_active to False for credits where payments_made is equal to the number_of_payments
        base_queryset.filter(
            payments_made=F('number_of_payments'),
            next_payment_date__lt=now  # Checks if the next_payment_date is before the current date/time
        ).update(is_active=False)

        # Return the base queryset with additional annotations if needed
        return base_queryset.annotate(
            is_current=models.Case(
                models.When(
                    next_payment_date__year=now.year,
                    next_payment_date__month=now.month,
                    payments_made__lt=F('number_of_payments'),
                    then=True
                ),
                default=False,
                output_field=models.BooleanField()
            )
        )
