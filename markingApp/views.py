from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.forms.models import modelformset_factory
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDict
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'markingApp/home.html')

#Assignment
class assignmentCreateView(CreateView):
    model = Assignment
    template_name = 'markingApp/createAssignment.html'
    fields = ["assignmentName"]


    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()  # Save the object to the database
        return redirect(reverse_lazy('criteria-create', kwargs={'pk': self.object.pk}))

class assignmentEditView(UpdateView):
    model = Assignment
    template_name = 'markingApp/editAssignment.html'
    fields = ["assignmentName"]

class assignmentDeleteView(DeleteView):
    model = Assignment
    template_name = 'markingApp/deleteAssignment.html'
    fields = ["assignmentName"]
    success_url = "/"


    #Criteria

# Create a CreateView for creating Criteria objects
class criteriaCreateView(CreateView):
    model = Criteria # specify the model to use
    fields = ['assignmentID', 'criteriaDescription','criteriaTotalMark'] # specify the fields to use in the form
    template_name = 'markingApp/createCriteria.html' # specify the name of the template to use

    # specify the URL to redirect to upon successful submission
    def get_success_url(self):
        return reverse_lazy('criteria-create', kwargs={'pk': self.kwargs['pk']})

    # add additional context data to be passed to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        context['assignment'] = assignment
        # retrieve a queryset of existing Criteria objects for the current Assignment
        criteria_queryset = Criteria.objects.filter(assignmentID=assignment)
        # create a formset using modelformset_factory and pass it the queryset and initial values
        CriteriaFormSet = modelformset_factory(Criteria, extra=3, fields=('assignmentID', 'criteriaDescription','criteriaTotalMark'))
        formset = CriteriaFormSet(queryset=criteria_queryset, initial=[{'assignmentID': assignment}])
        # add the formset to the context data
        context['formset'] = formset
        return context

    # retrieve a queryset of Criteria objects for the current Assignment
    def get_queryset(self):
        queryset = super().get_queryset()
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        return queryset.filter(assignmentID=assignment)

    # handle form submission, needs to be overriden due to prepopulating assignmentID field
    def post(self, request, *args, **kwargs):
        # create a formset using modelformset_factory and pass it the submitted POST data
        CriteriaFormSet = modelformset_factory(Criteria, extra=3, fields=('assignmentID', 'criteriaDescription','criteriaTotalMark'))
        print(request.POST)
        formset = CriteriaFormSet(request.POST)
        if formset.is_valid(): # if the formset data is valid
            formset.save() # create objects from the formset data, but don't save them yet
            # for instance in instances: # loop over each instance
            #     instance.save() # save each instance to the database
            return redirect(self.get_success_url()) # redirect to the success URL
        else: # if the formset data is not valid
            return self.form_invalid(formset) # return an error response with the formset


class criteriaDeleteView(DeleteView):
    model = Assignment
    template_name = 'markingApp/deleteAssignment.html'
    fields = ["assignmentName"]
    success_url = "/"

    

class submissionCreateView(CreateView):
    model = Submission # specify the model to use
    fields = ["studentFirstName","studentLastName","submissionFile","assignmentID"] # specify the fields to use in the form
    template_name = 'markingApp/viewMarked.html' # specify the name of the template to use
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submissions'] = Submission.objects.filter(mark__isnull=False)
        return context
        

def mark(request):
    return render(request, 'markingApp/mark.html')

def feedbackCreateView(request, pk):
    submission = Submission.objects.get(id=pk)
    assignment = submission.assignmentID
    criteria = Criteria.objects.filter(assignmentID=assignment.id)
    criteria_list = list(criteria)
    FeedbackFormset = modelformset_factory(
        Feedback,
        extra=len(criteria),
        max_num=len(criteria),
        fields=['criteriaLevelID', 'comment'],
        widgets={'criteriaLevelID':forms.RadioSelect(),}
    )

    if request.method == "POST":
        formset = FeedbackFormset(request.POST, queryset=Feedback.objects.none())
        total_mark = request.POST.get('total_mark')
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.submissionID = submission
                instance.save()
            submission.mark= total_mark
            submission.save()
            return redirect('/')
        else:
            print("Formset Invalid")
            return redirect('/')

    else:
        formset = FeedbackFormset(queryset=Feedback.objects.none())
        for i, criterion in enumerate(criteria):
            formset.forms[i].fields['criteriaLevelID'].queryset = criterion.criterialevel_set.all()

        context = {
            'submission': submission,
            'formset': formset,
            'criteria':criteria_list
        }
        
        return render(request, 'markingApp/createFeedback.html', context)


def assignments(request):
    context={
        'assignments': Assignment.objects.all()
    }
    return render(request, 'markingApp/assignments.html', context)

class submissionDetailView(DetailView):
    model = Submission # specify the model to use
    template_name='markingApp/submissionDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission = self.object
        feedback = submission.feedback_set.all()
        context['feedback'] = feedback
        return context

def view_pdf(request, pk):
    submission = Submission.objects.get(pk=pk)
    with open(submission.submissionFile.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=' + submission.submissionFile.name
        return response


class markListView(ListView):
    model = Submission # specify the model to use
    template_name = 'markingApp/mark.html' # specify the name of the template to use
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submissions'] = Submission.objects.filter(mark__isnull=True)
        return context
        
class criteriaLevelCreateView(CreateView):
    model = CriteriaLevel # specify the model to use
    fields = ['criteriaID','criteriaLevel','criteriaLevelDescription']
    template_name = 'markingApp/createCriteriaLevel.html' # specify the name of the template to use

    # specify the URL to redirect to upon successful submission
    def get_success_url(self):
        return reverse_lazy('level-create', kwargs={'pk': self.kwargs['pk']})

    # add additional context data to be passed to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        # criteria = Criteria.objects.get(assignmentID=assignment)
        # context['criteria'] = criteria
        # retrieve a queryset of existing CriteriaLevel objects for the current Criteria
        # criteriaLevel_queryset = CriteriaLevel.objects.filter(criteriaID=criteria)
        criteriaLevel_queryset = CriteriaLevel.objects.none()
        # create a formset using modelformset_factory and pass it the queryset and initial values
        CriteriaLevelFormSet = modelformset_factory(CriteriaLevel, extra=3, fields=('criteriaID','criteriaLevel','criteriaLevelDescription'))
        formset = CriteriaLevelFormSet(queryset=criteriaLevel_queryset)
        # add the formset to the context data
        context['formset'] = formset
        context['assignment'] = assignment
        return context

    # handle form submission, needs to be overriden due to prepopulating assignmentID field
    def post(self, request, *args, **kwargs):
        # create a formset using modelformset_factory and pass it the submitted POST data
        CriteriaLevelFormSet = modelformset_factory(CriteriaLevel, extra=3, fields=('criteriaID','criteriaLevel','criteriaLevelDescription'))
        print(request.POST)
        formset = CriteriaLevelFormSet(request.POST)
        if formset.is_valid(): # if the formset data is valid
            formset.save() # create objects from the formset data, but don't save them yet
            # for instance in instances: # loop over each instance
            #     instance.save() # save each instance to the database
            return redirect(self.get_success_url()) # redirect to the success URL
        else: # if the formset data is not valid
            return self.form_invalid(formset) # return an error response with the formset

@csrf_exempt
def calculateMark(request):
    if request.method == 'POST':
        selected_radios = request.POST.getlist('selectedRadios[]')
        criteria_levels = CriteriaLevel.objects.filter(id__in=selected_radios)

        criteria_total_marks = {}
        for cl in criteria_levels:
            criteria_id = cl.criteriaID.pk
            criteria_total_mark = cl.criteriaID.criteriaTotalMark
            criteria_level = cl.criteriaLevel
            level_weight = criteria_level * 0.25
            criteria_weight = criteria_total_mark * level_weight
            if criteria_id in criteria_total_marks:
                criteria_total_marks[criteria_id] += criteria_weight
            else:
                criteria_total_marks[criteria_id] = criteria_weight
        
        total_mark = sum(criteria_total_marks.values())
        total_mark = round(total_mark)
        mark_data = {'total_mark': total_mark,
                     'criteria_marks':criteria_total_marks}
        return JsonResponse(mark_data, safe=False)
    
    else:
        return HttpResponse('Invalid request method')