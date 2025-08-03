# Drawing Module - NEURO Learning Platform

## Overview

The Drawing Module is a comprehensive digital art creation system designed specifically for children with special needs. It provides an intuitive, touch-friendly drawing interface with advanced features for therapy and learning purposes.

## Features

### 🎨 Core Drawing Features
- **HTML5 Canvas Drawing**: High-performance drawing with touch and mouse support
- **Multiple Drawing Tools**: Brush, eraser, color picker, and size adjustment
- **Rich Color Palette**: 10 predefined colors with easy selection
- **Brush Sizes**: 4 different brush sizes (2px, 5px, 10px, 20px)
- **Undo/Redo**: Full stroke-based undo and redo functionality
- **Clear Canvas**: One-click canvas clearing

### 💾 Save & Load System
- **Auto-save**: Automatic saving every 30 seconds
- **Manual Save**: Save button for immediate saving
- **Version Control**: Create new versions of existing drawings
- **Drawing History**: Track all drawing versions and changes

### 🔒 Sharing & Permissions
- **Role-based Access**: Different permissions for parents, therapists, and teachers
- **Selective Sharing**: Choose who can view each drawing
- **Privacy Controls**: Granular sharing settings per drawing

### 📊 Analytics & Tracking
- **Session Tracking**: Monitor drawing session duration and activity
- **Usage Analytics**: Track colors used, tools used, and stroke counts
- **Progress Monitoring**: View drawing completion status
- **Performance Metrics**: Analyze drawing patterns and engagement

### 🎯 Child-Friendly Interface
- **Responsive Design**: Works on tablets, desktops, and mobile devices
- **Touch Optimized**: Designed for touch interaction
- **Visual Feedback**: Clear visual indicators for all actions
- **Accessible UI**: Large buttons and clear navigation

## Technical Architecture

### Models

#### Drawing Model
```python
class Drawing(models.Model):
    title = models.CharField(max_length=200)
    child = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    canvas_data = models.JSONField()  # Serialized canvas data
    canvas_width = models.PositiveIntegerField(default=800)
    canvas_height = models.PositiveIntegerField(default=600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    
    # Sharing permissions
    shared_with_parents = models.BooleanField(default=True)
    shared_with_therapists = models.BooleanField(default=True)
    shared_with_teachers = models.BooleanField(default=True)
    
    # Version control
    parent_drawing = models.ForeignKey('self', null=True, blank=True)
    version_number = models.PositiveIntegerField(default=1)
```

#### DrawingSession Model
```python
class DrawingSession(models.Model):
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE)
    child = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Analytics
    strokes_count = models.PositiveIntegerField(default=0)
    colors_used = models.JSONField(default=list)
    tools_used = models.JSONField(default=list)
```

### Views

#### Main Views
- `drawing_dashboard()`: Child's main drawing dashboard
- `drawing_canvas()`: Main drawing interface
- `drawing_list()`: List all accessible drawings
- `drawing_detail()`: View specific drawing details
- `drawing_analytics()`: Analytics for therapists/parents/teachers

#### AJAX Endpoints
- `save_drawing_data()`: Save canvas data
- `load_drawing_data()`: Load canvas data
- `create_new_version()`: Create new drawing version
- `end_drawing_session()`: End drawing session

### Templates

#### Core Templates
- `canvas.html`: Main drawing interface with HTML5 canvas
- `dashboard.html`: Child's drawing dashboard
- `drawing_list.html`: List of all drawings
- `drawing_detail.html`: Detailed drawing view
- `drawing_form.html`: Create/edit drawing metadata
- `analytics.html`: Analytics dashboard

## Usage Guide

### For Children

1. **Accessing the Drawing Module**
   - Login with child account
   - Navigate to `/drawing/`
   - View your drawing dashboard

2. **Creating a New Drawing**
   - Click "Start New Drawing" button
   - Enter a title and set sharing preferences
   - Begin drawing on the canvas

3. **Using the Drawing Tools**
   - **Brush Tool**: Click the paintbrush icon to draw
   - **Eraser Tool**: Click the eraser icon to erase
   - **Color Selection**: Click colors from the color palette
   - **Size Adjustment**: Select brush size from the size options
   - **Undo/Redo**: Use the undo/redo buttons to go back/forward

4. **Saving Your Work**
   - Click "Save" button to save immediately
   - Drawing auto-saves every 30 seconds
   - Use "New Version" to create a copy of your drawing

### For Parents/Therapists/Teachers

1. **Viewing Children's Drawings**
   - Login with your account
   - Navigate to `/drawing/list/`
   - View all drawings shared with you

2. **Analytics Dashboard**
   - Navigate to `/drawing/analytics/`
   - View drawing statistics and progress
   - Monitor engagement and activity patterns

3. **Drawing Details**
   - Click on any drawing to view details
   - See version history and metadata
   - Export drawings as images

## API Endpoints

### Drawing Management
```
GET  /drawing/                    # Drawing dashboard
GET  /drawing/list/               # List all drawings
GET  /drawing/analytics/          # Analytics dashboard
GET  /drawing/canvas/             # New drawing canvas
GET  /drawing/canvas/<id>/        # Edit existing drawing
GET  /drawing/detail/<id>/        # View drawing details
POST /drawing/create/             # Create new drawing
POST /drawing/edit/<id>/          # Edit drawing metadata
POST /drawing/delete/<id>/        # Delete drawing
```

### AJAX Endpoints
```
POST /drawing/save/<id>/          # Save canvas data
GET  /drawing/load/<id>/          # Load canvas data
POST /drawing/version/<id>/       # Create new version
POST /drawing/session/end/<id>/   # End drawing session
```

## Installation & Setup

1. **Database Migration**
   ```bash
   python manage.py makemigrations drawing
   python manage.py migrate
   ```

2. **Test the Module**
   ```bash
   python manage.py test_drawing
   ```

3. **Create Test User**
   - Email: `testchild@neuro.com`
   - Password: `testpass123`
   - Role: Child

## Configuration

### Settings
The drawing module uses the following Django settings:
- `MEDIA_URL` and `MEDIA_ROOT`: For file uploads
- `STATIC_URL` and `STATIC_ROOT`: For static assets
- `AUTH_USER_MODEL`: Custom user model

### Canvas Configuration
- Default canvas size: 800x600 pixels
- Supported formats: PNG export
- Touch support: Enabled for mobile devices
- Auto-save interval: 30 seconds

## Security Features

- **CSRF Protection**: All forms and AJAX requests protected
- **Role-based Access**: Users can only access appropriate drawings
- **Input Validation**: All user inputs validated and sanitized
- **Session Security**: Secure session management
- **File Upload Security**: Safe file handling

## Performance Optimizations

- **Canvas Optimization**: Efficient drawing algorithms
- **Database Indexing**: Optimized queries for large datasets
- **Caching**: Session data caching for better performance
- **Lazy Loading**: Images and data loaded on demand

## Browser Support

- **Desktop**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile, Samsung Internet
- **Tablet**: iPad Safari, Android Chrome
- **Touch Support**: Full touch gesture support

## Troubleshooting

### Common Issues

1. **Canvas Not Loading**
   - Check browser console for JavaScript errors
   - Ensure HTML5 canvas is supported
   - Verify static files are served correctly

2. **Drawing Not Saving**
   - Check network connectivity
   - Verify CSRF token is present
   - Check server logs for errors

3. **Touch Not Working**
   - Ensure device supports touch events
   - Check if touch events are enabled
   - Verify browser supports touch API

### Debug Mode
Enable Django debug mode to see detailed error messages:
```python
DEBUG = True
```

## Future Enhancements

- **Advanced Tools**: Shapes, text, layers
- **Collaborative Drawing**: Real-time multi-user drawing
- **AI Integration**: Drawing suggestions and analysis
- **Export Options**: PDF, SVG, and other formats
- **Templates**: Pre-made drawing templates
- **Voice Commands**: Voice-controlled drawing tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This module is part of the NEURO Learning Platform and follows the same license terms.

---

**Note**: This drawing module is specifically designed for children with special needs and includes features that support therapy and learning objectives. The interface is optimized for touch interaction and provides a safe, engaging environment for creative expression. 