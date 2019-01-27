from django import forms
from blog.models import Post, Comments

class PostForm(forms.ModelForm):
    # All the below inherits from the Post model
    class Meta():
        model = Post
        # Including only these fields on the form:
        fields = ('author', 'title','text')

        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
class CommentForm(forms.ModelForm):
    # All the below inherits from the Comments Model
    class Meta():
        model = Comments
        # Including only these fields on the form:
        fields = ('author', 'text')

        widgets = {
        'author': forms.TextInput(attrs={'class':'textinputclass'}),
        'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
# ++++++++++++++++++++++++++++++++++++
# ++++++++++NOTES ON WIDGETS++++++++++
# ++++++++++++++++++++++++++++++++++++
# Widgets here allow us to essentially assign classes to form field inputs etc
# for styling later on. The form input type needs to be related/the same as the
# model and then we can pass in attributes such as a class or ID etc. and give
# it values which we can use in css.
