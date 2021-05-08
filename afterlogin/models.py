from django.db import models


class Reviews(models.Model):
    email = models.EmailField()
    paper_name = models.CharField(max_length=500)
    review = models.CharField(max_length=2000)
    conference_name = models.CharField(max_length=500, default='')
    Suggest = models.CharField(max_length=40, default='NO')

    def __str__(self):
        return self.paper_name


class Feedback(models.Model):
    email = models.EmailField()
    paper_name = models.CharField(max_length=500)
    Feedback = models.CharField(max_length=2000)
    conference_name = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.paper_name


class CfpData(models.Model):
    email = models.EmailField(blank=True)
    conference_name = models.CharField(max_length=500, unique=True)
    conference_acronym = models.CharField(max_length=500, unique=True)
    conference_start_date = models.DateField()
    conference_end_date = models.DateField()
    topic = models.CharField(max_length=500, blank=True)
    deadline = models.DateField()

    def __str__(self):
        return self.conference_name


class ConferenceData(models.Model):
    email = models.EmailField(blank=True)
    conference_name = models.CharField(max_length=500, unique=True)
    conference_acronym = models.CharField(max_length=500, unique=True)
    conference_start_date = models.DateField()
    conference_end_date = models.DateField()
    organizer = models.CharField(max_length=500)
    organizer_webpage = models.CharField(max_length=500)
    venue = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country_region = models.CharField(max_length=500)
    topic = models.CharField(max_length=500)
    area_notes = models.CharField(max_length=500)
    extra_information = models.CharField(max_length=500)
    assigned_paper = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.conference_name


class ASSigned(models.Model):
    paper_name = models.CharField(max_length=500)
    conference_name = models.CharField(max_length=500)


class AuthorData(models.Model):
    email = models.EmailField()
    paper_name = models.CharField(max_length=100, unique=True, blank=True)
    conference_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    co_author = models.BinaryField(max_length=1000)
    topics = models.CharField(max_length=1000, blank=True)
    abstract = models.CharField(max_length=2000)
    keywords = models.BinaryField(max_length=1000)
    pdf_paper = models.FileField()
    paper_assigned = models.BooleanField(default=False)
    deadline = models.DateField()
    feedback = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.paper_name


class PaperAssignmentS(models.Model):
    email = models.EmailField()
    paper_name = models.CharField(max_length=100)
    conference_name = models.CharField(max_length=100)
    topic_name = models.CharField(max_length=100)
