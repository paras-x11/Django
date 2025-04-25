from django.db import models

# Create your models here.
class Author(models.Model):
    authorName = models.CharField( max_length=50)

    def __str__(self):
        return self.authorName

class Publication(models.Model):
    publicationName = models.CharField( max_length=50)

    def __str__(self):
        return self.publicationName

class Book(models.Model):
    bookName = models.CharField( max_length=50)
    bookQty = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bookName}"