# NEURO Learning Platform

python manage.py runserver 127.0.0.1:8000

A comprehensive learning and therapy platform designed for children with special needs, providing personalized learning experiences through role-based access for parents, therapists, teachers, and children.

## 🎯 Project Overview

The NEURO Learning Platform is a Django-based web application that serves as a comprehensive learning and therapy tool for children with special needs. The platform provides:

- **Role-based user management** (Parent, Therapist, Teacher, Child)
- **Personalized dashboards** for each user type
- **Visual routine management** for therapy sessions
- **Interactive learning modules** (Alphabet, Numbers, Words)
- **Drawing and creative tools** for children
- **Progress tracking and analytics** for all stakeholders

## 🚀 Phase 1 & 2 Completion Status: ✅ COMPLETE

### Phase 1: User System & Authentication ✅

#### ✅ User System & Authentication
- Custom user model with role-based access
- Email-based authentication system
- User registration with role selection
- Profile management for all user types
- Admin interface for user management

#### ✅ Role-Based Dashboards
- **Parent Dashboard**: Child progress overview, recent activities, notifications
- **Therapist Dashboard**: Patient management interface with routine and activity tools
- **Teacher Dashboard**: Classroom management interface with routine and activity tools
- **Child Dashboard**: Learning games interface (placeholder for Phase 3)

#### ✅ User Profiles
- Comprehensive profile forms for each role
- Profile picture upload functionality
- Role-specific information fields
- Profile editing capabilities

#### ✅ Modern UI/UX
- Bootstrap 5 responsive design
- Font Awesome icons
- Modern gradient styling
- Mobile-friendly interface
- Intuitive navigation

### Phase 2: Core Therapy Tools ✅

#### ✅ Visual Schedule (Routine Module)
- **Routine Management**: Create, edit, and manage visual schedules
- **Task System**: Add tasks with images, descriptions, and time estimates
- **Drag-and-Drop Interface**: Reorder tasks within routines (ready for JavaScript implementation)
- **Assignment System**: Assign routines to specific children
- **Completion Tracking**: Mark tasks as completed with timestamps
- **Progress Analytics**: Track completion rates and patterns
- **Scheduling**: Schedule routines for specific days and times

#### ✅ Personalized Therapy Module
- **Activity Types**: Matching, Focus, Memory, Motor Skills, Sorting, Sequencing
- **Difficulty Levels**: Easy, Medium, Hard progression system
- **Activity Creation**: Therapists/teachers can create custom activities
- **Item Management**: Add images, audio, and interactive elements to activities
- **Assignment System**: Assign activities to specific children
- **Progress Tracking**: Track attempts, scores, and success rates
- **Analytics Dashboard**: Comprehensive progress reports and statistics

#### ✅ Role-Based Access Control
- **Therapists/Teachers**: Create and manage routines and activities
- **Parents**: View and track their children's routines and activities
- **Children**: Access assigned routines and activities
- **Progress Monitoring**: All stakeholders can view relevant progress data

#### ✅ Database Architecture
- **Routine Models**: Routine, Task, TaskCompletion, RoutineSchedule
- **Therapy Models**: TherapyActivity, ActivityItem, ActivityAssignment, ActivityAttempt, ActivityProgress
- **Relationships**: Proper foreign key relationships between all entities
- **Admin Interface**: Full Django admin integration for all models

#### ✅ Error Resolution & Testing
- **QuerySet Type Mismatches**: Fixed all ChildProfile to CustomUser conversion issues
- **Filtering Logic**: Resolved boolean field validation errors in forms
- **Template System**: Complete set of responsive templates for all features
- **System Validation**: All Django system checks pass successfully

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in auth with custom user model
- **File Handling**: Pillow for image processing
- **Forms**: Django Forms with Bootstrap styling

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NEURO
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python create_superuser.py
   ```

6. **Create test users (optional)**
   ```bash
   python create_test_users.py
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## 👥 User Accounts

### Superuser Account
- **Email**: admin@neurolearn.com
- **Password**: NeuroLearn2024!
- **Access**: Full admin privileges

### Test User Accounts
See `authentication.md` for complete list of test accounts for all roles.

## 📁 Project Structure

```
NEURO/
├── neurolearn/                 # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── apps/                      # Django applications
│   ├── users/                 # User management app
│   ├── routines/              # Routine management (Phase 2)
│   ├── therapy/               # Therapy activities (Phase 2)
│   ├── learning/              # Learning modules (Phase 3)
│   └── drawing/               # Drawing tools (Phase 4)
├── templates/                 # HTML templates
│   ├── base.html              # Base template
│   └── users/                 # User-specific templates
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User-uploaded files
├── requirements.txt           # Python dependencies
├── authentication.md          # User credentials
├── script.md                  # Detailed implementation plan
└── README.md                  # This file
```

## 🔐 Authentication & Security

- **Custom User Model**: Email-based authentication
- **Role-Based Access**: Four distinct user roles with specific permissions
- **Profile Management**: Comprehensive user profiles with role-specific fields
- **Admin Interface**: Full Django admin integration
- **Session Management**: Secure session handling with configurable timeouts

## 🎨 User Interface Features

### Design Principles
- **Accessibility**: Designed for users with special needs
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Intuitive**: Clear navigation and user-friendly interface
- **Modern**: Contemporary design with gradient styling

### Key Components
- **Navigation Bar**: Role-based navigation with user dropdown
- **Dashboard Cards**: Visual progress indicators and quick stats
- **Forms**: Bootstrap-styled forms with validation
- **Messages**: Flash messages for user feedback
- **Footer**: Consistent branding and information

## 📊 Database Schema

### User Models
- **CustomUser**: Base user model with role field
- **ParentProfile**: Parent-specific information
- **TherapistProfile**: Therapist credentials and specializations
- **TeacherProfile**: Classroom and grade information
- **ChildProfile**: Child-specific data including age and learning level

### Relationships
- Parents can have multiple children
- Therapists can be assigned to multiple children
- Teachers can manage multiple children
- Children can have primary relationships with parents, therapists, and teachers

## 🚧 Development Phases

### ✅ Phase 1: Project Setup & User System (COMPLETE)
- Django project initialization
- Custom user model and authentication
- Role-based dashboards
- Profile management

### ✅ Phase 2: Core Therapy Tools (COMPLETE)
- Visual schedule (routine) module
- Personalized therapy activities
- Drag-and-drop interface (ready for JavaScript implementation)
- Progress tracking and analytics

### 📋 Phase 3: Learning System
- Alphabet learning (A-Z)
- Number learning (0-20)
- Common word learning
- Progress analytics

### 🎨 Phase 4: Drawing Module
- Canvas-based drawing tools
- Save/load functionality
- Sharing capabilities

## 🧪 Testing

### Manual Testing Checklist
- [x] User registration with all roles
- [x] User login/logout functionality
- [x] Role-based dashboard access
- [x] Profile editing for all roles
- [x] Admin interface access
- [x] Responsive design on different screen sizes

### Test Users Available
- Parent: parent@neurolearn.com / Parent123!
- Therapist: therapist@neurolearn.com / Therapist123!
- Teacher: teacher@neurolearn.com / Teacher123!
- Child: child@neurolearn.com / Child123!

## 🚀 Deployment

### Development
- SQLite database
- Django development server
- Debug mode enabled

### Production (Recommended)
- PostgreSQL database
- Gunicorn or uWSGI
- Nginx reverse proxy
- Static file serving
- Environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in `script.md`
- Review the authentication guide in `authentication.md`
- Create an issue in the repository

## 🎉 Phase 1 & 2 Success!

Phase 1 and Phase 2 have been successfully completed with:

### Phase 1 Achievements:
- ✅ Complete user authentication system
- ✅ Role-based access control
- ✅ Modern, responsive UI
- ✅ Comprehensive admin interface
- ✅ Profile management for all user types

### Phase 2 Achievements:
- ✅ Complete routine management system
- ✅ Visual schedule creation and management
- ✅ Task system with completion tracking
- ✅ Therapy activity creation and assignment
- ✅ Progress tracking and analytics
- ✅ Role-based access for all therapy tools
- ✅ Database architecture for scalable growth

The platform now provides comprehensive therapy tools and is ready for Phase 3 development, which will focus on implementing the learning system (alphabet, numbers, and word learning). 