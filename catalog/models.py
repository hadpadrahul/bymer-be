from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Product categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    image = models.ImageField(upload_to="products/", blank=True)
    description = models.TextField()
    customer = models.CharField(max_length=150, blank=True)
    specification = models.TextField(blank=True)
    extra_details = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Machinery(models.Model):
    class Plant(models.TextChoices):
        PLANT_1 = "plant_1", "Plant I"
        PLANT_2 = "plant_2", "Plant II"

    plant = models.CharField(max_length=20, choices=Plant.choices, db_index=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="machinery/", blank=True)
    total_machines = models.PositiveIntegerField(blank=True, null=True)
    make = models.CharField(max_length=150, blank=True)
    year_of_purchase = models.PositiveIntegerField(blank=True, null=True)
    tonnage_or_capacity = models.CharField(max_length=150, blank=True)
    platen_size_or_dimensions = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Machinery"

    def __str__(self):
        return self.name
