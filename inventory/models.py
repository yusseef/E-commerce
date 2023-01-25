from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
# Create your models here.

class Category(MPTTModel):
    """
    Category table with mptt
    """
    name = models.CharField(
        max_length=500,
        null = False,
        unique= False,
        blank = False,
        verbose_name = _('Category name'),
        help_text = _("format: required, max = 500 cahrachter")
         )
    
    slug = models.SlugField(
        max_length = 150,
        verbose_name = _('Category safe url'),
        help_text = _("format: required, letters, numbers, underscores, hyphens")
    )

    is_active = models.BooleanField(
        default = True,
    )

    parent = TreeForeignKey(
        "self",
        on_delete = models.PROTECT,
        related_name = "children",
        null = True,
        blank = True,
        unique = False,
        verbose_name= _("Parent of category"),
        help_text = _("format: not required")
    ) 

    class MPTTMeta:
        order_insertion_by = ["name"]
    
    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product details table
    """
    web_id = models.CharField(
        max_length = 255,
        unique = True,
        null = False,
        blank = False,
        verbose_name = _("Product safe url"),
        help_text = _("Format: required, max-255"),
    )

    name = models.CharField(
        max_length = 255,
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Product name"),
        help_text = _("format: required, max-255"),
    )

    description = models.TextField(
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Product description"),
        help_text = _("format: required")
    )

    category = TreeManyToManyField(Category)
    
    is_active = models.BooleanField(
        unique = False,
        null = False,
        blank = False,
        default = True,
        verbose_name = _("Product visibility"),
        help_text = _("format: True+ product visible")
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        verbose_name = _("date product created"),
        help_text = _("format: Y-M-d H:M:s")
    )

    updated_at = models.DateTimeField(
        auto_now = True,
        verbose_name = _("date product updated"),
        help_text = _("format: Y-M-d H:M:s")
    ) 

    def __str__(self):
        return self.name