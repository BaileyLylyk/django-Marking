from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


# Assignment
class Assignment(models.Model):
    assignmentName = models.CharField(max_length=100)

    def __str__(self):
        return self.assignmentName
    
    def get_absolute_url(self):
        return reverse('assignment-view')



#Criteria
class Criteria(models.Model):
    assignmentID = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    criteriaDescription = models.TextField()
    criteriaTotalMark = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.criteriaDescription

#Criteria Level
class CriteriaLevel(models.Model):
    LEVEL_CHOICES = [
    (1,'Level 1'),
    (2,'Level 2'),
    (3,'Level 3'),
    (4,'Level 4'),
]

    criteriaID = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    criteriaLevel = models.IntegerField(choices=LEVEL_CHOICES)
    criteriaLevelDescription = models.TextField()

    def __str__(self):
        return self.criteriaLevelDescription

#Submission
class Submission(models.Model):
    studentFirstName = models.CharField(max_length=100)
    studentLastName = models.CharField(max_length=100)
    mark = models.IntegerField(blank=True, null=True)
    submissionFile = models.FileField(upload_to='submissions', validators=[FileExtensionValidator(['pdf'])])
    assignmentID = models.ForeignKey(Assignment, on_delete=models.CASCADE)


#Feedback
class Feedback(models.Model):
    submissionID = models.ForeignKey(Submission, on_delete=models.CASCADE)
    criteriaLevelID = models.ForeignKey(CriteriaLevel, on_delete=models.CASCADE)
    comment = models.TextField()
