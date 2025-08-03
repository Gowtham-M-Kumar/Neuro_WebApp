from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.therapy.models import ActivityAssignment
from apps.users.models import CustomUser

User = get_user_model()

class Command(BaseCommand):
    help = 'Test game URLs and assignments'

    def handle(self, *args, **options):
        self.stdout.write('Testing game URLs and assignments...')
        
        # Get the child user
        try:
            child = User.objects.get(email='child@neurolearn.com')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Child user not found.'))
            return
        
        # Get all assignments
        assignments = ActivityAssignment.objects.filter(child=child)
        
        if not assignments.exists():
            self.stdout.write(self.style.ERROR('No assignments found for child.'))
            return
        
        self.stdout.write(f'\nChild: {child.get_full_name()}')
        self.stdout.write(f'Total assignments: {assignments.count()}')
        
        for assignment in assignments:
            self.stdout.write(f'\n--- {assignment.activity.title} ---')
            self.stdout.write(f'Assignment ID: {assignment.id}')
            self.stdout.write(f'Activity ID: {assignment.activity.id}')
            self.stdout.write(f'Activity Type: {assignment.activity.get_activity_type_display()}')
            self.stdout.write(f'Difficulty: {assignment.activity.get_difficulty_level_display()}')
            self.stdout.write(f'Game URL: http://127.0.0.1:8000/therapy/assignments/{assignment.id}/play/')
            self.stdout.write(f'Detail URL: http://127.0.0.1:8000/therapy/{assignment.activity.id}/')
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ All game URLs are ready for testing!')
        )
        self.stdout.write('\nTo test:')
        self.stdout.write('1. Login as child@neurolearn.com')
        self.stdout.write('2. Go to Learning Games dashboard')
        self.stdout.write('3. Click on any game card to play')
        self.stdout.write('4. Or go to My Activities and click "Start Activity"') 