from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    metamask_wallet_address = models.CharField(max_length=42)

    def __str__(self):
        return self.user.username


class Chatbox(models.Model):
    chatbox_id = models.CharField(max_length=200)
    
    def __str__(self):
        return self.chatbox_id

class Poll(models.Model):
    VOTING_STATUS_CHOICES = [
        ('open', 'open'),
        ('closed', 'closed'),
    ]

    class Option(models.TextChoices):
        OPTION_A = 'a', 'a'
        OPTION_B = 'b', 'b'

    title = models.CharField(max_length=200)
    option_a_label = models.CharField(max_length=200)
    option_a_votes = models.PositiveIntegerField(default=0)
    option_b_label = models.CharField(max_length=200)
    option_b_votes = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbox = models.OneToOneField(Chatbox, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length=1, choices=Option.choices, null=True, blank=True)
    voting_status = models.CharField(max_length=10, choices=VOTING_STATUS_CHOICES, default='open')
    duration_minutes = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    def get_total_votes(self):
        return self.option_a_votes + self.option_b_votes
    
    def get_percentage(self, option):
        if option == 'a':
            return round(self.option_a_votes / self.get_total_votes() * 100)
        elif option == 'b':
            return round(self.option_b_votes / self.get_total_votes() * 100)
        else:
            return 0
        
    def get_winner(self):
        if self.duration_minutes == 0:
            if self.option_a_votes > self.option_b_votes:
                self.winner = 'a'
            elif self.option_b_votes > self.option_a_votes:
                self.winner = 'b'
                
    def get_voting_status(self):
        if self.duration_minutes > 0:
            self.voting_status = 'open'
        else:
            self.voting_status = 'closed'
    
        
        
class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chatbox = models.ForeignKey(Chatbox, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"{self.creator} - {self.text}"

