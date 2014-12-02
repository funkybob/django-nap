from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)

    def vote_count(self):
        return self.aggregate(vote_sum=models.Sum('votes__weight'))


class Votes(models.Model):
    choice = models.ForeignKey('Choice', related_name='votes')
    weight = models.IntegerField(default=1)
