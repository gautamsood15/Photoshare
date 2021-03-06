from django.shortcuts import render, redirect
from .models import Category, Photo

# Create your views here.


def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__contains=category)





    categories = Category.objects.all()
    

    context = {'categories': categories, 'photos': photos}
    return render(request, "photos/gallery.html", context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    
    if request.method == 'POST':
        Photo.objects.filter(id=pk).delete()
        return redirect('gallery')
        

    return render(request, "photos/photo.html", {'photo': photo})

def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )

        return redirect('gallery')


    context = {'categories': categories}
    return render(request, "photos/add.html", context)


def editPhoto(request, pk):

    photo = Photo.objects.get(id=pk)
    categories = Category.objects.all()

    

    if request.method == 'POST':
        data = request.POST
        print(data)

        category = Category.objects.get(name=data['category'])

        photo.category = category
        photo.description = data['description']
        photo.save()

         
        return redirect('photo', pk=pk)

    context = {'photo': photo, 'categories': categories}
    return render(request, "photos/edit.html", context)