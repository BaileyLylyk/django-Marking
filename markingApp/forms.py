from django import forms
from .models import *

# class assignmentNameForm(forms.Form):
#     assignmentName = forms.CharField(label='Assignment Name', max_length=100)

# class CriteriaForm(forms.Form):
#     criteriaID = forms.IntegerField(label= 'Criteria ID')
#     criteriaDescription = forms.CharField(widget=forms.Textarea(attrs={'size': '400'}))

class CriteriaLevelForm(forms.Form):
    pass

class FeedbackForm(forms.Form):
    pass

class SubmissionForm(forms.Form):
    pass

    
class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['criteriaLevelID', 'comment']
        widgets = {
            # 'submissionID' : forms.HiddenInput(),
            # 'criteriaLevelID':forms.RadioSelect(),
        }
        