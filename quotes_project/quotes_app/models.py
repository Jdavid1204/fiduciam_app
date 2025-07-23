from django.db import models



class Author(models.Model):
    """Represents a quote author."""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Represents a tag for categorising quotes."""
    name_tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name_tag


class Quote(models.Model):
    """Represents a quote with its author and tags."""
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)

    def __str__(self):
        return f'"{self.text}" by {self.author.name} with tags {", ".join(tag.name_tag for tag in self.tags.all())}'

