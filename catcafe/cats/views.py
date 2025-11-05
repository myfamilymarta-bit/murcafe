from django.shortcuts import render, get_object_or_404
from django.db.models import Q


def index(request):
    featured_cats = Cat.objects.filter(status='available')[:3]
    context = {
        'featured_cats': featured_cats,
    }
    return render(request, 'index.html', context)


def cats_list(request):
    cats = Cat.objects.all().order_by('status', 'name')

    # Статистика для отображения
    stats = {
        'total_cats': Cat.objects.count(),
        'available_cats': Cat.objects.filter(status='available').count(),
        'adopted_this_month': Cat.objects.filter(
            status='adopted',
            adoption_date__month=timezone.now().month
        ).count(),
        'total_adopted': Cat.objects.filter(status='adopted').count(),
    }

    context = {
        'cats': cats,
        'stats': stats,
    }
    return render(request, 'cats.html', context)


def cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)

    # Похожие котики (по характеру и возрасту)
    similar_cats = Cat.objects.filter(
        Q(temperament=cat.temperament) | Q(age=cat.age),
        status='available'
    ).exclude(id=cat.id)[:4]

    context = {
        'cat': cat,
        'similar_cats': similar_cats,
    }
    return render(request, 'cats_detail.html', context)
