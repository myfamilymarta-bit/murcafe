from django.db import models
from django.utils import timezone


class Cat(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мальчик'),
        ('F', 'Девочка'),
    ]

    AGE_CHOICES = [
        ('kitten', 'Котенок (до 1 года)'),
        ('young', 'Молодой (1-3 года)'),
        ('adult', 'Взрослый (3-8 лет)'),
        ('senior', 'Пожилой (8+ лет)'),
    ]

    STATUS_CHOICES = [
        ('available', 'Ищет дом'),
        ('reserved', 'В процессе'),
        ('adopted', 'Пристроен'),
    ]

    TEMPERAMENT_CHOICES = [
        ('active', 'Активный'),
        ('calm', 'Спокойный'),
        ('playful', 'Игривый'),
        ('affectionate', 'Ласковый'),
        ('shy', 'Стеснительный'),
        ('lazy', 'Ленивый'),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    age = models.CharField(max_length=10, choices=AGE_CHOICES, verbose_name="Возраст")
    breed = models.CharField(max_length=100, blank=True, null=True, verbose_name="Порода")
    description = models.TextField(verbose_name="Описание")
    story = models.TextField(blank=True, verbose_name="История")
    temperament = models.CharField(max_length=20, choices=TEMPERAMENT_CHOICES, verbose_name="Характер")
    good_with_children = models.BooleanField(default=False, verbose_name="Ладит с детьми")
    good_with_other_animals = models.BooleanField(default=False, verbose_name="Ладит с животными")
    health_status = models.TextField(default="Здоров, привит, обработан от паразитов",
                                     verbose_name="Состояние здоровья")
    special_needs = models.TextField(blank=True, verbose_name="Особые потребности")
    vaccinated = models.BooleanField(default=True, verbose_name="Привит")
    sterilized = models.BooleanField(default=True, verbose_name="Стерилизован")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available', verbose_name="Статус")
    arrival_date = models.DateField(default=timezone.now, verbose_name="Дата поступления")
    image = models.ImageField(upload_to='images/', verbose_name="Фото")

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"

    class Meta:
        verbose_name = "Котик"
        verbose_name_plural = "Котики"
        ordering = ['status', 'name']


class Staff(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Менеджер'),
        ('barista', 'Бариста'),
        ('cat_caretaker', 'Грумер'),
        ('vet', 'Ветеринар'),
        ('shef', "Шеф Повар"),
        ('waiter', "Официант")
    ]

    name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name='Должность')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активный сотрудник')

    def get_full_name(self):
        if hasattr(self, 'name') and hasattr(self, 'surname'):
            return f"{self.name} {self.surname}"
        elif hasattr(self, 'full_name'):
            return self.full_name
        else:
            return "Сотрудник"
    def __str__(self):
        return f"{self.name} {self.surname} - {self.get_position_display()}"


class StaffReview(models.Model):
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="Сотрудник")
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    review = models.TextField(verbose_name="Отзыв")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(default=True, verbose_name="Одобрен")

    def __str__(self):
        return f"Отзыв от {self.customer_name} для {self.staff.user.get_full_name()}"

    class Meta:
        verbose_name = "Отзыв о сотруднике"
        verbose_name_plural = "Отзывы о сотрудниках"
        ordering = ['-created_at']


class MenuItem(models.Model):
    VEGETARIAN_CHOICES = [
        ('none', 'Содержит животные продукты'),
        ('vegetarian', 'Вегетарианское'),
        ('vegan', 'Веганское'),
    ]

    ALLERGEN_CHOICES = [
        ('gluten', 'Глютен'),
        ('milk', 'Молоко'),
        ('eggs', 'Яйца'),
        ('nuts', 'Орехи'),
        ('soy', 'Соя'),
        ('fish', 'Рыба'),
        ('shellfish', 'Морепродукты'),
    ]

    CATEGORY_CHOICES = [
        ('coffee', '☕ Кофе и напитки'),
        ('tea', '🍵 Чайная карта'),
        ('desserts', '🍰 Десерты'),
        ('snacks', '🥪 Закуски и сэндвичи'),
        ('cats', '🐱 Лакомства для котиков'),
        ('specials', '⭐ Специальные предложения'),
    ]

    CATEGORY_ORDER = {
        'coffee': 1,
        'tea': 2,
        'desserts': 3,
        'snacks': 4,
        'cats': 5,
        'specials': 6,
    }

    CATEGORY_DESCRIPTIONS = {
        'coffee': 'Ароматный кофе и освежающие напитки',
        'tea': 'Традиционные и авторские чаи',
        'desserts': 'Сладкие искушения для настоящих гурманов',
        'snacks': 'Легкие закуски и сытные сэндвичи',
        'cats': 'Специальные лакомства для наших пушистых жителей',
        'specials': 'Сезонные предложения и акции',
    }

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Изображение")
    vegetarian = models.CharField(max_length=20, choices=VEGETARIAN_CHOICES, default='none', verbose_name="Тип питания")
    allergens = models.CharField(max_length=200, blank=True, verbose_name="Аллергены")
    volume = models.CharField(max_length=50, blank=True, verbose_name="Объем/Вес")
    is_available = models.BooleanField(default=True, verbose_name="Доступно")

    def get_allergens_list(self):
        if self.allergens:
            return self.allergens.split(',')
        return []

    def get_category_description(self):
        return self.CATEGORY_DESCRIPTIONS.get(self.category, '')

    def get_category_order(self):
        return self.CATEGORY_ORDER.get(self.category, 99)

    def __str__(self):
        return f"{self.name} - {self.price}₽"

    class Meta:
        verbose_name = "Позиция меню"
        verbose_name_plural = "Позиции меню"
        ordering = ['category', 'name']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name} - {self.subject}"

    class Meta:
        verbose_name = "Контактное сообщение"
        verbose_name_plural = "Контактные сообщения"
        ordering = ['-created_at']
