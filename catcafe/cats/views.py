from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Cat, Staff, StaffReview, MenuItem, ContactMessage


def index(request):
    featured_cats = Cat.objects.filter(status='available').order_by('?')[:3]
    stats = {
        'total_cats': Cat.objects.count(),
        'available_cats': Cat.objects.filter(status='available').count(),
        'total_adopted': Cat.objects.filter(status='adopted').count(),
    }

    context = {
        'featured_cats': featured_cats,
        'stats': stats,
    }
    return render(request, 'index.html', context)


def cats_list(request):
    cats = Cat.objects.exclude(status='adopted').order_by('status', 'name')
    gender_filter = request.GET.get('gender', '')
    age_filter = request.GET.get('age', '')
    status_filter = request.GET.get('status', '')
    temperament_filter = request.GET.get('temperament', '')

    if gender_filter:
        cats = cats.filter(gender=gender_filter)
    if age_filter:
        cats = cats.filter(age=age_filter)
    if status_filter:
        cats = cats.filter(status=status_filter)
    if temperament_filter:
        cats = cats.filter(temperament=temperament_filter)

    stats = {
        'total_cats': Cat.objects.exclude(status='adopted').count(),
        'available_cats': Cat.objects.filter(status='available').count(),
        'adopted_this_month': Cat.objects.filter(
            status='adopted',
        ).count(),
        'total_adopted': Cat.objects.filter(status='adopted').count(),
    }

    context = {
        'cats': cats,
        'stats': stats,
        'filters': {
            'gender': gender_filter,
            'age': age_filter,
            'status': status_filter,
            'temperament': temperament_filter,
        }
    }
    return render(request, 'cats.html', context)


def cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    context = {
        'cat': cat,
    }
    return render(request, 'cats_detail.html', context)


def staff_page(request):
    staff_members = Staff.objects.filter(is_active=True).order_by('position')

    thirty_days_ago = timezone.now() - timedelta(days=30)
    latest_reviews = StaffReview.objects.filter(
        created_at__gte=thirty_days_ago,
        is_approved=True
    ).select_related('staff').order_by('-created_at')[:6]

    context = {
        'staff_members': staff_members,
        'latest_reviews': latest_reviews,
    }
    return render(request, 'staff.html', context)


def submit_review(request):
    staff_id = request.GET.get('staff_id')
    selected_staff = None

    if staff_id:
        try:
            selected_staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            pass

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')
        staff_id_from_form = request.POST.get('staff')

        if customer_name and review_text and rating and staff_id_from_form:
            try:
                staff = Staff.objects.get(id=staff_id_from_form)
                StaffReview.objects.create(
                    staff=staff,
                    customer_name=customer_name,
                    review=review_text,
                    rating=int(rating)
                )
                return redirect('staff')
            except (Staff.DoesNotExist, ValueError):
                pass

    staff_members = Staff.objects.filter(is_active=True)

    context = {
        'staff_members': staff_members,
        'staff_id': staff_id,
        'selected_staff': selected_staff,
    }
    return render(request, 'reviews.html', context)

def menu_page(request):
    all_items = MenuItem.objects.all()

    menu_by_category = {}

    for item in all_items:
        category_key = item.category

        if category_key not in menu_by_category:
            menu_by_category[category_key] = {
                'items': [],
                'description': get_category_description(category_key)
            }

        menu_by_category[category_key]['items'].append(item)

    context = {
        'menu_by_category': menu_by_category,
    }
    return render(request, 'menu.html', context)


def get_category_description(category_key):
    descriptions = {
        'coffee': 'Ароматный кофе из свежеобжаренных зерен',
        'tea': 'Традиционные и авторские чаи',
        'desserts': 'Сладкие искушения для настоящих гурманов',
        'snacks': 'Легкие закуски к напиткам',
        'cats': 'Специальное меню для наших пушистых гостей',
        'specials': 'Сезонные и специальные предложения',
    }
    return descriptions.get(category_key, '')


def help_page(request):
    faqs = [
        {
            'question': 'Как часто можно приходить волонтером?',
            'answer': 'Вы можете выбрать удобный для вас график. Мы рады помощи как на регулярной основе (1-2 раза в неделю), так и разовым визитам. Главное - предварительно согласовать время визита с координатором.'
        },
        {
            'question': 'Можно ли помочь дистанционно?',
            'answer': 'Да! Мы нуждаемся в помощи с ведением социальных сетей, созданием контента, переводом текстов, дизайном и другими задачами, которые можно выполнять удаленно.'
        },
        {
            'question': 'Какую сумму лучше пожертвовать?',
            'answer': 'Любая сумма важна! 500 рублей - это корм для одного котика на 3 дня, 1500 рублей - полное содержание на месяц, 5000 рублей - помощь в оплате ветеринарных услуг.'
        },
        {
            'question': 'Можно ли привезти корм или вещи без предварительного звонка?',
            'answer': 'Мы рекомендуем всегда звонить заранее, так как у нас может не быть места для хранения или конкретная марка корма может не подходить нашим котикам по рекомендациям ветеринара.'
        },
        {
            'question': 'Предоставляете ли вы документы для налогового вычета?',
            'answer': 'Да, при пожертвовании от 1000 рублей мы можем предоставить все необходимые документы для налогового вычета. Обратитесь к нашему бухгалтеру по email: finance@murcat-cafe.ru'
        }
    ]

    contact_info = {
        'phone': '+7 (999) 123-45-67',
        'telegram': '@murchashij_ugolok',
        'email': 'help@murcat-cafe.ru',
        'volunteer_coordinator': {
            'name': 'Марта',
            'phone': '+7 (999) 765-43-21',
            'email': 'volunteer@murcat-cafe.ru'
        }
    }

    context = {
        'faqs': faqs,
        'contact_info': contact_info,
    }
    return render(request, 'help.html', context)


def locations_page(request):
    locations = [
        {
            'name': 'Основное кафе',
            'address': 'ул. Кошачья, 15',
            'phone': '+7 (999) 123-45-67',
            'hours': 'Пн-Вс: 10:00 - 22:00',
            'description': 'Наше главное кафе в центре города с уютной атмосферой и большим количеством котиков.'
        },
    ]

    context = {
        'locations': locations,
    }
    return render(request, 'locations.html', context)


def contact_form(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )

            messages.success(request, 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.')
            return redirect('index')

        except Exception as e:
            messages.error(request, 'Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте еще раз.')

    return redirect('index')
