from django import forms

# A text field to use in those TextField's which don't require large texts, but can use one-line text inputs
textInputWidget = forms.TextInput(attrs={'class': 'vLargeTextField'})
textAreaWidget = forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 5})
largeTextAreaWidget = forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 10})
