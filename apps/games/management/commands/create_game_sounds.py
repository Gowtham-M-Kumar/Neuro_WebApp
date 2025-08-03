from django.core.management.base import BaseCommand
from django.conf import settings
import os
import wave
import struct
import math

class Command(BaseCommand):
    help = 'Create game sound effects'

    def handle(self, *args, **options):
        self.stdout.write('Creating game sound effects...')
        
        # Create static directory for game sounds
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'games', 'sounds')
        os.makedirs(static_dir, exist_ok=True)
        
        # Create different sound effects
        sounds = [
            ('match', 800, 0.3),      # Higher pitch for match
            ('flip', 600, 0.2),       # Medium pitch for flip
            ('success', 1000, 0.5),   # High pitch for success
            ('gameover', 300, 0.4),   # Low pitch for game over
        ]
        
        for sound_name, frequency, duration in sounds:
            try:
                self.stdout.write(f'Creating {sound_name} sound...')
                self.create_sound_effect(sound_name, frequency, duration, static_dir)
                self.stdout.write(self.style.SUCCESS(f'✓ Created {sound_name} sound'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Failed to create {sound_name} sound: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Game sound effects setup completed!'))

    def create_sound_effect(self, name, frequency, duration, output_dir):
        """Create a sound effect with given frequency and duration"""
        try:
            # Create a simple sine wave
            sample_rate = 44100  # 44.1 kHz
            
            # Generate sine wave
            samples = []
            for i in range(int(sample_rate * duration)):
                sample = math.sin(2 * math.pi * frequency * i / sample_rate)
                # Add fade in/out
                fade_factor = 1.0
                if i < sample_rate * 0.1:  # Fade in
                    fade_factor = i / (sample_rate * 0.1)
                elif i > sample_rate * (duration - 0.1):  # Fade out
                    fade_factor = (sample_rate * duration - i) / (sample_rate * 0.1)
                sample *= fade_factor
                samples.append(sample)
            
            # Convert to 16-bit PCM
            pcm_samples = [int(sample * 16383) for sample in samples]  # Reduced volume
            
            # Create WAV file
            output_path = os.path.join(output_dir, f'{name}.wav')
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Write audio data
                for sample in pcm_samples:
                    wav_file.writeframes(struct.pack('<h', sample))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create {name} sound: {e}')) 