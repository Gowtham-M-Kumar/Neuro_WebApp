from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.drawing.models import Drawing, DrawingSession
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Test the drawing module functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Drawing Module...'))
        
        # Create test child user if not exists
        try:
            child_user = User.objects.get(email='testchild@neuro.com')
            self.stdout.write(self.style.WARNING(f'Test child user already exists: {child_user.email}'))
        except User.DoesNotExist:
            child_user = User.objects.create_user(
                email='testchild@neuro.com',
                username='testchild_drawing',
                password='testpass123',
                role='child',
                first_name='Test',
                last_name='Child',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created test child user: {child_user.email}'))
        

        
        # Create test drawing
        drawing, created = Drawing.objects.get_or_create(
            title='Test Drawing',
            child=child_user,
            defaults={
                'canvas_data': {
                    'strokes': [
                        {
                            'color': '#ff0000',
                            'size': 5,
                            'points': [100, 100, 200, 200]
                        },
                        {
                            'color': '#00ff00',
                            'size': 3,
                            'points': [150, 150, 250, 250]
                        }
                    ]
                },
                'canvas_width': 800,
                'canvas_height': 600,
                'is_completed': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created test drawing: {drawing.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Test drawing already exists: {drawing.title}'))
        
        # Create test session
        session, created = DrawingSession.objects.get_or_create(
            drawing=drawing,
            child=child_user,
            defaults={
                'strokes_count': 2,
                'colors_used': ['#ff0000', '#00ff00'],
                'tools_used': ['brush'],
                'duration_seconds': 300
            }
        )
        
        if created:
            session.end_session()
            self.stdout.write(self.style.SUCCESS(f'Created test session for drawing'))
        else:
            self.stdout.write(self.style.WARNING(f'Test session already exists'))
        
        # Test drawing methods
        self.stdout.write('\nTesting Drawing Methods:')
        
        # Test canvas data methods
        canvas_data = drawing.get_canvas_data()
        self.stdout.write(f'Canvas data strokes: {len(canvas_data.get("strokes", []))}')
        
        # Test version creation
        new_version = drawing.create_new_version()
        self.stdout.write(f'Created new version: {new_version.version_number}')
        
        # Test permissions
        can_view = drawing.can_be_viewed_by(child_user)
        self.stdout.write(f'Child can view own drawing: {can_view}')
        
        # Display summary
        total_drawings = Drawing.objects.count()
        total_sessions = DrawingSession.objects.count()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('DRAWING MODULE TEST SUMMARY'))
        self.stdout.write('='*50)
        self.stdout.write(f'Total Drawings: {total_drawings}')
        self.stdout.write(f'Total Sessions: {total_sessions}')
        self.stdout.write(f'Test Child User: {child_user.email}')
        self.stdout.write(f'Test Drawing: {drawing.title}')
        self.stdout.write('='*50)
        
        self.stdout.write(self.style.SUCCESS('\nDrawing module test completed successfully!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Login with testchild@neuro.com / testpass123')
        self.stdout.write('2. Visit /drawing/ to access the drawing dashboard')
        self.stdout.write('3. Create and edit drawings using the canvas interface') 