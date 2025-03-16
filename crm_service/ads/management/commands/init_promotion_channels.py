from django.utils.translation import gettext_lazy as _

from django.core.management.base import BaseCommand
from ads.models_as_description import PromotionChannel


class Command(BaseCommand):
    """
    Команды:
        ./manage.py init_promotion_channels

        python manage.py init_promotion_channels

    Создаёт каналы продвижения для рекламных компаний.
    Вызовите эту команду перед созданием первых рекламных компаний,
    или же вы можете создать свои собственные каналы.

    Заметка:
        Если каналы уже созданы, то дубликатов не появился, но выведется оповещение:
            Promotion channel already exists: Social Media
    """

    help = "Initialize standard promotion channels in the database."

    def handle(self, *args, **kwargs):
        standard_channels = [
            {
                "name": _("Social Media"),
                "description": _(
                    "Promotion through social networks like Facebook, Instagram, etc."
                ),
            },
            {
                "name": _("Search Engines"),
                "description": _(
                    "Promotion through search engines like Google, Bing, etc."
                ),
            },
            {
                "name": _("Email Marketing"),
                "description": _("Promotion through email newsletters."),
            },
            {
                "name": _("Contextual Advertising"),
                "description": _("Promotion through contextual ads on websites."),
            },
            {
                "name": _("Display Advertising"),
                "description": _("Promotion through display ads on websites."),
            },
            {
                "name": _("Offline Channels"),
                "description": _(
                    "Promotion through offline methods like billboards, flyers, etc."
                ),
            },
            {
                "name": _("Partnership Programs"),
                "description": _(
                    "Promotion through partnerships with other companies."
                ),
            },
            {
                "name": _("Messengers"),
                "description": _(
                    "Promotion through messaging apps like WhatsApp, Telegram, etc."
                ),
            },
            {
                "name": _("Own Channels"),
                "description": _(
                    "Promotion through company-owned channels like blogs, websites, etc."
                ),
            },
        ]

        for channel_data in standard_channels:
            channel, created = PromotionChannel.objects.get_or_create(
                name=channel_data["name"],
                defaults={"description": channel_data["description"]},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created promotion channel: {channel_data["name"]}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Promotion channel already exists: {channel_data["name"]}'
                    )
                )
