from django.db import models

class Email(models.Model):
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.timestamp)

class Recipient(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    address = models.CharField(max_length=254) # 254 max email address length

    def __str__(self):
        return str(self.email) + " " + str(self.address)

class Word(models.Model):
    address = models.CharField(max_length=254) # 254 max email address length
    # We shouldn't need more than 45 chars here but better safe than sorry
    word = models.CharField(max_length=255)
    # Max possible value is 9223372036854775807
    # Supports negatives - ideally we'd create a custom type
    count = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.address) + " " + str(self.word) + " " + str(self.count)
