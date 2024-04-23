from django.db import models
from django.conf import settings
from decimal import Decimal


class Restriction(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.description


class TrickDefinition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default= '', null=True, blank=True)
    has_orientation = models.BooleanField(default=False)
    reverse_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    twisted_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    twisted_exit_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    flipped_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    double_flipped_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    devil_twist_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    cab_slide_bonus = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    restrictions = models.ManyToManyField(Restriction, blank=True, default=None)

    def __str__(self):
        return self.name


class Run(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="runs"
    )
    date = models.DateField()
    time = models.TimeField()
    wing = models.CharField(max_length=100, null=True, default=None)
    site = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return str(self.date) + " " + str(self.time)


class TrickInstance(models.Model):
    trick_definition = models.ForeignKey(TrickDefinition, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="tricks")
    right = models.BooleanField(default=False, null=True)
    reverse = models.BooleanField(default=False, null=True)
    twisted = models.BooleanField(default=False, null=True)
    twisted_exit = models.BooleanField(default=False, null=True)
    flipped = models.BooleanField(default=False, null=True)
    double_flipped = models.BooleanField(default=False, null=True)
    devil_twist = models.BooleanField(default=False, null=True)
    cab_slide = models.BooleanField(default=False, null=True)
    successful = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.trick_definition.name
