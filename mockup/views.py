from django.shortcuts import render, redirect
from textile.settings import BASE_DIR
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

import os


def index(request):
    return render(request, 'mockups.html')
    # return render(request, 'gomlek.html')


def load_images(request):
    image_list = ""
    string = """<li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <img src="{}" height="70" width="70" class="pattern"  id="pattern_{}">

              </div>
              <button type="button" class="delete-img btn btn-default" id="{}">
                <span class="input-group-text"><i class="fa fa-trash-alt"></i></span>
              </button>
              </li>
              """
    path = os.path.join('static', 'images', 'pattern')
    images = os.listdir(path)
    for image in images:
        image_name, extension = image.split(".")
        if extension == "png" or extension == "jpg" or extension == "jpeg":
            image_list += string.format(os.path.join(path, image),image, image)

    data = {
        'image_list': image_list,
    }
    return JsonResponse(data)


def delete_image(request):

    try:
        image_name = request.GET.get('image_name')
        image_path = os.path.join(BASE_DIR, 'static', 'images', 'pattern', image_name)
        os.remove(image_path)
    except Exception as e:
        response = False
    else:
        response = True
    data = {
        'response': response
    }
    return JsonResponse(data)


def upload_pattern(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        pattern_path = os.path.join(BASE_DIR,'media', filename)
        patterns_path = os.path.join(BASE_DIR, 'static', 'images', 'pattern', myfile.name)

        print(pattern_path)
        print(patterns_path)
        os.rename(pattern_path, patterns_path)
        return redirect('index')
        # return render(request, 'core/simple_upload.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })

    # return render(request, 'core/simple_upload.html')