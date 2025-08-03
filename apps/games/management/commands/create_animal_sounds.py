from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
import os
from apps.games.models import Animal
import wave
import struct
import math

class Command(BaseCommand):
    help = 'Create placeholder sound files for animals'

    def handle(self, *args, **options):
        self.stdout.write('Creating animal sound files...')
        
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'games', 'sounds')
        os.makedirs(media_dir, exist_ok=True)
        
        # Get all animals
        animals = Animal.objects.filter(is_active=True)
        
        for animal in animals:
            # Create sound if animal doesn't have one
            if not animal.sound or not animal.sound.name:
                try:
                    self.stdout.write(f'Creating sound for {animal.name}...')
                    self.create_animal_sound(animal)
                    self.stdout.write(self.style.SUCCESS(f'✓ Created sound for {animal.name}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Failed to create sound for {animal.name}: {e}'))
            else:
                self.stdout.write(f'✓ {animal.name} already has a sound')
        
        self.stdout.write(self.style.SUCCESS('Animal sounds setup completed!'))

    def create_animal_sound(self, animal):
        """Create a simple beep sound for the animal"""
        try:
            # Create a simple sine wave beep
            sample_rate = 44100  # 44.1 kHz
            duration = 0.5  # 0.5 seconds
            frequency = 440 + (hash(animal.name) % 200)  # Different frequency for each animal
            
            # Generate sine wave
            samples = []
            for i in range(int(sample_rate * duration)):
                sample = math.sin(2 * math.pi * frequency * i / sample_rate)
                samples.append(sample)
            
            # Convert to 16-bit PCM
            pcm_samples = [int(sample * 32767) for sample in samples]
            
            # Create WAV file
            with wave.open('temp_sound.wav', 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Write audio data
                for sample in pcm_samples:
                    wav_file.writeframes(struct.pack('<h', sample))
            
            # Read the file and save to model
            with open('temp_sound.wav', 'rb') as f:
                sound_data = f.read()
            
            # Clean up temp file
            os.remove('temp_sound.wav')
            
            # Save to model
            filename = f"{animal.name.lower().replace(' ', '_')}.wav"
            animal.sound.save(filename, ContentFile(sound_data), save=True)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create sound for {animal.name}: {e}')) 