from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
import os
import requests
from apps.games.models import Animal, AnimalMatchingLevel, AnimalMatchingGame
from io import BytesIO
from PIL import Image

class Command(BaseCommand):
    help = 'Download animal images and assign them to game levels'

    def handle(self, *args, **options):
        self.stdout.write('Downloading animal images...')
        
        # Animal data with image URLs (using free stock images)
        animals_data = [
            {
                'name': 'Lion',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Elephant',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1557050543-4d5f2e07c346?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Giraffe',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Zebra',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Tiger',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Monkey',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Penguin',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Dolphin',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Cat',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Dog',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Horse',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Cow',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Pig',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Sheep',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Chicken',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Duck',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Rabbit',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Hamster',
                'category': 'domestic',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Bird',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Fish',
                'category': 'wild',
                'image_url': 'https://images.unsplash.com/photo-1549366021-9f761d450615?w=300&h=300&fit=crop&crop=center'
            },
        ]
        
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'games', 'animals')
        os.makedirs(media_dir, exist_ok=True)
        
        # Download and create animals
        animals = []
        for animal_data in animals_data:
            animal, created = Animal.objects.get_or_create(
                name=animal_data['name'],
                defaults={
                    'category': animal_data['category'],
                    'is_active': True
                }
            )
            
            # Download image if animal doesn't have one
            if not animal.image or not animal.image.name:
                try:
                    self.stdout.write(f'Downloading image for {animal.name}...')
                    response = requests.get(animal_data['image_url'], timeout=10)
                    response.raise_for_status()
                    
                    # Process image
                    img = Image.open(BytesIO(response.content))
                    img = img.convert('RGB')
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)
                    
                    # Save to BytesIO
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG', quality=85)
                    img_io.seek(0)
                    
                    # Save to model
                    filename = f"{animal.name.lower().replace(' ', '_')}.jpg"
                    animal.image.save(filename, ContentFile(img_io.getvalue()), save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ Downloaded image for {animal.name}'))
                    
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Failed to download image for {animal.name}: {e}'))
                    # Create a placeholder image
                    self.create_placeholder_image(animal)
            else:
                self.stdout.write(f'✓ {animal.name} already has an image')
            
            animals.append(animal)
        
        # Assign animals to levels based on difficulty
        self.assign_animals_to_levels(animals)
        
        self.stdout.write(self.style.SUCCESS('Animal images setup completed!'))

    def create_placeholder_image(self, animal):
        """Create a simple placeholder image for animals"""
        try:
            # Create a simple colored square with animal name
            img = Image.new('RGB', (300, 300), color=(100, 150, 200))
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Save to model
            filename = f"{animal.name.lower().replace(' ', '_')}_placeholder.jpg"
            animal.image.save(filename, ContentFile(img_io.getvalue()), save=True)
            
            self.stdout.write(f'✓ Created placeholder for {animal.name}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create placeholder for {animal.name}: {e}'))

    def assign_animals_to_levels(self, animals):
        """Assign animals to game levels based on difficulty"""
        # Get all game levels
        levels = AnimalMatchingGame.objects.filter(is_active=True).order_by('level')
        
        for level in levels:
            try:
                level_config = AnimalMatchingLevel.objects.get(game=level)
                
                # Calculate how many animals we need for this level
                grid_size = level_config.grid_size
                num_animals_needed = (grid_size * grid_size) // 2
                
                # Get animals for this level (use different animals for different levels)
                start_index = (level.level - 1) * 4  # Different animals for each level
                level_animals = animals[start_index:start_index + num_animals_needed]
                
                # If we don't have enough animals, cycle through them
                if len(level_animals) < num_animals_needed:
                    level_animals = animals[:num_animals_needed]
                
                # Assign animals to level
                level_config.animals.set(level_animals)
                
                self.stdout.write(f'✓ Assigned {len(level_animals)} animals to Level {level.level}')
                
            except AnimalMatchingLevel.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠ Level configuration not found for Level {level.level}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error assigning animals to Level {level.level}: {e}')) 