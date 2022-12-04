from django.core.management.base import BaseCommand, CommandError
from app1.models import Post, Category

class Command(BaseCommand):
    help = 'Удаление всех новостей заданной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):

        answer = input(f'Вы действительно хотите удалить новости категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено, удаление не будет выполняться'))
        else:
            try:
                category = Category.objects.get(name=options['category'])
                self.stdout.write(self.style.SUCCESS(f'категория {category.name} выбрана для удаления'))
                Post.objects.filter(postCategory=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Все новости в категории {category.name} успешно удалены!'))

            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {options["category"]}.'))


