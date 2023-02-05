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
class ProductType(models.Model):
    '''
    Product Type table
    '''

    name = models.CharField(
        max_length = 255,
        unique = True,
        null = False,
        blank = False,
        verbose_name = _("Type of product"),
        help_text = _("Format: required, max-255")
    )

    def __str__(self):
        return self.name

class Brand(models.Model):
    '''
    Product brand table
    '''
    name = models.CharField(
        max_length = 255,
        unique = True,
        blank = False,
        null = False,
        verbose_name = _("Brand name"),
        help_text = _("Format: required, max-255")
    )

class ProductAttribute(models.Model):
    '''
    Product attribute table
    '''
    name = models.CharField(
        max_length = 255,
        unique = True,
        null = False,
        blank = False,
        verbose_name = _("product attribute name"),
        help_text = _("format:required, unique, max-255")
    )

    description = models.TextField(
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("prodcut attribute description"),
        help_text = _("Format:required, unique, max-255")
    )

    def __str__(self):
        return self.name

class ProductAttributeValue(models.Model):
    '''
    Product attribute value table
    '''
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name ='product_attribute',
        on_delete = models.PROTECT
    )

    attribute_values = models.CharField(
        max_length = 255,
        unique = False,
        blank = False,
        null = False,
        verbose_name = _("attribute values"),
        help_text = _("Format:text or numbers, required, max-255")
    )

    def __str__(self):
        return f'{self.product_attribute.name}: {self.attribute_values}'
        
class ProductInventory(models.Model):
    '''
    Product inventory table
    '''
    sku = models.CharField(max_length=20, 
    unique = True, 
    null = False,
    blank = False,
    verbose_name = _("Stock keeping unit"),
    help_text = _("Format: reqired, unique, max-20"),
    )

    upc = models.CharField(max_length = 20,
        unique = True, 
        null = False,
        blank = False,
        verbose_name = _("Universal product unit"),
        help_text = _("Format:required, unique, max-20"))

    product_type = models.ForeignKey(ProductType, related_name="product_type",
     on_delete = models.PROTECT)

    product = models.ForeignKey(Product, related_name = "product" ,on_delete = models.PROTECT)

    brand = models.ForeignKey(Brand, related_name="brand" ,on_delete = models.PROTECT)

    attribute_values = models.ManyToManyField(
        ProductAttributeValue, 
        related_name = "prouct_attribute_value",
        through= "ProductAttributesValues"
    )

    is_active = models.BooleanField(default=True, 
    verbose_name = _("product visibility"),
    help_text= _("Format: True ==> product visible"))

    retail_price = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Recommended retail price"),
        help_text = _("format: max 999.99"),
        error_messages={
            "name": {
                "max_length":_("the price must be between 0 and 999.99")
            }
        }
    )

    store_price = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Regular store price"),
        help_text = _("format: max 999.99"),
        error_messages={
            "name": {
                "max_length":_("the price must be between 0 and 999.99")
            }
        }
    )

    sale_price = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("sale_price"),
        help_text = _("format: max 999.99"),
        error_messages={
            "name": {
                "max_length":_("the price must be between 0 and 999.99")
            }
        }
    )

    weight = models.FloatField(
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Product weight"),
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        verbose_name = _("Product created date"),
        help_text = _("Format: Y-m-d H:M:S")
    )

    updated_at = models.DateTimeField(
        auto_now = True,
        editable = False,
        verbose_name = _("Product updated date"),
        help_text = _("Format: Y-m-d H:M:S")
    )

    def __str__(self):
        return self.product.name


class Media (models.Model):
    '''
    The product images table
    '''
    product_inventory = models.ForeignKey(ProductInventory,
    on_delete = models.PROTECT, 
    related_name = "media_product_inventory")

    image = models.ImageField(
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("product image"),
        upload_to = "images/",
        default = "images/default.png",
        help_text = _("Format: required, default-default.png")
    )

    alt_text = models.CharField(
        max_length = 255, 
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Alt text for image"),
        help_text = _("Format: required, max:  255"),

    )

    is_feature = models.BooleanField(
        default = False,
        verbose_name = _("The main image of the product"),
        help_text = _("Format: default-false, true:main image")
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        verbose_name = _("Image created date"),
        help_text = _("Format: Y-m-d H:M:S")
    )

    updated_at = models.DateTimeField(
        auto_now = True,
        editable = False,
        verbose_name = _("Image updated date"),
        help_text = _("Format: Y-m-d H:M:S")
    )

    class Meta:
        verbose_name = _("product_image")
        verbose_name_plural = _("product_images")

class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name = "product inventory",
        on_delete = models.PROTECT
    )

    last_checked = models.DateTimeField(
        unique = False,
        null = True,
        blank = True,
        verbose_name = _("inventory stock check date"),
        help_text = _("Format: Y-m-d H-M-S")
    )

    units = models.IntegerField(
        default = 0,
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Quantity left in the stock"),
        help_text = _("Format: required, default-0")
    )

    units_sold = models.IntegerField(
        default = 0,
        unique = False,
        null = False,
        blank = False,
        verbose_name = _("Units sold to date"),
        help_text = _("Format: required, default-0")
    )

    def __str__(self):
        return self.product_inventory.upc


class ProductAttributeValues(models.Model):
    '''
    Product attribute value link table
    '''

    attribute_values = models.ForeignKey("ProductAttributeValues",
    related_name = "attributevalues",
    on_delete = models.PROTECT
    )

    product_inventory = models.ForeignKey(ProductInventory,
    related_name= "productattrvalues",
    on_delete = models.PROTECT
    )

    class Meta:
        unique_together = (("attribute_values", "product_inventory"),)

        