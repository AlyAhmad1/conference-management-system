from django.db import models


class Reviews(models.Model):
    email = models.EmailField()
    conference_acronym = models.CharField(max_length=500)
    review = models.CharField(max_length=2000)
    conference_name = models.CharField(max_length=500, default='')
    Suggest = models.CharField(max_length=40, default='NO')


class Feedback(models.Model):
    email = models.EmailField()
    conference_acronym = models.CharField(max_length=500)
    Feedback = models.CharField(max_length=2000)
    conference_name = models.CharField(max_length=500,default='')


class CfpData(models.Model):
    email = models.EmailField(blank=True)
    conference_name = models.CharField(max_length=500, unique=True)
    conference_acronym = models.CharField(max_length=500, unique=True)
    conference_start_date = models.DateField()
    conference_end_date = models.DateField()
    cfp_abstract_deadlines = models.DateField()
    cfp_submission_deadline = models.DateField()
    webpage = models.CharField(max_length=500)
    venue = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country_region = models.CharField(max_length=500)
    primary_area = models.CharField(max_length=500)
    secondary_area = models.CharField(max_length=500)
    area_notes = models.CharField(max_length=500)
    topic_1 = models.CharField(max_length=500)
    topic_2 = models.CharField(max_length=500)
    topic_3 = models.CharField(max_length=500)
    topic_4 = models.CharField(max_length=500)
    extra_information = models.CharField(max_length=500)
    paper_assigned = models.BooleanField(default=False)
    document = models.FileField(null=True, default=None)

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
    webpage = models.CharField(max_length=500)
    venue = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country_region = models.CharField(max_length=500)
    primary_area = models.CharField(max_length=500)
    secondary_area = models.CharField(max_length=500)
    area_notes = models.CharField(max_length=500)
    topic_1 = models.CharField(max_length=500)
    topic_2 = models.CharField(max_length=500)
    topic_3 = models.CharField(max_length=500)
    topic_4 = models.CharField(max_length=500)
    extra_information = models.CharField(max_length=500)
    assigned_paper = models.CharField(max_length=500, blank=True)


class AuthorData(models.Model):
    email = models.EmailField()
    paper_name = models.CharField(max_length=100, unique=True, blank=True)
    conference_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    co_author = models.BinaryField(max_length=1000)
    topics = models.CharField(max_length=1000,blank=True)
    abstract = models.CharField(max_length=2000)
    keywords = models.BinaryField(max_length=1000)
    pdf_paper = models.FileField()