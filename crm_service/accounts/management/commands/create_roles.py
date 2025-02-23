from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from service_product.models import Product


# TODO доделать команды для создания ролей. И возможно перенести из accounts в более логичное приложение.
class Command(BaseCommand):
    help = "Создаёт роли и назначает разрешения"

    def handle(self, *args, **kwargs):
        # Создаём группы
        groups = {
            "Administrator": [
                "add_user",
                "change_user",
                "delete_user",
                "add_group",
                "change_group",
                "delete_group",
            ],
            "Operator": [
                "add_client",
                "change_client",
                "delete_client",
            ],
            "Marketer": [
                "add_product",
                "change_product",
                "delete_product",
                "add_campaign",
                "change_campaign",
                "delete_campaign",
            ],
            "Manager": [
                "add_contract",
                "change_contract",
                "delete_contract",
                "change_client",
            ],
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Группа "{group_name}" уже существует')
                )

            for perm in permissions:
                try:
                    app_label, codename = perm.split("_", 1)
                    content_type = ContentType.objects.get(app_label=app_label)
                    permission = Permission.objects.get(
                        content_type=content_type, codename=codename
                    )
                    group.permissions.add(permission)
                except (ContentType.DoesNotExist, Permission.DoesNotExist):
                    self.stdout.write(
                        self.style.ERROR(f'Разрешение "{perm}" не найдено')
                    )

            self.stdout.write(
                self.style.SUCCESS(f'Разрешения для группы "{group_name}" назначены')
            )

        # Общее разрешение для просмотра статистики
        can_view_statistics, _ = Permission.objects.get_or_create(
            codename="can_view_statistics",
            name="Can view statistics",
            content_type=ContentType.objects.get_for_model(
                Product
            ),  # Модель для привязки разрешения
        )
        for group in Group.objects.all():
            group.permissions.add(can_view_statistics)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Разрешение "can_view_statistics" добавлено для группы "{group.name}"'
                )
            )
