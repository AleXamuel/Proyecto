from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
         return self.name
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
    related_name="products")
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        unique_together = [("category", "name")]
        ordering = ["name"]
    def __str__(self):
        return f"{self.name} ({self.category})"    