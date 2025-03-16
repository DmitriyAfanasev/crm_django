from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from service_product.models import Product


class Command(BaseCommand):
    """Создаёт роли и назначает разрешения."""

    help = "Создаёт роли и назначает разрешения"

    def handle(self, *args, **kwargs) -> None:
        groups = {
            "operator": [
                "add_lead",
                "change_lead",
                "view_lead",
                "delete_lead",
            ],
            "marketer": [
                "add_product",
                "change_product",
                "delete_product",
                "view_product",
                "add_adscompany",
                "change_adscompany",
                "delete_adscompany",
                "view_adscompany",
            ],
            "manager": [
                "add_contract",
                "change_contract",
                "delete_contract",
                "view_contract",
                "add_customer",
                "view_lead",
            ],
        }

        model_to_app_label = {
            "lead": ("leads", "lead"),
            "product": ("service_product", "product"),
            "adscompany": ("ads", "adscompany"),
            "contract": ("contracts", "contract"),
            "customer": ("customers", "customer"),
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            self.stdout.write(
                self.style.WARNING(
                    f'Группа "{group_name}" {"создана" if created else "уже существует"}'
                )
            )

            for perm in permissions:
                self.add_permission_to_group(perm, group, model_to_app_label)

            self.stdout.write(
                self.style.SUCCESS(f'Разрешения для группы "{group_name}" назначены')
            )

        self.add_view_statistics_permission()

    def add_permission_to_group(self, perm, group, model_to_app_label):
        """Добавляет указанные права доступа указанной группе."""
        try:
            action, model_name = perm.split("_", 1)
            app_label, model = model_to_app_label.get(model_name, (None, None))
            if not app_label or not model:
                raise ValueError(f"Неправильное имя модели: {model_name}")

            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(
                content_type=content_type, codename=perm
            )
            group.permissions.add(permission)
        except (ContentType.DoesNotExist, Permission.DoesNotExist, ValueError) as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при добавлении разрешения '{perm}': {e}")
            )

    @staticmethod
    def add_view_statistics_permission():
        """Добавляет право просмотра статистики всем группам."""
        can_view_statistics, _ = Permission.objects.get_or_create(
            codename="can_view_statistics",
            name="Can view statistics",
            content_type=ContentType.objects.get_for_model(Product),
        )

        for group in Group.objects.all():
            if can_view_statistics in group.permissions.all():
                group.permissions.add(can_view_statistics)
