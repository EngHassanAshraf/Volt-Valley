from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.forms import (
    ModelForm,
    ValidationError,
    CharField,
    TextInput,
    EmailInput,
    PasswordInput,
    Textarea,
    NumberInput,
    Select,
    FileInput,
    CheckboxInput,
)
from .models import Product, Media, Category, Department


class RegisterForm(ModelForm):
    """User registration form with email and password."""

    password1 = CharField(
        label="كلمة المرور",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "minlength": "10",
                "required": True,
                "placeholder": "كلمة المرور",
            }
        ),
    )
    password2 = CharField(
        label="تأكيد كلمة المرور",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "تأكد كلمة المرور",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "first_name": TextInput(
                attrs={
                    "class": "form-control text-start",
                    "required": True,
                    "placeholder": "الاسم الاول",
                }
            ),
            "last_name": TextInput(
                attrs={
                    "class": "form-control text-start",
                    "required": True,
                    "placeholder": "الاسم الثاني",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "col form-control text-start",
                    "required": True,
                    "placeholder": "الايميل",
                }
            ),
        }

    def clean_password2(self):
        """Check if both password fields match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("كلمة السر ليست متطابقة")
        return password2

    def save(self, commit=True):
        """Save the user with the hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProductForm(ModelForm):
    """Product From"""

    class Meta:
        """Form model, fields and fields' attributes"""

        model = Product
        fields = [
            "name",
            "description",
            "qty",
            # "offer",
            "price",
            "category",
            "is_deleted",
        ]

        widgets = {
            "name": TextInput(attrs={"class": "col form-control", "required": True}),
            "description": Textarea(
                attrs={
                    "class": "col form-control",
                    "required": True,
                }
            ),
            "qty": NumberInput(
                attrs={"class": "col form-control text-start", "min": "0"}
            ),
            "price": NumberInput(
                attrs={
                    "class": "col form-control text-start",
                    "min": "0",
                    "max": "9999.99",
                }
            ),
            # "offer": NumberInput(
            #     attrs={"class": "col form-control text-start", "min": "0"}
            # ),
            "category": Select(attrs={"class": "col form-control"}),
            "is_deleted": CheckboxInput(attrs={"class": "col-1"}),
        }


class MediaForm(ModelForm):
    """Media From"""

    class Meta:
        """Form model, fields and fields' attributes"""

        model = Media
        fields = ["file", "media_type"]
        widgets = {
            "file": FileInput(
                attrs={
                    "class": "col form-control",
                    "required": True,
                    "hidden": True,
                },
            ),
            "media_type": Select(
                attrs={
                    "class": "col form-control",
                    "hidden": True,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        # Check if instance exists (indicating edit mode)
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if instance:  # Editing an existing record
            self.fields["file"].required = False

            self.fields["file"].widget.attrs.pop(
                "required", None
            )  # Remove the "required" attribute

    def clean_file(self):
        file = self.cleaned_data.get("file")
        max_size_mb = 2  # Set max size in MB

        if file and file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"File size should not exceed {max_size_mb}MB.")

        return file


class CategoryForm(ModelForm):
    """Category Form"""

    class Meta:
        """Form model, fields and fields' attributes"""

        model = Category
        fields = ["name"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "col form-control",
                    "required": True,
                }
            )
        }


class DepartmentForm(ModelForm):
    """Department Form"""

    class Meta:
        """Form model, fields and fields' attributes"""

        model = Department
        fields = ["title", "image", "is_deleted"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "col form-control",
                    "required": True,
                }
            ),
            "image": FileInput(
                attrs={
                    "class": "col form-control",
                    "required": True,
                }
            ),
            "is_deleted": CheckboxInput(attrs={"class": "col-1"}),
        }

    def __init__(self, *args, **kwargs):
        # Check if instance exists (indicating edit mode)
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if instance:  # Editing an existing record
            self.fields["image"].required = False
            self.fields["image"].widget.attrs.pop(
                "required", None
            )  # Remove the "required" attribute

    def clean_file(self):
        image = self.cleaned_data.get("image")
        max_size_mb = 2  # Set max size in MB

        if image and image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"File size should not exceed {max_size_mb}MB.")

        return image
