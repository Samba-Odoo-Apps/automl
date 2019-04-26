import os
from time import time
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import  r2_score

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse

from auto.forms import DocumentForm, PredictDocumentForm
from auto.models import Document, PredictDocument
def predict_doc_list_view(request, pk=None):
	docs=[]
	if not pk:
		docs = PredictDocument.objects.all()
	return render(request, "auto/predict_document_list.html", {"data":docs})

def build_delete_view(request, pk):
	doc = Document.objects.get(pk=pk)
	doc.delete()
	return redirect("/list_models/")

def upload_doc_view(request):
	if request.method=="POST":
		data = request.POST
		form = DocumentForm(data=data, files=request.FILES)
		if form.is_valid():
			form.save()
			return redirect("/list_models")
		else:
			return render(request,"auto/document_form.html",
			{"error":form._errors})

	else:
		form = DocumentForm()
		return render(request,"auto/document_form.html",
			{"form":form})

def upload_predict_view(request):
	if request.method=="POST":
		data = request.POST
		form = PredictDocumentForm(data=data, files=request.FILES)
		if form.is_valid():
			form.save()
			inst = form.instance
			inst.doc_type = "p"
			inst.save()
			return redirect("/list_predictions")
		else:
			return render(request,"auto/document_form.html",
			{"error":form._errors})

	else:
		form = PredictDocumentForm()
		return render(request,"auto/document_form.html",
			{"form":form})

def predict_view(request, pk):
	doc = PredictDocument.objects.get(pk=pk)
	data = predict(doc, doc.doc)
	return HttpResponse(data.to_html())
	
def build_view(request,pk):
	doc = Document.objects.get(pk=pk)
	generate_model(doc)
	return redirect("/list_models")
def predict(doc, parent_doc):
	df_original = get_data(doc)
	df = clean_data(df_original)
	df = encode_data(df)
	#X1, y = split_data(df, doc)
	X1=df
	f=open(os.path.join(get_media_path(),doc.doc.model.name), 'rb')
	model = pickle.load(f)
	predictions = model.predict(X1)
	target = doc.doc.target
	df_original[target]=predictions
	return df_original

def get_media_path():
	return os.path.join(settings.BASE_DIR,"media")

def encode_data(df):
	le=LabelEncoder()
	df2=df.apply(le.fit_transform)
	return df2

def split_data(df,doc):
	target = doc.target
	X1=df.drop([target],axis=1)
	y=df[target]
	return X1,y

def clean_data(df):
	df_cat = df.select_dtypes(include=["object",'datetime64[ns]'])
	df_num=df.select_dtypes(include=[np.number])
	# fill all numerical data null columns with median of that column
	df_num.fillna(df_num.median(),inplace=True)
	for col in df_cat:
		if df_cat[col].isnull().sum()>0:
			mode = df_cat[col].mode()
			if len(mode)>1:
				df_cat[col].fillna(method="ffill",inplace=True)
			else:
				df_cat[col].fillna(mode[0], inplace=True)
	df=pd.concat([df_cat,df_num],axis=1)
	return df
def get_data(doc):
	file_path = os.path.join(get_media_path(),doc.data.name)
	df = pd.read_csv(file_path)
	return df

def generate_model(doc):
	df = get_data(doc)
	df = clean_data(df)
	df = encode_data(df)
	X1, y = split_data(df, doc)
	X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.3)
	Linreg=LinearRegression()
	DecTree=DecisionTreeRegressor()
	RandFor=RandomForestRegressor()
	GBM=GradientBoostingRegressor()
	linearregressionmodel=Linreg.fit(X_train,y_train)
	decissiontreemodel=DecTree.fit(X_train,y_train)
	randomforestmodel=RandFor.fit(X_train,y_train)
	gradientboostingmodel=GBM.fit(X_train,y_train)
	scores = {"decissiontreemodel":decissiontreemodel.score(X_train,y_train),
	          'randomforestmodel':randomforestmodel.score(X_train,y_train),
	          "linearregressionmodel":linearregressionmodel.score(X_train,y_train),
	          "gradientboostingmodel":gradientboostingmodel.score(X_train,y_train)}
	gb_y_pred = gradientboostingmodel.predict(X_test)
	rf_y_pred = randomforestmodel.predict(X_test)
	lm_y_pred = linearregressionmodel.predict(X_test)
	dtm_y_pred = decissiontreemodel.predict(X_test)
	r2scores={"gradientboostingmodel": r2_score(y_test,gb_y_pred),
	          "randomforestmodel": r2_score(y_test,rf_y_pred),
	          "linearregressionmodel": r2_score(y_test,lm_y_pred),
	          "decissiontreemodel": r2_score(y_test,dtm_y_pred)
	         }
	doc.errors = str(r2scores)
	df3=pd.DataFrame({"scores":scores,"r2scores":r2scores})
	final_model = df3.sort_values(by='r2scores').tail(1)['r2scores'].index[0]
	file_name,extension = doc.data.name.split(".")
	file_name = "%s%s.%s"%(file_name,int(time()),extension)
	f=open(os.path.join(get_media_path(), file_name ),"wb")
	pickle.dump(eval(final_model),f)
	f.close()
	doc.model = file_name
	doc.save()
	return eval(final_model)