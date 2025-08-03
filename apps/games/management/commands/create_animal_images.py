from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
import os
from apps.games.models import Animal, AnimalMatchingLevel, AnimalMatchingGame
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

class Command(BaseCommand):
    help = 'Create animal images with names for the matching game'

    def handle(self, *args, **options):
        self.stdout.write('Creating animal images...')
        
        # Animal data with colors
        animals_data = [
            {'name': 'Lion', 'category': 'wild', 'color': (255, 165, 0)},  # Orange
            {'name': 'Elephant', 'category': 'wild', 'color': (128, 128, 128)},  # Gray
            {'name': 'Giraffe', 'category': 'wild', 'color': (255, 215, 0)},  # Gold
            {'name': 'Zebra', 'category': 'wild', 'color': (255, 255, 255)},  # White
            {'name': 'Tiger', 'category': 'wild', 'color': (255, 140, 0)},  # Dark Orange
            {'name': 'Monkey', 'category': 'wild', 'color': (139, 69, 19)},  # Brown
            {'name': 'Penguin', 'category': 'wild', 'color': (0, 0, 0)},  # Black
            {'name': 'Dolphin', 'category': 'wild', 'color': (0, 191, 255)},  # Deep Sky Blue
            {'name': 'Cat', 'category': 'domestic', 'color': (255, 182, 193)},  # Light Pink
            {'name': 'Dog', 'category': 'domestic', 'color': (210, 180, 140)},  # Tan
            {'name': 'Horse', 'category': 'domestic', 'color': (160, 82, 45)},  # Saddle Brown
            {'name': 'Cow', 'category': 'domestic', 'color': (255, 255, 240)},  # Ivory
            {'name': 'Pig', 'category': 'domestic', 'color': (255, 192, 203)},  # Pink
            {'name': 'Sheep', 'category': 'domestic', 'color': (245, 245, 245)},  # White Smoke
            {'name': 'Chicken', 'category': 'domestic', 'color': (255, 255, 0)},  # Yellow
            {'name': 'Duck', 'category': 'domestic', 'color': (255, 215, 0)},  # Gold
            {'name': 'Rabbit', 'category': 'domestic', 'color': (255, 250, 250)},  # Snow
            {'name': 'Hamster', 'category': 'domestic', 'color': (255, 228, 196)},  # Bisque
            {'name': 'Bird', 'category': 'wild', 'color': (0, 255, 255)},  # Cyan
            {'name': 'Fish', 'category': 'wild', 'color': (0, 0, 255)},  # Blue
        ]
        
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'games', 'animals')
        os.makedirs(media_dir, exist_ok=True)
        
        # Create animals with images
        animals = []
        for animal_data in animals_data:
            animal, created = Animal.objects.get_or_create(
                name=animal_data['name'],
                defaults={
                    'category': animal_data['category'],
                    'is_active': True
                }
            )
            
            # Create image if animal doesn't have one
            if not animal.image or not animal.image.name:
                try:
                    self.stdout.write(f'Creating image for {animal.name}...')
                    self.create_animal_image(animal, animal_data['color'])
                    self.stdout.write(self.style.SUCCESS(f'✓ Created image for {animal.name}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Failed to create image for {animal.name}: {e}'))
            else:
                self.stdout.write(f'✓ {animal.name} already has an image')
            
            animals.append(animal)
        
        # Assign animals to levels based on difficulty
        self.assign_animals_to_levels(animals)
        
        self.stdout.write(self.style.SUCCESS('Animal images setup completed!'))

    def create_animal_image(self, animal, color):
        """Create a colorful image with animal name"""
        try:
            # Create a 300x300 image with the animal's color
            img = Image.new('RGB', (300, 300), color=color)
            draw = ImageDraw.Draw(img)
            
            # Add a border
            border_color = tuple(max(0, c - 50) for c in color)  # Darker version of the color
            draw.rectangle([0, 0, 299, 299], outline=border_color, width=5)
            
            # Add a circle in the center
            circle_color = tuple(max(0, c - 30) for c in color)  # Slightly darker
            draw.ellipse([75, 75, 225, 225], fill=circle_color)
            
            # Add animal name
            try:
                # Try to use a default font
                font = ImageFont.load_default()
                font_size = 24
            except:
                # Fallback to default
                font = ImageFont.load_default()
                font_size = 20
            
            # Calculate text position to center it
            text = animal.name.upper()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (300 - text_width) // 2
            y = (300 - text_height) // 2
            
            # Draw text with outline for better visibility
            outline_color = (0, 0, 0) if sum(color) > 500 else (255, 255, 255)
            text_color = (255, 255, 255) if sum(color) < 500 else (0, 0, 0)
            
            # Draw outline
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=text_color)
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)
            img_io.seek(0)
            
            # Save to model
            filename = f"{animal.name.lower().replace(' ', '_')}.jpg"
            animal.image.save(filename, ContentFile(img_io.getvalue()), save=True)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create image for {animal.name}: {e}'))

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