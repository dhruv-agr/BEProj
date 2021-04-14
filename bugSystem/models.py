from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    #Model representing a project



    name = models.CharField(max_length=200, help_text='Enter the name of project')

    teamMember = models.ManyToManyField(User)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('project-detail', args=[str(self.id)])
    


class Bugreport(models.Model):
    # Model for bug reports

    class Meta:
        permissions = (("can_view_all_bugreports", "View All bug reports"),
        ("can_file_new_bugreport", "Can file new bugreport"),
        )


    severity_type = (
        ('Major','Major'),
        ('Normal','Normal'),
        ('Blocker','Blocker'),
        ('Critical','Critical'),
        ('Minor','Minor'),
        ('Trivial','Trivial'),
        ('Enhancement','Enhancement'),
    )

    status_type = (
        ('Fixed','Fixed'),
        ('Worksforme','Worksforme'),
        ('Duplicate','Duplicate'),
        ('Wontfix','Wontfix'),
        ('Open','Open'),
    )



    bugid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular bug')

    Assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
     

    Summary = models.TextField(max_length=1000, help_text='Enter a brief description of the bug')

    Status = models.CharField(
        max_length=200,
        choices = status_type,
        default = 'open',
        help_text = 'Status Type',
    )

    Severity = models.CharField(
        max_length=200,
        choices = severity_type,
        default = 'Normal',
        help_text = 'Severity Type',
    )

    project = models.ForeignKey('Project',on_delete=models.RESTRICT, null=True)

    project_name = models.CharField(max_length=200, help_text='Enter the name of project',default = 'Default Name')


    def __str__(self):
            """String for representing the Model object."""
            return str(self.bugid)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this bug."""
        return reverse('bugreport-detail', args=[str(self.bugid)])
