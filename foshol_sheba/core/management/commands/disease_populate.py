from django.core.management.base import BaseCommand
from core.models import Crop, Disease

class Command(BaseCommand):
    help = 'Populates the database with initial disease data'

    def handle(self, *args, **kwargs):
        diseases = [
            {
                "crop_name": "Paddy",
                "name_en": "Blast Disease",
                "name_bn": "ব্লাস্ট রোগ",
                "description_en": "Blast is one of the most destructive diseases of rice worldwide.",
                "description_bn": "ব্লাস্ট ধানের অন্যতম ধ্বংসাত্মক রোগ যা বিশ্বব্যাপী দেখা যায়।",
                "symptoms_en": "Spindle-shaped spots with grey centers on leaves.",
                "symptoms_bn": "পাতায় ধূসর কেন্দ্রবিশিষ্ট মাকু আকৃতির দাগ দেখা যায়।",
                "organic_remedy_en": "Use resistant varieties and balanced nitrogen fertilization.",
                "organic_remedy_bn": "প্রতিরোধী জাত ব্যবহার করুন এবং সুষম নাইট্রোজেন সার প্রয়োগ করুন।",
                "chemical_treatment_en": "Apply Tricyclazole or Carbendazim fungicides.",
                "chemical_treatment_bn": "ট্রাইসাইক্লাজোল বা কার্বেন্ডাজিম ছত্রাকনাশক প্রয়োগ করুন।",
                "preventative_measures_en": "Avoid excessive nitrogen and keep the field flooded.",
                "preventative_measures_bn": "অতিরিক্ত নাইট্রোজেন সার পরিহার করুন এবং জমিতে পানি ধরে রাখুন।"
            },
            {
                "crop_name": "Paddy",
                "name_en": "Bacterial Leaf Blight",
                "name_bn": "ব্যাকটেরিয়াজনিত পাতা পোড়া রোগ",
                "description_en": "A bacterial disease that causes wilting and yellowing of leaves.",
                "description_bn": "ব্যাকটেরিয়াজনিত রোগ যা পাতা শুকিয়ে যাওয়া ও হলুদ হওয়ার কারণ হয়।",
                "symptoms_en": "Water-soaked streaks that turn yellow or white.",
                "symptoms_bn": "পানিতে ভেজা দাগ যা পরে হলুদ বা সাদা হয়ে যায়।",
                "organic_remedy_en": "Burn infected straw and use clean seeds.",
                "organic_remedy_bn": "আক্রান্ত খড় পুড়িয়ে ফেলুন এবং পরিষ্কার বীজ ব্যবহার করুন।",
                "chemical_treatment_en": "Apply Copper Oxychloride or Streptomycin.",
                "chemical_treatment_bn": "কপার অক্সিক্লোরাইড বা স্ট্রেপ্টোমাইসিন প্রয়োগ করুন।",
                "preventative_measures_en": "Maintain proper drainage and avoid leaf injury.",
                "preventative_measures_bn": "সঠিক নিষ্কাশন ব্যবস্থা রাখুন এবং পাতার আঘাত এড়িয়ে চলুন।"
            },
            {
                "crop_name": "Potato",
                "name_en": "Late Blight",
                "name_bn": "লেট ব্লাইট বা নাবি ধসা রোগ",
                "description_en": "The most serious disease of potato, causing rapid decay of leaves and tubers.",
                "description_bn": "আলুর সবচেয়ে মারাত্মক রোগ, যা পাতা ও কন্দের দ্রুত পচন ঘটায়।",
                "symptoms_en": "Water-soaked lesions on leaf margins with white fungal growth underneath.",
                "symptoms_bn": "পাতার কিনারায় পানিতে ভেজা দাগ এবং নিচে সাদা ছত্রাক দেখা যায়।",
                "organic_remedy_en": "Use neem oil spray and destroy infected plants.",
                "organic_remedy_bn": "নিমের তেল স্প্রে করুন এবং আক্রান্ত গাছ ধ্বংস করুন।",
                "chemical_treatment_en": "Spray Mancozeb or Metalaxyl fungicides.",
                "chemical_treatment_bn": "ম্যানকোজেব বা মেটালাক্সিল ছত্রাকনাশক স্প্রে করুন।",
                "preventative_measures_en": "Plant healthy tubers and ensure good spacing.",
                "preventative_measures_bn": "সুস্থ কন্দ রোপণ করুন এবং যথেষ্ট দূরত্ব বজায় রাখুন।"
            },
            {
                "crop_name": "Tomato",
                "name_en": "Tomato Yellow Leaf Curl",
                "name_bn": "টমেটোর পাতা কোঁকড়ানো রোগ",
                "description_en": "A viral disease spread by whiteflies, leading to stunted growth.",
                "description_bn": "সাদা মাছি দ্বারা ছড়ানো একটি ভাইরাসজনিত রোগ, যা গাছের বৃদ্ধি থামিয়ে দেয়।",
                "symptoms_en": "Upward curling of leaves and yellowing between veins.",
                "symptoms_bn": "পাতার ওপরের দিকে কোঁকড়ানো এবং শিরার মাঝখানে হলুদ হওয়া।",
                "organic_remedy_en": "Use yellow sticky traps to control whiteflies.",
                "organic_remedy_bn": "সাদা মাছি দমনে হলুদ আঠালো ফাঁদ ব্যবহার করুন।",
                "chemical_treatment_en": "Use Imidacloprid to control the vector (whitefly).",
                "chemical_treatment_bn": "বাহক পোকা (সাদা মাছি) দমনে ইমিডাক্লোপ্রিড ব্যবহার করুন।",
                "preventative_measures_en": "Remove weeds and use fine mesh netting.",
                "preventative_measures_bn": "আগাছা পরিষ্কার করুন এবং সূক্ষ্ম জালের নেট ব্যবহার করুন।"
            },
            {
                "crop_name": "Mango",
                "name_en": "Anthracnose",
                "name_bn": "অ্যানথ্রাকনোজ বা ডাই-ব্যাক",
                "description_en": "Causes dark spots on leaves, stems, and fruits.",
                "description_bn": "পাতা, কাণ্ড এবং ফলে কালো দাগ সৃষ্টি করে।",
                "symptoms_en": "Sunken black lesions on ripe fruits and dark spots on leaves.",
                "symptoms_bn": "পাকা ফলে দেবে যাওয়া কালো দাগ এবং পাতায় কালো দাগ।",
                "organic_remedy_en": "Prune infected twigs and spray with bio-fungicides.",
                "organic_remedy_bn": "আক্রান্ত ডাল ছাঁটাই করুন এবং জৈব-ছত্রাকনাশক স্প্রে করুন।",
                "chemical_treatment_en": "Apply Carbendazim or Copper fungicides.",
                "chemical_treatment_bn": "কার্বেন্ডাজিম বা কপার ছত্রাকনাশক প্রয়োগ করুন।",
                "preventative_measures_en": "Control mango hoppers and maintain orchard hygiene.",
                "preventative_measures_bn": "আমের শোষক পোকা দমন করুন এবং বাগানের পরিচ্ছন্নতা বজায় রাখুন।"
            },
            {
                "crop_name": "Wheat",
                "name_en": "Wheat Blast",
                "name_bn": "গমের ব্লাস্ট রোগ",
                "description_en": "A devastating fungal disease that affects the wheat heads.",
                "description_bn": "একটি বিধ্বংসী ছত্রাকজনিত রোগ যা গমের ছড়াকে আক্রান্ত করে।",
                "symptoms_en": "Bleaching of the whole or part of the wheat spike.",
                "symptoms_bn": "গমের ছড়ার পুরো বা অংশবিশেষ সাদা হয়ে যাওয়া।",
                "organic_remedy_en": "Adjust planting dates to avoid humid periods during flowering.",
                "organic_remedy_bn": "ফুলের সময় আর্দ্র সময় এড়াতে রোপণের তারিখ সমন্বয় করুন।",
                "chemical_treatment_en": "Apply Tebuconazole or Azoxystrobin fungicides.",
                "chemical_treatment_bn": "টেবুকোনাজোল বা অ্যাজোক্সিস্ট্রবিন ছত্রাকনাশক প্রয়োগ করুন।",
                "preventative_measures_en": "Burn crop residues and use resistant seeds.",
                "preventative_measures_bn": "ফসলের অবশিষ্টাংশ পুড়িয়ে ফেলুন এবং প্রতিরোধী বীজ ব্যবহার করুন।"
            },
            {
                "crop_name": "Jute",
                "name_en": "Stem Rot",
                "name_bn": "পাটের কাণ্ড পচা রোগ",
                "description_en": "Most common disease of jute reducing quality and yield.",
                "description_bn": "পাটের সবচেয়ে সাধারণ রোগ যা গুণমান ও ফলন কমিয়ে দেয়।",
                "symptoms_en": "Brown or black lesions on the stem near the soil line.",
                "symptoms_bn": "মাটির কাছাকাছি কাণ্ডে বাদামী বা কালো দাগ।",
                "organic_remedy_en": "Rotate crops and use lime in the soil.",
                "organic_remedy_bn": "ফসল পরিবর্তন করুন এবং মাটিতে চুন ব্যবহার করুন।",
                "chemical_treatment_en": "Seed treatment with Carbendazim.",
                "chemical_treatment_bn": "কার্বেন্ডাজিম দিয়ে বীজ শোধন করুন।",
                "preventative_measures_en": "Ensure proper drainage and avoid waterlogging.",
                "preventative_measures_bn": "সঠিক নিষ্কাশন নিশ্চিত করুন এবং জলাবদ্ধতা এড়িয়ে চলুন।"
            },
            {
                "crop_name": "Brinjal",
                "name_en": "Leucinodes orbonalis (Fruit Borer)",
                "name_bn": "ডগা ও ফল ছিদ্রকারী পোকা",
                "description_en": "A major pest that tunnels into shoots and fruits.",
                "description_bn": "একটি প্রধান পোকা যা ডগা ও ফলের ভেতর সুড়ঙ্গ তৈরি করে।",
                "symptoms_en": "Drooping of shoots and holes in fruits with excreta.",
                "symptoms_bn": "ডগা নেতিয়ে পড়া এবং বিষ্ঠাসহ ফলে ছিদ্র।",
                "organic_remedy_en": "Use pheromone traps and remove damaged parts manually.",
                "organic_remedy_bn": "ফেরোমোন ফাঁদ ব্যবহার করুন এবং ক্ষতিগ্রস্ত অংশ হাত দিয়ে সরিয়ে ফেলুন।",
                "chemical_treatment_en": "Apply Spinosad or Chlorantraniliprole.",
                "chemical_treatment_bn": "স্পিনোস্যাড বা ক্লোরঅ্যান্ট্রানিলিপ্রোল প্রয়োগ করুন।",
                "preventative_measures_en": "Intercropping with coriander or fennel.",
                "preventative_measures_bn": "ধনে বা মৌরির সাথে সাথি ফসল চাষ করুন।"
            },
            {
                "crop_name": "Onion",
                "name_en": "Purple Blotch",
                "name_bn": "পার্পল ব্লচ বা বেগুনী দাগ রোগ",
                "description_en": "Fungal disease causing purple lesions on leaves and seed stalks.",
                "description_bn": "ছত্রাকজনিত রোগ যা পাতা ও বীজের কাণ্ডে বেগুনী দাগ সৃষ্টি করে।",
                "symptoms_en": "Small water-soaked lesions that turn purple with white margins.",
                "symptoms_bn": "ছোট পানিতে ভেজা দাগ যা পরে সাদা কিনারাযুক্ত বেগুনী রঙ ধারণ করে।",
                "organic_remedy_en": "Apply wood ash and ensure proper drying after harvest.",
                "organic_remedy_bn": "কাঠের ছাই ব্যবহার করুন এবং সংগ্রহের পর সঠিক শুকানো নিশ্চিত করুন।",
                "chemical_treatment_en": "Spray Mancozeb or Copper Oxychloride.",
                "chemical_treatment_bn": "ম্যানকোজেব বা কপার অক্সিক্লোরাইড স্প্রে করুন।",
                "preventative_measures_en": "Destroy crop fragments and use wide spacing.",
                "preventative_measures_bn": "ফসলের টুকরো ধ্বংস করুন এবং যথেষ্ট দূরত্ব বজায় রাখুন।"
            },
            {
                "crop_name": "Paddy",
                "name_en": "Brown Spot",
                "name_bn": "লিফ স্পট বা বাদামী দাগ রোগ",
                "description_en": "Common disease in poor soils deficient in nutrients.",
                "description_bn": "পুষ্টিহীন দুর্বল মটিতে হওয়া সাধারণ রোগ।",
                "symptoms_en": "Small oval brown spots on leaves.",
                "symptoms_bn": "পাতায় ছোট ডিম্বাকৃতি বাদামী দাগ।",
                "organic_remedy_en": "Improve soil fertility with compost and balanced nutrients.",
                "organic_remedy_bn": "কম্পোস্ট ও সুষম পুষ্টি দিয়ে মাটির উর্বরতা বৃদ্ধি করুন।",
                "chemical_treatment_en": "Apply Mancozeb or Zineb.",
                "chemical_treatment_bn": "ম্যানকোজেব বা জিনেব প্রয়োগ করুন।",
                "preventative_measures_en": "Provide irrigation and manage nutritional deficiencies.",
                "preventative_measures_bn": "সেচ প্রদান করুন এবং পুষ্টির অভাব দূর করুন।"
            }
        ]

        for disease_data in diseases:
            try:
                crop = Crop.objects.get(name_en=disease_data['crop_name'])
                obj, created = Disease.objects.update_or_create(
                    crop=crop,
                    name_en=disease_data['name_en'],
                    defaults={
                        'name_bn': disease_data['name_bn'],
                        'description_en': disease_data['description_en'],
                        'description_bn': disease_data['description_bn'],
                        'symptoms_en': disease_data['symptoms_en'],
                        'symptoms_bn': disease_data['symptoms_bn'],
                        'organic_remedy_en': disease_data['organic_remedy_en'],
                        'organic_remedy_bn': disease_data['organic_remedy_bn'],
                        'chemical_treatment_en': disease_data['chemical_treatment_en'],
                        'chemical_treatment_bn': disease_data['chemical_treatment_bn'],
                        'preventative_measures_en': disease_data['preventative_measures_en'],
                        'preventative_measures_bn': disease_data['preventative_measures_bn'],
                        'is_expert_verified': True
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created disease: {obj.name_en} for {crop.name_en}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated disease: {obj.name_en} for {crop.name_en}'))
            except Crop.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Crop '{disease_data['crop_name']}' does not exist!"))

        self.stdout.write(self.style.SUCCESS('Disease population complete!'))
