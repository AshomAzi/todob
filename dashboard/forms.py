from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    description = forms.CharField(required=False)

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority"]
