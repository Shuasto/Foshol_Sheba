from django.core.management.base import BaseCommand
from core.models import Badge

class Command(BaseCommand):
    help = 'Populate the Badge model with default badges'

    def handle(self, *args, **kwargs):
        badges_data = [
            {
                'title': 'নতুন কৃষক',
                'description': 'আপনার প্রথম ফসল স্ক্যান করেছেন।',
                'badge_type': 'scan',
                'required_count': 1,
                'icon': '🌱'
            },
            {
                'title': 'নিয়মিত পর্যবেক্ষক',
                'description': '৫টি ফসল স্ক্যান সম্পন্ন করেছেন।',
                'badge_type': 'scan',
                'required_count': 5,
                'icon': '🌿'
            },
            {
                'title': 'খামার বিশেষজ্ঞ',
                'description': '২০টি ফসল স্ক্যান সম্পন্ন করেছেন।',
                'badge_type': 'scan',
                'required_count': 20,
                'icon': '🌳'
            },
            {
                'title': 'নতুন মুখ',
                'description': 'ফোরামে আপনার প্রথম পোস্ট করেছেন।',
                'badge_type': 'post',
                'required_count': 1,
                'icon': '💬'
            },
            {
                'title': 'ফোরাম লিডার',
                'description': '৫টি আলোচনা শুরু করেছেন।',
                'badge_type': 'post',
                'required_count': 5,
                'icon': '📢'
            },
            {
                'title': 'কমিউনিটি আইকন',
                'description': '১৫টি আলোচনা শুরু করেছেন।',
                'badge_type': 'post',
                'required_count': 15,
                'icon': '👑'
            },
            {
                'title': 'সাহায্যকারী',
                'description': 'আপনার প্রথম মন্তব্য করেছেন।',
                'badge_type': 'comment',
                'required_count': 1,
                'icon': '🤝'
            },
            {
                'title': 'বুদ্ধিমান পরামর্শক',
                'description': '১০টি মন্তব্য করেছেন।',
                'badge_type': 'comment',
                'required_count': 10,
                'icon': '💡'
            },
            {
                'title': 'ফোরাম নক্ষত্র',
                'description': '৩০টি মন্তব্য করেছেন।',
                'badge_type': 'comment',
                'required_count': 30,
                'icon': '🌟'
            },
            {
                'title': 'অভিজ্ঞ কৃষক',
                'description': '১০টি ফসল স্ক্যান এবং ৫টি পোস্ট সম্পন্ন করেছেন।',
                'badge_type': 'scan',
                'required_count': 10,
                'icon': '🚜'
            }
        ]

        for data in badges_data:
            badge, created = Badge.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created badge: {badge.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated badge: {badge.title}'))
