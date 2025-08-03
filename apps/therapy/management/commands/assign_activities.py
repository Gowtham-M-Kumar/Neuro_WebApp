from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.therapy.models import TherapyActivity, ActivityAssignment
from apps.users.models import CustomUser

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign activities to children for testing'

    def handle(self, *args, **options):
        self.stdout.write('Assigning activities to children...')
        
        # Get the child user
        try:
            child = User.objects.get(email='child@neurolearn.com')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Child user not found. Please run create_sample_activities first.'))
            return
        
        # Get all activities
        activities = TherapyActivity.objects.filter(is_active=True)
        
        if not activities.exists():
            self.stdout.write(self.style.ERROR('No activities found. Please run create_sample_activities first.'))
            return
        
        # Assign activities to child
        assigned_count = 0
        for activity in activities:
            assignment, created = ActivityAssignment.objects.get_or_create(
                activity=activity,
                child=child,
                defaults={
                    'assigned_by': activity.created_by
                }
            )
            
            if created:
                self.stdout.write(f'Assigned: {activity.title}')
                assigned_count += 1
            else:
                self.stdout.write(f'Already assigned: {activity.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned {assigned_count} activities to {child.get_full_name()}')
        )
        
        self.stdout.write('\nYou can now login as the child and play the games!')
        self.stdout.write('Child email: child@neurolearn.com')
        self.stdout.write('Use any password to login.') 