from django.contrib import admin
from .models import Run, TrickInstance, TrickDefinition, Restriction
from django import forms
from decimal import Decimal

# class TrickInstanceInline(admin.TabularInline):
#     model = TrickInstance
#     extra = 1  # Defines how many blank forms are displayed by default.
#     fields = [
#         "name",
#         "trick_id",
#         "right",
#         "reverse",
#         "successful",
#         "twisted",
#         "twisted_exit",
#         "flipped",
#         "double_flipped",
#         "devil_twist",
#         "cab_slide",
#     ]


# class RunAdmin(admin.ModelAdmin):
#     list_display = ("date", "time", "wing", "site", "user")  # Customize as needed.
#     inlines = [TrickInstanceInline]


# admin.site.register(Run, RunAdmin)


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


admin.site.register(TrickDefinition)


# class TrickDefinitionAdmin(admin.ModelAdmin):
#     inlines = [TrickDefinitionInline]


# admin.site.register(TrickDefinition, TrickDefinitionAdmin)
# class TrickInstanceForm(forms.ModelForm):
#     class Meta:
#         model = TrickInstance
#         fields = "__all__"  # Start with all fields

#     def __init__(self, *args, **kwargs):
#         super(TrickInstanceForm, self).__init__(*args, **kwargs)
#         if self.instance:# and self.instance.trick_definition_id:
#             trick_def = TrickDefinition.objects.get(id=self.instance.trick_definition_id)
#             # Conditionally display fields based on TrickDefinition
#             if not trick_def.has_orientation:
#                 del self.fields['orientation']
#             if trick_def.reverse_bonus == 0:
#                 del self.fields['reverse']
#             # Add more conditions as necessary for each field

# class TrickInstanceAdmin(admin.ModelAdmin):
#     form = TrickInstanceForm
#     list_display = [ 'run', 'right', 'reverse', 'twisted']

# admin.site.register(TrickInstance, TrickInstanceAdmin)

# class TrickInstanceInline(admin.TabularInline):
#     model = TrickInstance
#     form = TrickInstanceForm
#     extra = 1

# class RunAdmin(admin.ModelAdmin):
#     inlines = [TrickInstanceInline]
#     list_display = ('date', 'time', 'wing', 'site', 'user')

# admin.site.register(Run, RunAdmin)


from django import forms
from django.contrib import admin
from .models import TrickInstance, TrickDefinition


class TrickInstanceForm(forms.ModelForm):
    class Meta:
        model = TrickInstance
        exclude = []


class TrickInstanceInline(admin.TabularInline):
    model = TrickInstance
    extra = 1

    def get_exclude(self, request, obj=None, **kwargs):
        excluded_fields = super().get_exclude(request, obj, **kwargs) or []
        if obj:  # Check if there is a parent object
            # Check each TrickInstance related to the obj (Run in this case)
            for trick_instance in obj.tricks.all():
                trick_def = trick_instance.trick_definition
                # Determine which fields to exclude based on the trick definition
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

    # Optionally set the fields manually to control order and inclusion
    # fields = [
    #     "trick_definition",
    #     "right",
    #     "reverse",
    #     "twisted",
    #     "twisted_exit",
    #     "flipped",
    #     "double_flipped",
    #     "devil_twist",
    #     "cab_slide",
    #     "successful",
    # ]


class RunAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "wing", "site", "user")
    inlines = [TrickInstanceInline]


admin.site.register(Run, RunAdmin)


admin.site.register(Restriction)
