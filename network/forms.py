from django import forms


from .models import Post

MAX_POST_LENGTH = 240

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]

    def clean_content(self):
        data = self.cleaned_data["content"]
        if len(data) > MAX_POST_LENGTH:
            raise forms.ValidationError("This post is too long")
        return data
