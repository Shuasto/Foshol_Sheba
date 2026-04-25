from django.core.management.base import BaseCommand
from core.models import Crop, MarketPrice
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populates the database with initial market price data'

    def handle(self, *args, **kwargs):
        markets = ["Kawran Bazar, Dhaka", "Savar Bazar, Dhaka", "Pabna Sadar", "Rajshahi City Market", "Bogura Central Market", "Dinajpur Road"]
        
        crops_available = list(Crop.objects.all())
        if not crops_available:
            self.stdout.write(self.style.ERROR("No crops found! Please run crop_populate first."))
            return

        # 10 Price objects
        price_data_list = []
        for _ in range(10):
            crop = random.choice(crops_available)
            market = random.choice(markets)
            # Realistic price range per kg
            price = Decimal(random.randint(20, 150))
            
            price_data_list.append({
                "crop": crop,
                "market_name": market,
                "price_per_kg": price
            })

        for data in price_data_list:
            # We use update_or_create but market prices change daily, 
            # so usually we might want to just create new entries, 
            # but for seeding we will match by crop and market
            obj, created = MarketPrice.objects.update_or_create(
                crop=data['crop'],
                market_name=data['market_name'],
                defaults={'price_per_kg': data['price_per_kg']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {obj.crop.name_en} at {obj.market_name} - {obj.price_per_kg} TK'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated: {obj.crop.name_en} at {obj.market_name} - {obj.price_per_kg} TK'))

        self.stdout.write(self.style.SUCCESS('Market price population complete!'))
