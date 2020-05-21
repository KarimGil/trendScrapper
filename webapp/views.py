from django.shortcuts import render, HttpResponse
import pandas as pd
from pytrends.request import TrendReq
from webapp.models import CourseVideos
import glob
import json

loc = ""

# Create your views here.
def index(request):

    
    return render(request,'index.html')

def new_search(request):
    request.session['myimg']= []
    # myimg = []
   
    pytrend = TrendReq()

    getFile = request.FILES['file']
    keywordFile = CourseVideos(imageFile=getFile)
    keywordFile.save()

    # data = CourseVideos.objects.get(VideoId=1)
    a = keywordFile.imageFile.path
    book = pd.read_excel(a,"Sheet1")
    keywords = book['keywords'].values.tolist()

    final_postings = []

    for i in keywords:
        country = request.POST['country']
        time = request.POST['time']
        try:
            pytrend.build_payload(
                    kw_list=[i],
                    cat=0,
                    timeframe=time,
                    geo=country,
                    gprop='')
            data = pytrend.interest_over_time()

            data= data.drop(labels=['isPartial'],axis='columns')
            image = data.plot(title = i+' on Google Trends ')
                
            fig = image.get_figure()
            figure = fig.savefig('upload/data/'+i+'.png')
            request.session['myimg'].append('upload/data/'+i+'.png')
                
            graph = CourseVideos(graphImage=image)
            graph.save()
            final_postings.append(graph)
            data.to_csv('Py_VS_R.csv', encoding='utf_8_sig')
        except:
            
            print("Data for " +i+ " is not available")



    return render(request,'new_search.html')

