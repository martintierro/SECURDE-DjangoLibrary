from django.contrib import admin
from .models import Publisher, Author, Book, BookInstance, Review

# Register your models here.
admin.site.register(Review)

class BookInline(admin.TabularInline):
    model = Book
    fieldsets = (
        ('BOOKS', {
            'fields': ('title', 'isbn', 'author',)
        }),
    )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    fields = ['first_name', 'last_name']
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    inlines = [BooksInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'id')
    list_filter = ('status',)

    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status',)
        }),
    )


admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)