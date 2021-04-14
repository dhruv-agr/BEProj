from django import forms
from django.core.exceptions import ValidationError
from bugSystem.models import Project, Bugreport


class NewBugreportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('u',None)
        super(NewBugreportForm, self).__init__(*args, **kwargs)

        projectlist = Project.objects.filter(teamMember=self.user).values('name')
        c=[x for x in projectlist]
        clist=[]
        for x in c:
            clist.append(x.get('name'))
        
        ch = tuple((x,x) for x in clist)
        self.fields['project_name']  = forms.ChoiceField(
            choices = ch
        )




    severity_type = (
        ('m','Major'),
        ('n','Normal'),
        ('b','Blocker'),
        ('c','Critical'),
        ('mi','Minor'),
        ('t','Trivial'),
        ('e','Enhancement'),
    )
    severity = forms.ChoiceField(
        choices=severity_type,
        help_text = "Select a severity",

    )   
    summary = forms.CharField(
        max_length=1000,
        help_text='Enter a brief description of the bug'
    )
    # project_name = forms.ChoiceField( )

    def clean_summary(self):
        data = self.cleaned_data['summary']

        return data

class EditAssignee(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('u',None)
        self.proj = kwargs.pop('p',None)
        super(EditAssignee, self).__init__(*args, **kwargs)
        # print(self.proj.id)
        projectlist = Project.objects.all().values()#filter(teamMember__pk=self.proj.id).values()
        # print('Project:',projectlist)
        # c=[x for x in projectlist]
        # clist=[]
        # for x in c:
        #     clist.append(x.get('name'))
        
        # ch = tuple((x,x) for x in clist)

        p = Project.objects.get(name = self.proj)
        print(p)
        tm = p.teamMember.values('username')
        clist = []
        for x in tm:
            clist.append(x.get('username'))
        
        ch = tuple((x,x) for x in clist)

        print(tm)
        self.fields['assignee']  = forms.ChoiceField(
            choices = ch
        )