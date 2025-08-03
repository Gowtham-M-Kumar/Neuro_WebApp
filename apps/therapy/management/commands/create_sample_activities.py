from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.therapy.models import TherapyActivity, ActivityItem
from apps.users.models import CustomUser

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample therapy activities with interactive games'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample therapy activities...')
        
        # Get or create a therapist user
        therapist, created = User.objects.get_or_create(
            email='therapist@neurolearn.com',
            defaults={
                'username': 'therapist@neurolearn.com',
                'first_name': 'Dr.',
                'last_name': 'Therapist',
                'role': 'therapist',
                'is_active': True
            }
        )
        
        if created:
            # Create therapist profile
            from apps.users.models import TherapistProfile
            TherapistProfile.objects.create(
                user=therapist,
                license_number='TH123456',
                specialization='Child Development',
                years_of_experience=5
            )
            self.stdout.write(f'Created therapist: {therapist.get_full_name()}')
        
        # Create sample activities
        activities_data = [
            {
                'title': 'Color Matching Game',
                'description': 'Match the colors to improve visual recognition and memory skills.',
                'activity_type': 'matching',
                'difficulty_level': 'easy',
                'instructions': 'Click on two cards to find matching colors. Match all pairs to complete the game!',
                'items': [
                    {'title': 'Red', 'order': 1, 'is_correct_answer': True, 'group_id': 'colors'},
                    {'title': 'Blue', 'order': 2, 'is_correct_answer': True, 'group_id': 'colors'},
                    {'title': 'Yellow', 'order': 3, 'is_correct_answer': True, 'group_id': 'colors'},
                    {'title': 'Green', 'order': 4, 'is_correct_answer': True, 'group_id': 'colors'},
                    {'title': 'Orange', 'order': 5, 'is_correct_answer': True, 'group_id': 'colors'},
                    {'title': 'Purple', 'order': 6, 'is_correct_answer': True, 'group_id': 'colors'},
                ]
            },
            {
                'title': 'Focus Training',
                'description': 'Improve attention span and focus by clicking on targets as they appear.',
                'activity_type': 'focus',
                'difficulty_level': 'medium',
                'instructions': 'Click on the target (🎯) as quickly as possible when it appears on screen!',
                'items': [
                    {'title': 'Target', 'order': 1, 'is_correct_answer': True, 'group_id': 'focus'},
                ]
            },
            {
                'title': 'Memory Card Game',
                'description': 'Test and improve memory by finding matching pairs of cards.',
                'activity_type': 'memory',
                'difficulty_level': 'medium',
                'instructions': 'Find matching pairs of cards. Remember their positions to complete the game!',
                'items': [
                    {'title': 'Dog', 'order': 1, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Cat', 'order': 2, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Mouse', 'order': 3, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Hamster', 'order': 4, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Rabbit', 'order': 5, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Fox', 'order': 6, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Bear', 'order': 7, 'is_correct_answer': True, 'group_id': 'memory'},
                    {'title': 'Panda', 'order': 8, 'is_correct_answer': True, 'group_id': 'memory'},
                ]
            },
            {
                'title': 'Drawing Practice',
                'description': 'Improve fine motor skills by drawing shapes and patterns.',
                'activity_type': 'motor',
                'difficulty_level': 'easy',
                'instructions': 'Use your mouse to draw the shape shown below. Practice your fine motor skills!',
                'items': [
                    {'title': 'Circle', 'order': 1, 'is_correct_answer': True, 'group_id': 'shapes'},
                    {'title': 'Square', 'order': 2, 'is_correct_answer': True, 'group_id': 'shapes'},
                    {'title': 'Triangle', 'order': 3, 'is_correct_answer': True, 'group_id': 'shapes'},
                    {'title': 'Star', 'order': 4, 'is_correct_answer': True, 'group_id': 'shapes'},
                ]
            },
            {
                'title': 'Category Sorting',
                'description': 'Sort items into correct categories to improve classification skills.',
                'activity_type': 'sorting',
                'difficulty_level': 'medium',
                'instructions': 'Drag and drop items into the correct categories: Fruits, Vegetables, Animals, and Vehicles.',
                'items': [
                    {'title': 'Apple', 'order': 1, 'is_correct_answer': True, 'group_id': 'fruits'},
                    {'title': 'Banana', 'order': 2, 'is_correct_answer': True, 'group_id': 'fruits'},
                    {'title': 'Carrot', 'order': 3, 'is_correct_answer': True, 'group_id': 'vegetables'},
                    {'title': 'Broccoli', 'order': 4, 'is_correct_answer': True, 'group_id': 'vegetables'},
                    {'title': 'Dog', 'order': 5, 'is_correct_answer': True, 'group_id': 'animals'},
                    {'title': 'Cat', 'order': 6, 'is_correct_answer': True, 'group_id': 'animals'},
                    {'title': 'Car', 'order': 7, 'is_correct_answer': True, 'group_id': 'vehicles'},
                    {'title': 'Airplane', 'order': 8, 'is_correct_answer': True, 'group_id': 'vehicles'},
                ]
            },
            {
                'title': 'Number Sequence',
                'description': 'Arrange numbers in the correct order to improve sequencing skills.',
                'activity_type': 'sequencing',
                'difficulty_level': 'hard',
                'instructions': 'Click on the numbers to arrange them in the correct order from 1 to 5.',
                'items': [
                    {'title': '1', 'order': 1, 'is_correct_answer': True, 'group_id': 'numbers'},
                    {'title': '2', 'order': 2, 'is_correct_answer': True, 'group_id': 'numbers'},
                    {'title': '3', 'order': 3, 'is_correct_answer': True, 'group_id': 'numbers'},
                    {'title': '4', 'order': 4, 'is_correct_answer': True, 'group_id': 'numbers'},
                    {'title': '5', 'order': 5, 'is_correct_answer': True, 'group_id': 'numbers'},
                ]
            },
        ]
        
        for activity_data in activities_data:
            activity, created = TherapyActivity.objects.get_or_create(
                title=activity_data['title'],
                defaults={
                    'description': activity_data['description'],
                    'activity_type': activity_data['activity_type'],
                    'difficulty_level': activity_data['difficulty_level'],
                    'instructions': activity_data['instructions'],
                    'created_by': therapist,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created activity: {activity.title}')
                
                # Create activity items
                for item_data in activity_data['items']:
                    ActivityItem.objects.create(
                        activity=activity,
                        title=item_data['title'],
                        order=item_data['order'],
                        is_correct_answer=item_data['is_correct_answer'],
                        group_id=item_data['group_id']
                    )
                
                self.stdout.write(f'  - Added {len(activity_data["items"])} items')
            else:
                self.stdout.write(f'Activity already exists: {activity.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample therapy activities!')
        )
        
        # Create a parent and child for testing
        parent, created = User.objects.get_or_create(
            email='parent@neurolearn.com',
            defaults={
                'username': 'parent@neurolearn.com',
                'first_name': 'John',
                'last_name': 'Parent',
                'role': 'parent',
                'is_active': True
            }
        )
        
        if created:
            from apps.users.models import ParentProfile
            ParentProfile.objects.create(
                user=parent,
                phone='555-0123',
                address='123 Parent St, City, State'
            )
            self.stdout.write(f'Created parent: {parent.get_full_name()}')
        
        child, created = User.objects.get_or_create(
            email='child@neurolearn.com',
            defaults={
                'username': 'child@neurolearn.com',
                'first_name': 'Alex',
                'last_name': 'Child',
                'role': 'child',
                'is_active': True
            }
        )
        
        if created:
            from apps.users.models import ChildProfile
            ChildProfile.objects.create(
                user=child,
                age=8,
                grade='3rd Grade',
                special_needs='ADHD',
                parent=parent.parent_profile
            )
            self.stdout.write(f'Created child: {child.get_full_name()}')
        
        self.stdout.write(
            self.style.SUCCESS('\nTest accounts created:')
        )
        self.stdout.write('Therapist: therapist@neurolearn.com')
        self.stdout.write('Parent: parent@neurolearn.com')
        self.stdout.write('Child: child@neurolearn.com')
        self.stdout.write('\nYou can use any password to login with these accounts.') 