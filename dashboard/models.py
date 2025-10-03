from nanoid import generate
from django.utils.text import slugify

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def validate_file_size(file):
    max_size_kb = 2000  # Set max file size (in KB)
    if file.size > max_size_kb * 1024:  # Convert KB to bytes
        raise ValidationError(f"File size should not exceed {max_size_kb}KB.")


# abstract models


class IdSlug(models.Model):
    """
    Abstract model
    provide
        - id field of type nanoid
        - slug field for readability and SEO optimization
    """

    id = models.CharField(
        primary_key=True,
        max_length=21,
        default=generate,
        editable=False,
    )
    slug = models.SlugField(unique=True, blank=True, max_length=200)

    class Meta:
        """Abstract Class"""

        abstract = True


class SoftDelete(models.Model):
    """
    Abstract model
    provide
        - soft delete mechanism using an `is_deleted` flag.
    """

    is_deleted = models.BooleanField(default=False, verbose_name="Deleted?")

    class Meta:
        """Abstract Class"""

        abstract = True


class Timestamped(models.Model):
    """
    Abstract model
    provide
        - created_at field to hold the datetime of creating an object
        - updated_at field to hold the datetime of updating an object
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        """Abstract Class"""

        abstract = True


# main models


class User(AbstractUser):
    id = models.CharField(
        primary_key=True, max_length=21, default=generate, editable=False
    )
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.email


class Department(IdSlug, Timestamped, SoftDelete):
    """Main Site Depatments consists of at least two categories of products"""

    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="departments/%Y/%m/%d/",
        verbose_name="Image",
        validators=[validate_file_size],
    )

    def save(self, *args, **kwargs):
        """nanoid.generate a title and unique slug based on the department title"""

        categories = self.category.all()
        if categories:
            title = ""
            for category in categories:
                title += f"{category.name} / "
            title = title.strip().strip("/ ")
            self.title = title

        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)  # Convert name to slug
            unique_id = generate(size=6)  # nanoid.generate a short unique ID
            self.slug = f"{base_slug}-{unique_id}"  # Create unique slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Category(IdSlug, Timestamped):
    """
    Model representing a products ctegoriss with category name.
    """

    name = models.CharField(max_length=50, verbose_name="Category Name")
    department = models.ForeignKey(
        Department,
        related_name="category",
        on_delete=models.SET_NULL,
        verbose_name="Department",
        null=True,
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """nanoid.generate a unique slug based on the category name"""
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)  # Convert name to slug
            unique_id = generate(size=6)  # nanoid.generate a short unique ID
            self.slug = f"{base_slug}-{unique_id}"  # Create unique slug
        super().save(*args, **kwargs)


class Product(IdSlug, Timestamped, SoftDelete):
    """
    Model representing a product with various attributes including category, price, and stock.
    """

    name = models.CharField(max_length=150, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    qty = models.PositiveSmallIntegerField(default=0, verbose_name="Quantity")
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.0,
        verbose_name="Unit Price",
    )

    offer = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        verbose_name="Discount",
    )

    category = models.ForeignKey(
        Category,
        related_name="product",
        on_delete=models.SET_NULL,
        verbose_name="Category",
        null=True,
    )

    def __str__(self):
        return str(self.name)

    def is_in_stock(self):
        """
        Check if the product is in stock
        """
        return self.qty > 0

    @property
    def discounted_price(self):
        """
        calculate the new price
        """
        return self.price * (1 - (self.offer / 100))

    def save(self, *args, **kwargs):
        """nanoid.generate a unique slug based on the product name"""
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)  # Convert name to slug
            unique_id = generate(size=6)  # nanoid.generate a short unique ID
            self.slug = f"{base_slug}-{unique_id}"  # Create unique slug
        super().save(*args, **kwargs)


class Media(Timestamped):
    """
    Model for storing media files (images/videos) related to products.
    """

    IMAGE = "image"
    VIDEO = "video"

    MEDIA_TYPE_CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    ]

    product = models.ForeignKey(
        Product, related_name="media", on_delete=models.CASCADE, verbose_name="Product"
    )
    file = models.FileField(
        upload_to="products/%Y/%m/%d/",
        default="products/default.png",
        verbose_name="File",
        validators=[validate_file_size],
    )
    media_type = models.CharField(
        max_length=50, choices=MEDIA_TYPE_CHOICES, verbose_name="File Type"
    )

    def __str__(self):
        return f"{self.product.name}:{str(self.media_type).capitalize()}"
