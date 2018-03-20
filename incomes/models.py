from django.db import models
import calendar


class Customer(models.Model):
    """The table to store all the possible cash origins."""

    date = models.DateField()
    name = models.CharField('customer', max_length=60)
    comments = models.TextField(blank=True)

    def post(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Hour(models.Model):
    """The table to store the monthly hours per customer."""

    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1, 13)]

    who = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dedication = models.DecimalField(max_digits=5, decimal_places=2)
    month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    comments = models.TextField(blank=True)

    def post(self):
        """Save the hours in the db."""
        self.save()

    def __str__(self):
        return '%s %s' % (self.who, self.month)


class Income(models.Model):
    """The table to store each income per customer."""

    date = models.DateField()
    who = models.ForeignKey(Customer, related_name='who', on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=5, decimal_places=2)
    tip = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField(blank=True)

    def post(self):
        """Save the income in the db."""
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return '%s %s' % (self.who, self.date)

    class Meta:
        ordering = ('date',)
