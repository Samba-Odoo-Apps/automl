from django.forms import ModelForm
from auto.models import Document, PredictDocument

class DocumentForm(ModelForm):
	class Meta:
		model=Document
		fields=["name","data","target"]
class PredictDocumentForm(ModelForm):
	class Meta:
		model=PredictDocument
		fields = ["name","data","doc"]