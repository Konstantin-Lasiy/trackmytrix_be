from django.contrib import admin
from .models import Run, TrickInstance, TrickDefinition, Restriction
from django import forms
from decimal import Decimal


class TrickDefinitionInline(admin.TabularInline):
    model = TrickDefinition
    extra = 1  # Defines how many blank forms are displayed by default.
    fields = [
        "name",
        "id",
        "has_orientation",
        "reverse_bonus",
        "twisted_bonus ",
        "twisted_exit_bonus",
        "flipped_bonus",
        "double_flipped_bonus",
        "devil_twist_bonus",
        "cab_slide_bonus",
    ]


class TrickInstanceForm(forms.ModelForm):
    class Meta:
        model = TrickInstance
        exclude = []


class TrickInstanceInline(admin.TabularInline):
    model = TrickInstance
    extra = 1

    def get_exclude(self, request, obj=None, **kwargs):
        excluded_fields = super().get_exclude(request, obj, **kwargs) or []
        if obj:
            for trick_instance in obj.tricks.all():
                trick_def = trick_instance.trick_definition
                if not trick_def.has_orientation:
                    excluded_fields.append("orientation")
                if trick_def.reverse_bonus == Decimal("0.00"):
                    excluded_fields.append("reverse")
                if trick_def.twisted_bonus == Decimal("0.00"):
                    excluded_fields.append("twisted")
                if trick_def.twisted_exit_bonus == Decimal("0.00"):
                    excluded_fields.append("twisted_exit")
                if trick_def.flipped_bonus == Decimal("0.00"):
                    excluded_fields.append("flipped")
                if trick_def.double_flipped_bonus == Decimal("0.00"):
                    excluded_fields.append("double_flipped")
                if trick_def.devil_twist_bonus == Decimal("0.00"):
                    excluded_fields.append("devil_twist")
                if trick_def.cab_slide_bonus == Decimal("0.00"):
                    excluded_fields.append("cab_slide")
        return list(set(excluded_fields))  # Use set to eliminate any duplicates


class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = "__all__"  # Include all fields

    def __init__(self, *args, **kwargs):
        super(RunForm, self).__init__(*args, **kwargs)
        self.fields["wing"].required = False  # Make 'wing' not required
        self.fields["site"].required = False  # Make 'site' not required


class RunAdmin(admin.ModelAdmin):
    form = RunForm
    list_display = ("date", "time", "wing", "site", "user")
    inlines = [TrickInstanceInline]


admin.site.register(Run, RunAdmin)
admin.site.register(Restriction)
admin.site.register(TrickDefinition)
