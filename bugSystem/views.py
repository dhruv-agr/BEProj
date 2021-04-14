from django.shortcuts import render
from bugSystem.models import Project, Bugreport
from django.views import generic
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from bugSystem.forms import NewBugreportForm,EditAssignee
import pickle
from django.http import JsonResponse
import json
import sklearn

import nltk
nltk.download('stopwords')
import gensim
from gensim import corpora
import string

import pprint as pp
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


# In class based views, the default template variable name and template file name 
# is modelname_list.html( for ListView)

# for eg, in ProjectListView and ProjectOfTeamMemberListView, the model used is Project, so 
# the default template variable and template file name is project_list.html.
# so if we donot specify a specific template file name to ProjectOfTeamMemberListView, it calls 
# the project_list.html which we have already used for ProjectListView for listing All Projects.
# But since the template file is now called with the same default template varibale name project_list,
# the user specific project list is passed from the ProjectOfTeamMemberListView view 
# compare the heading of the pages to know which page is served since both list projects and it can be 
# confusing.

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_projects = Project.objects.all().count()
    num_bugreports = Bugreport.objects.all().count()

    # Available books (status = 'a')
    num_bugreports_open = Bugreport.objects.filter(Status__exact='open').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_projects': num_projects,
        'num_bugreports': num_bugreports,
        'num_bugreports_open': num_bugreports_open,
        'num_visits': num_visits,
        'is_manager':False
    }
    if request.user.groups.filter(name = 'Manager').exists():
        context['is_manager'] = True


    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 10
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Project.objects.name # Get all project names
    # template_name = 'projects/my_arbitrary_template_name_list.html'  # Specify your own template name/location

class ProjectDetailView(generic.DetailView):
    model = Project
def ProjectDetailView(request,pk):
    p = Project.objects.get(id = pk)
    tm = p.teamMember.values('username')


    context={'project':p,
            'teamMember':tm}
    return render(request,'project_detail.html',context = context)

def UserProfileView(request):
    
    context={}
    return render(request, 'userprofile.html', context=context)

class ProjectOfTeamMemberListView(LoginRequiredMixin,generic.ListView):
    # Generic class based view listing projects for a particular team member
    model = Project
    template_name = 'bugSystem/project_of_teamMember.html'
    paginate_by=10

    def get_queryset(self):
        return Project.objects.filter(teamMember=self.request.user)

class BugreportsOfTeamMemberListView(LoginRequiredMixin,generic.ListView):
    model = Bugreport
    template_name = 'bugSystem/bugreport_of_teamMember.html'
    paginate_by = 10

    def get_queryset(self):
        allBugreportOfAllMyProjects = Bugreport.objects.filter(project__teamMember=self.request.user)
        developerAssignedBugreports = Bugreport.objects.filter(Assignee = self.request.user)
        if self.request.user.groups.filter(name ="Tester"):
            return allBugreportOfAllMyProjects
        elif self.request.user.groups.filter(name = "Developer"):
            return developerAssignedBugreports


# class BugreportsDetailView(LoginRequiredMixin,generic.DetailView):
#     model = Bugreport
#     paginate_by = 10
@login_required
def bugreportdetailview(request,pk):
    thisbugreport = Bugreport.objects.get(bugid=pk)
    
    # record = Bugreport()
    prj = thisbugreport.project
    # print('This should be the primary key of project:',prj)
    if request.method == 'POST':

        form = EditAssignee(request.POST,u = request.user,p=prj)
        
        if form.is_valid():
            assigneeName = form.cleaned_data['assignee']
            userInstanceOfAssigneeName = User.objects.get(username=assigneeName)
            thisbugreport.Assignee = userInstanceOfAssigneeName
            thisbugreport.save()

            return HttpResponseRedirect(reverse('bugreport-detail', args=[str(pk)]))

    else:

        form = EditAssignee(initial={'assignee': 'None'},u=request.user,p=prj)



    context = {
        'form': form,
        'bugreport':thisbugreport,
    }

    

    return render(request, 'bugreport_detail.html', context=context)



class AllBugreportsListView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    permission_required = 'bugSystem.can_view_all_bugreports'
    model = Bugreport
    template_name = 'bugSystem/all_bugreports.html'

@login_required
@permission_required('bugSystem.can_file_new_bugreport', raise_exception=True)
def new_bugreport(request):
    record = Bugreport()

    if request.method == 'POST':

        form = NewBugreportForm(request.POST,u = request.user)
        # print(request.POST)
        if form.is_valid():
            record.Severity = form.cleaned_data['severity']
            record.Summary = form.cleaned_data['summary']
            record.project_name = form.cleaned_data['project_name']
            record.project = Project.objects.get(name = record.project_name)
            record.save()

            return HttpResponseRedirect(reverse('my-bug-reports') )

    else:

        form = NewBugreportForm(initial={'severity': 'n'},u=request.user)

    # projectlist = Project.objects.filter(teamMember=request.user).values('name')
    # print(projectlist)
    # print(type(projectlist))
    # c=[x for x in projectlist]
    # print(c)
    # clist=[]
    # for x in c:
    #     clist.append(x.get('name'))
    # print(clist)
    
    # ch = tuple((x,x) for x in clist)
    # print((ch))
    # form.project_name.choices = ch

    context = {
        'form': form,
        
    }

    return render(request, 'bugSystem/new_bugreport.html', context)

def mlseverity(request):
    mlmodel = pickle.load(open('linearsvc-severity.sav','rb'))
    s = json.load(request)['summary']
    # print(type(s))
    clean_data = clean(s)
    # print(clean_data)
    cv2 = pickle.load(open('tfidfseverity.sav','rb'))
    inputstr = cv2.transform([s])
    # print(inputstr)




    result = mlmodel.predict(inputstr)
    # print(result)
    result = str(result)
    result = result.strip("'[]")
    # print(data_from_post)
    data = {
        'my_data':result,
    }
    
    # print('inside view')
    # print(request.body)
    return JsonResponse(data)




def clean(text):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in text.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

    
def mlass(request):
    mlmodel = pickle.load(open('linearsvc-ass.sav','rb'))
    s = json.load(request)['summary']
    # print(type(s))
    clean_data = clean(s)
    # print(clean_data)
    cv2 = pickle.load(open('tfidfass.sav','rb'))
    inputstr = cv2.transform([s])
    # print(inputstr)




    result = mlmodel.predict(inputstr)
    # print(result)
    result = str(result)
    result = result.strip("'[]")

    # print(data_from_post)
    data = {
        'my_data':result,
    }
    
    # print('inside view')
    # print(request.body)
    return JsonResponse(data)
