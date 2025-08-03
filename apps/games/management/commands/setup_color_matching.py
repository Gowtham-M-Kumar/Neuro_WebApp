from django.core.management.base import BaseCommand
from apps.games.models import Game, ColorMatchingGame, Color, ColorMatchingLevel

class Command(BaseCommand):
    help = 'Setup color matching game with colors and levels'

    def handle(self, *args, **options):
        self.stdout.write('Setting up color matching game...')
        
        # Create the main game
        game, created = Game.objects.get_or_create(
            name='Color Matching Game',
            defaults={
                'description': 'Match colors to improve memory and concentration',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created game: {game.name}'))
        else:
            self.stdout.write(f'✓ Game already exists: {game.name}')
        
        # Create colors
        colors_data = [
            # Primary colors
            {'name': 'Red', 'hex_code': '#FF0000', 'category': 'primary'},
            {'name': 'Blue', 'hex_code': '#0000FF', 'category': 'primary'},
            {'name': 'Yellow', 'hex_code': '#FFFF00', 'category': 'primary'},
            
            # Secondary colors
            {'name': 'Green', 'hex_code': '#00FF00', 'category': 'secondary'},
            {'name': 'Orange', 'hex_code': '#FFA500', 'category': 'secondary'},
            {'name': 'Purple', 'hex_code': '#800080', 'category': 'secondary'},
            
            # Warm colors
            {'name': 'Pink', 'hex_code': '#FFC0CB', 'category': 'warm'},
            {'name': 'Brown', 'hex_code': '#A52A2A', 'category': 'warm'},
            {'name': 'Coral', 'hex_code': '#FF7F50', 'category': 'warm'},
            {'name': 'Gold', 'hex_code': '#FFD700', 'category': 'warm'},
            
            # Cool colors
            {'name': 'Cyan', 'hex_code': '#00FFFF', 'category': 'cool'},
            {'name': 'Teal', 'hex_code': '#008080', 'category': 'cool'},
            {'name': 'Navy', 'hex_code': '#000080', 'category': 'cool'},
            {'name': 'Turquoise', 'hex_code': '#40E0D0', 'category': 'cool'},
            
            # Neutral colors
            {'name': 'Black', 'hex_code': '#000000', 'category': 'neutral'},
            {'name': 'White', 'hex_code': '#FFFFFF', 'category': 'neutral'},
            {'name': 'Gray', 'hex_code': '#808080', 'category': 'neutral'},
            {'name': 'Silver', 'hex_code': '#C0C0C0', 'category': 'neutral'},
            {'name': 'Beige', 'hex_code': '#F5F5DC', 'category': 'neutral'},
            {'name': 'Tan', 'hex_code': '#D2B48C', 'category': 'neutral'},
        ]
        
        colors = []
        for color_data in colors_data:
            color, created = Color.objects.get_or_create(
                name=color_data['name'],
                defaults={
                    'hex_code': color_data['hex_code'],
                    'category': color_data['category'],
                    'is_active': True
                }
            )
            colors.append(color)
            if created:
                self.stdout.write(f'✓ Created color: {color.name}')
            else:
                self.stdout.write(f'✓ Color already exists: {color.name}')
        
        # Create game levels
        levels_data = [
            {
                'level': 1,
                'name': 'Level 1 - Easy',
                'description': 'Match 4 pairs of colors in a 4x4 grid',
                'time_limit': 120,
                'required_matches': 4,
                'grid_size': 4,
                'colors_needed': 4
            },
            {
                'level': 2,
                'name': 'Level 2 - Beginner',
                'description': 'Match 6 pairs of colors in a 4x4 grid',
                'time_limit': 100,
                'required_matches': 6,
                'grid_size': 4,
                'colors_needed': 6
            },
            {
                'level': 3,
                'name': 'Level 3 - Intermediate',
                'description': 'Match 8 pairs of colors in a 5x5 grid',
                'time_limit': 90,
                'required_matches': 8,
                'grid_size': 5,
                'colors_needed': 8
            },
            {
                'level': 4,
                'name': 'Level 4 - Advanced',
                'description': 'Match 10 pairs of colors in a 5x5 grid',
                'time_limit': 80,
                'required_matches': 10,
                'grid_size': 5,
                'colors_needed': 10
            },
            {
                'level': 5,
                'name': 'Level 5 - Expert',
                'description': 'Match 12 pairs of colors in a 6x6 grid',
                'time_limit': 70,
                'required_matches': 12,
                'grid_size': 6,
                'colors_needed': 12
            },
        ]
        
        for level_data in levels_data:
            level, created = ColorMatchingGame.objects.get_or_create(
                level=level_data['level'],
                defaults={
                    'name': level_data['name'],
                    'description': level_data['description'],
                    'time_limit': level_data['time_limit'],
                    'required_matches': level_data['required_matches'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'✓ Created level: {level.name}')
            else:
                self.stdout.write(f'✓ Level already exists: {level.name}')
            
            # Create level configuration
            level_config, created = ColorMatchingLevel.objects.get_or_create(
                game=level,
                defaults={
                    'grid_size': level_data['grid_size'],
                    'shuffle_count': 3
                }
            )
            
            # Assign colors to this level
            colors_needed = level_data['colors_needed']
            level_colors = colors[:colors_needed]  # Use first N colors
            level_config.colors.set(level_colors)
            
            if created:
                self.stdout.write(f'✓ Created level configuration for {level.name}')
            else:
                self.stdout.write(f'✓ Level configuration already exists for {level.name}')
        
        self.stdout.write(self.style.SUCCESS('Color matching game setup completed!')) 