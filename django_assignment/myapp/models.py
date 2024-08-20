from django.db import models
from django.utils import timezone

class Location(models.Model):
    LOCATION_TYPES = [
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ]
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=LOCATION_TYPES, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=255,null=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.TextField(null=True)
    locations = models.ManyToManyField(Location, related_name='properties')
    room_type = models.TextField(null=True)
    rating = models.TextField(null=True)
    amenities = models.ManyToManyField(Amenity, related_name='properties')
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='property_images/', null=True, max_length=255)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.property:
            return f"Image for {self.property.title}"
        else:
            return "Image with no associated property"
