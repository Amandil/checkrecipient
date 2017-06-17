from django.db import models

class Email(models.Model):
    timestamp = models.DateTimeField()

class Recipient(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    address = models.CharField(max_length=254) # 254 max email address length

class Word(models.Model):
    address = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    # We shouldn't need more than 45 chars here but better safe than sorry
    word = models.CharField(max_length=255)
    # Max possible value is 9223372036854775807
    # Supports negatives - ideally we'd create a custom type
    count = models.BigIntegerField()
