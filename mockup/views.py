from django.shortcuts import render, redirect, HttpResponse
from textile.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

import os, json

from mockup import dominant_color
from mockup import read_image_from_db


def index(request):
    return render(request, 'mockups.html')
    # return render(request, 'gomlek.html')


def show_layers(request, image_name):
    image_path = os.path.join(BASE_DIR, 'static', 'layers', image_name, 'image.json')
    if os.path.isfile(image_path):
        with open(image_path, "r") as read_file:
            context = json.load(read_file)
        return render(request, 'show_layers.html', context)
    else:
        response = read_image_from_db.read_image_from_db(image_name)
        if response == "True":
            with open(image_path, "r") as read_file:
                context = json.load(read_file)
            return render(request, 'show_layers.html', context)
        else:
            return HttpResponse(response)


def upload_image_page(request):
    files = os.listdir(MEDIA_ROOT)
    if len(files):
        for file in files:
            os.remove(os.path.join(MEDIA_ROOT, file))
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
        except Exception as e:
            print("Hata: ", e)
        else:
            print("Successful ")
            # return render(request, 'dominant_color.html', {'file_name': myfile.name})
            return redirect('dominant_color', )
    return render(request, 'upload_image.html')


def dominant_color_page(request):
    try:
        files = os.listdir(MEDIA_ROOT)
        if len(files) == 0:
            return HttpResponse("İlk önce fotoğraf yükleyin.")
        filename = files[0]

        image_with_abs_path = os.path.join(MEDIA_ROOT, filename)
        image_with_rel_path = os.path.join(MEDIA_URL, filename)

        # images_count = len(files)

        colors = dominant_color.get_dominant_colors(image_with_abs_path)

        # return render(request, 'dominant_color.html', {'images': images_with_path, 'images_count': images_count})

    except Exception as e:
        print("Hata: ", e)
    else:
        return render(request, 'dominant_color.html', {'colors': colors, 'file': image_with_rel_path})


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
            image_list += string.format(os.path.join(path, image), image, image)

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

        pattern_path = os.path.join(BASE_DIR, 'media', filename)
        patterns_path = os.path.join(BASE_DIR, 'static', 'images', 'pattern', myfile.name)

        print(pattern_path)
        print(patterns_path)
        os.rename(pattern_path, patterns_path)
        return redirect('index')
        # return render(request, 'core/simple_upload.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })

    # return render(request, 'core/simple_upload.html')
