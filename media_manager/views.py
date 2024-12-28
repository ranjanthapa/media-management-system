import os
from pyexpat.errors import messages
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from media_manager.models import MediaFile
from utils.validationExeception import FileValidationError


def home(request):
    errors = [] 
    allFile = MediaFile.objects.all()
    
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('files')
        
        # Check file count limit
        if len(files) > 10:
            errors.append("You cannot upload more than 10 files at a time.")
        
        errors.extend(validate_file(files))  
        
        if not errors:
            save_files(files)


        print("Error displayoing", errors)

    return render(request, 'home.html', {'errors': errors, 'files': allFile})


def validate_file(files):
    errors = []
    valid_extension = ['mp3', 'mp4', 'jpg', 'png', 'gif']

    if len(files) > 10: 
        errors.append("Select 10 files or less at a time")
        return errors

    for file in files:
        try:
            extension = file.name.split('.')[-1].lower()
            if extension not in valid_extension:
                raise FileValidationError(f"File extension of not supported.")
            
            if file.size > 10 * 1024 * 1024 or file.size < 100 * 1024:
                raise FileValidationError(f"File size of  must be between 100KB and 10MB.")
        
        except FileValidationError as e:
            print(e)
            errors.append(e.args[0])  
            break

    return errors



def save_files(files):
    for file in files:
        print("File are on process of save")
        MediaFile.objects.create(
            name=file.name,
            size=file.size,
            file=file, 
            category=get_file_category(file)  
        )


def get_file_category(file):
    extension = file.name.split('.')[-1].lower()
    if extension in ['mp3', 'mp4']:
        return 'Audio/Video'
    else:
        return 'Image'
    
def delete_file(request, id):
    print(id)
    file = MediaFile.objects.get(id=id)
    file.delete()
    return redirect("home")



def view_file(request, file_id):
    try:
        file = MediaFile.objects.get(id=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

        if not os.path.exists(file_path):
            raise Http404("File not found")

        content_type = 'application/octet-stream'  # Default
        if file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            content_type = 'image/jpeg' 
        elif file.name.lower().endswith('.pdf'):
            content_type = 'application/pdf'

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{file.name}"'
            return response

    except MediaFile.DoesNotExist:
        raise Http404("File does not exist")