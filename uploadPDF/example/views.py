from django.shortcuts import render
from django.http import HttpResponse
from .exampleBack import async_detect_document
from .list import print_list
from .forms import uploadFileForms
from .uploadobj import upload_blob_to_storage

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = uploadFileForms(request.POST, request.FILES) 
        file = request.FILES['file']

        upload_blob_to_storage('kayti0304-new-bucket', file, 'blobFile')
        result = async_detect_document("gs://kayti0304-new-bucket/blobamazon", "gs://kayti0304-bucket-return/sampleoutput/")

        doc_list = result.split()
        f = open("demofile3.txt", "w")
        for word in doc_list:
            f.write(word)
            f.write('\n')
        f.close()

        print_list()

        return HttpResponse('The name of the uploaded file is ' + str(file))
    else:
        form = uploadFileForms()
    return render(request, 'administration/upload.html', {'form': form})