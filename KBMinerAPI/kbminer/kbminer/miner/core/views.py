from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import sys
from subprocess import run,PIPE
from django.http import HttpResponse
from io import BytesIO
# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


# def upload(request):
#     context = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = OverwriteStorage()
#         filename = fs.save(uploaded_file.name, uploaded_file)
#         fileurl = fs.open(filename)
#         templateurl = fs.url(filename)
#         print("file raw url", filename)
#         print("file full url", fileurl)
#         print("template url", templateurl)
#         excel = run(
#             [sys.executable, 'D://Work//KB-Mining//Hecate//KBMinerAPI//kbminer//kbminer//miner//core//example.py',
#              str(filename)], shell=False, stdout=PIPE)
#         print(excel.stdout)
#         context['url'] = excel.stdout
#     return render(request, 'upload.html', context)


def button(request):
    return render(request,'home.html')

def external(request):
    excel=request.FILES['document']
    fs=OverwriteStorage()
    filename=fs.save(excel.name,excel)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    print("file raw url",filename)
    print("file full url", fileurl)
    print("template url",templateurl)
    out= run([sys.executable,'D://Work//KB-Mining//Hecate//KBMinerAPI//kbminer//kbminer//miner//core//example.py',str(fileurl),str(filename)],shell=False,stdout=PIPE)
    file_path = './miner/core/Output/out.xlsx'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename=mywebsitename.xlsx'
            return response
    else:
        pass


