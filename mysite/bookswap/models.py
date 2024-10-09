from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.book.title} by {self.user.username}'
    
    class Meta:
        unique_together = ('book','user')



class SwapRequest(models.Model):
    book_requested = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requested_swap')
    book_offered = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offered_swap')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swap_requests')
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('accepted','Accepted'),('declined','Declined')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Swap request from {self.user.username}'