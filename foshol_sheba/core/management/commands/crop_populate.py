from django.core.management.base import BaseCommand
from core.models import Crop

class Command(BaseCommand):
    help = 'Populates the database with initial crop data'

    def handle(self, *args, **kwargs):
        crops = [
            {
                "name_en": "Paddy",
                "name_bn": "ধান",
                "image": "crops/paddy.png",
                "description_en": "Paddy is the most important food crop of Bangladesh, covering about 75% of the total cropped area.",
                "description_bn": "ধান বাংলাদেশের সবচেয়ে গুরুত্বপূর্ণ খাদ্যশস্য, যা মোট আবাদকৃত জমির প্রায় ৭৫% জুড়ে রয়েছে।"
            },
            {
                "name_en": "Potato",
                "name_bn": "আলু",
                "image": "crops/potato.png",
                "description_en": "Potato is one of the most important vegetable crops in Bangladesh.",
                "description_bn": "আলু বাংলাদেশের অন্যতম গুরুত্বপূর্ণ সবজি জাতীয় ফসল।"
            },
            {
                "name_en": "Tomato",
                "name_bn": "টমেটো",
                "image": "crops/tomato.png",
                "description_en": "Tomato is a popular and nutritious vegetable grown across the country.",
                "description_bn": "টমেটো দেশের সর্বত্র চাষ করা একটি জনপ্রিয় ও পুষ্টিকর সবজি।"
            },
            {
                "name_en": "Wheat",
                "name_bn": "গম",
                "image": "crops/wheat.png",
                "description_en": "Wheat is the second most important cereal crop in Bangladesh after rice.",
                "description_bn": "ধানের পর গম বাংলাদেশের দ্বিতীয় গুরুত্বপূর্ণ দানাদার ফসল।"
            },
            {
                "name_en": "Mango",
                "name_bn": "আম",
                "image": "crops/mango.png",
                "description_en": "Mango is known as the king of fruits in Bangladesh, particularly grown in Rajshahi and Chapainawabganj.",
                "description_bn": "আম বাংলাদেশে ফলের রাজা হিসেবে পরিচিত, বিশেষ করে রাজশাহী ও চাঁপাইনবাবগঞ্জে প্রচুর উৎপন্ন হয়।"
            },
            {
                "name_en": "Jute",
                "name_bn": "পাট",
                "image": "crops/jute.png",
                "description_en": "Jute is known as the 'Golden Fibre' of Bangladesh and is a major cash crop.",
                "description_bn": "পাটকে বাংলাদেশের 'সোনালী আঁশ' বলা হয় এবং এটি একটি প্রধান অর্থকরী ফসল।"
            },
            {
                "name_en": "Onion",
                "name_bn": "পেঁয়াজ",
                "image": "crops/onion.png",
                "description_en": "Onion is an essential spice crop used daily in Bangladeshi cuisine.",
                "description_bn": "পেঁয়াজ একটি অত্যাবশ্যকীয় মসলা জাতীয় ফসল যা বাংলাদেশী রান্নায় প্রতিদিন ব্যবহৃত হয়।"
            },
            {
                "name_en": "Brinjal",
                "name_bn": "বেগুন",
                "image": "crops/brinjal.png",
                "description_en": "Brinjal is a common vegetable in Bangladesh, available year-round.",
                "description_bn": "বেগুন বাংলাদেশের একটি সাধারণ সবজি যা সারা বছর পাওয়া যায়।"
            }
        ]

        for crop_data in crops:
            obj, created = Crop.objects.update_or_create(
                name_en=crop_data['name_en'],
                defaults={
                    'name_bn': crop_data['name_bn'],
                    'image': crop_data.get('image'),
                    'description_en': crop_data['description_en'],
                    'description_bn': crop_data['description_bn'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created crop: {obj.name_en}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated crop: {obj.name_en}'))

        self.stdout.write(self.style.SUCCESS('Crop population complete!'))
