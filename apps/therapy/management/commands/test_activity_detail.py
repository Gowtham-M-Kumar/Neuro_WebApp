from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth import get_user_model
from apps.therapy.models import TherapyActivity, ActivityAssignment

User = get_user_model()

class Command(BaseCommand):
    help = 'Test activity detail view and assignment passing'

    def handle(self, *args, **options):
        self.stdout.write('Testing activity detail view...')
        
        # Get the child user
        try:
            child = User.objects.get(email='child@neurolearn.com')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Child user not found.'))
            return
        
        # Get an activity
        activity = TherapyActivity.objects.first()
        if not activity:
            self.stdout.write(self.style.ERROR('No activities found.'))
            return
        
        # Get assignment for this activity
        assignment = ActivityAssignment.objects.filter(
            activity=activity,
            child=child
        ).first()
        
        if not assignment:
            self.stdout.write(self.style.ERROR(f'No assignment found for activity: {activity.title}'))
            return
        
        self.stdout.write(f'Activity: {activity.title}')
        self.stdout.write(f'Activity ID: {activity.id}')
        self.stdout.write(f'Assignment ID: {assignment.id}')
        self.stdout.write(f'Child: {child.get_full_name()}')
        
        # Test the view
        client = Client()
        client.force_login(child)
        
        # Test activity detail view
        detail_url = f'/therapy/{activity.id}/'
        self.stdout.write(f'\nTesting detail URL: {detail_url}')
        
        response = client.get(detail_url)
        self.stdout.write(f'Status Code: {response.status_code}')
        
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS('✅ Activity detail view works!'))
            
            # Check if assignment is in context
            if hasattr(response, 'context') and response.context:
                assignment_in_context = response.context.get('assignment')
                if assignment_in_context:
                    self.stdout.write(f'✅ Assignment found in context: {assignment_in_context.id}')
                else:
                    self.stdout.write(self.style.WARNING('⚠️ Assignment not found in context'))
            else:
                self.stdout.write(self.style.WARNING('⚠️ No context available'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Activity detail view failed: {response.status_code}'))
        
        # Test game play URL
        play_url = f'/therapy/assignments/{assignment.id}/play/'
        self.stdout.write(f'\nTesting play URL: {play_url}')
        
        response = client.get(play_url)
        self.stdout.write(f'Status Code: {response.status_code}')
        
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS('✅ Game play view works!'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Game play view failed: {response.status_code}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('Test Summary:')
        self.stdout.write(f'Activity Detail URL: http://127.0.0.1:8000{detail_url}')
        self.stdout.write(f'Game Play URL: http://127.0.0.1:8000{play_url}')
        self.stdout.write('\nTo test manually:')
        self.stdout.write('1. Login as child@neurolearn.com')
        self.stdout.write('2. Go to the activity detail page')
        self.stdout.write('3. Click "Start Activity" button')
        self.stdout.write('4. You should be taken to the game play page') 