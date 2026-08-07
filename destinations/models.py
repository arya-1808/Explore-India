from django.db import models
from django.utils.text import slugify

CATEGORY_CHOICES = [
    ('beach', 'Beach'),
    ('hill_station', 'Hill Station'),
    ('heritage', 'Heritage'),
    ('wildlife', 'Wildlife'),
    ('adventure', 'Adventure'),
    ('pilgrimage', 'Pilgrimage'),
    ('city', 'City'),
    ('Waterfall','waterfall'),
    ('historical','historical')
]

STATE_CHOICES = [
      ('Goa', 'Goa'),
    ('Maharashtra', 'Maharashtra'),
    ('Rajasthan', 'Rajasthan'),
    ('Kerala', 'Kerala'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Karnataka', 'Karnataka'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Gujarat', 'Gujarat'),
    ('West Bengal', 'West Bengal'),
    ('Madhya Pradesh', 'Madhya Pradesh'),

    # add more states as needed
]


class Destination(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    state = models.CharField(max_length=30, choices=STATE_CHOICES)
    city = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    avg_budget_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)