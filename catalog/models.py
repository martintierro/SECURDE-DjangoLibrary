import uuid  # Required for unique book instances
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.TextField(max_length=8, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Publisher(models.Model):
    """Model representing a book genre"""
    name = models.CharField(
        max_length=200, help_text='Enter the name of the publisher')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than the object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(
        'Publisher', on_delete=models.SET_NULL, null=True)

    year = models.CharField('Year of Publication',
                            max_length=4, help_text='Enter Year of Publication')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character ISBN number')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    current_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='%(class)s_current_books')
    past_profiles = models.ManyToManyField(Profile)

    STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['status']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    text = models.CharField(max_length=2000)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(
        'Profile', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id}'
