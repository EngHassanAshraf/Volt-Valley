"""Filters Package"""

from django_filters import (
    FilterSet,
    CharFilter,
    RangeFilter,
    ModelMultipleChoiceFilter,
)

from django.forms.widgets import (
    TextInput,
    CheckboxSelectMultiple,
)

from .models import (
    Product,
    Category,
)


class ProductFilter(FilterSet):
    categories = Category.objects.all()

    name = CharFilter(
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control p-1"}),
        label="الإسم",
    )

    price = RangeFilter(
        field_name="price",
        label="السعر",
    )

    category = ModelMultipleChoiceFilter(
        field_name="category",
        queryset=categories,
        widget=CheckboxSelectMultiple(attrs={"class": "bg-white text-black p-1"}),
        label="الفئة",
    )

    class Meta:
        """Meta Class that take the model and the fields"""

        model = Product
        fields = [
            "name",
            "price",
            "category",
        ]
