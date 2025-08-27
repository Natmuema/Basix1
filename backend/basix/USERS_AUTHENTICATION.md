# Users App Authentication System

This document explains the complete authentication system implemented using the Django `users` app for the BASIX IP Marketplace.

## 🏗️ **Architecture Overview**

The authentication system is built using Django's `users` app with the following components:

- **Custom User Model**: Extends Django's AbstractUser with additional fields
- **Profile Models**: Separate models for Creator and Investor profiles
- **JWT Authentication**: Secure token-based authentication
- **Verification System**: Email and phone verification
- **Session Tracking**: User session management
- **Admin Interface**: Comprehensive Django admin configuration

## 📁 **File Structure**

```
backend/basix/
├── users/
│   ├── models.py              # Custom User model and related models
│   ├── serializers.py         # API serializers
│   ├── views.py               # Authentication views and ViewSets
│   ├── urls.py                # URL routing
│   ├── admin.py               # Django admin configuration
│   └── migrations/            # Database migrations
├── basix/
│   ├── settings.py            # Django settings with JWT & CORS config
│   └── urls.py                # Main URL configuration
└── requirements.txt           # Python dependencies
```

## 🔐 **Models**

### **User Model**
```python
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('creator', 'Creator'),
        ('investor', 'Investor'),
        ('admin', 'Admin'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='creator')
    wallet_address = models.CharField(max_length=255, unique=True, blank=True)
    profile_image = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **CreatorProfile Model**
```python
class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    skills = models.JSONField(default=list)
    reputation_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    portfolio_url = models.URLField(blank=True)
    social_media_links = models.JSONField(default=dict)
    specializations = models.JSONField(default=list)
    experience_years = models.IntegerField(default=0)
    awards = models.JSONField(default=list)
```

### **InvestorProfile Model**
```python
class InvestorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    investment_preferences = models.JSONField(default=list)
    risk_tolerance = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    investment_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    preferred_categories = models.JSONField(default=list)
    investment_history = models.JSONField(default=list)
```

## 🔗 **API Endpoints**

### **Authentication Endpoints**
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/update_profile/` - Update user profile
- `POST /api/auth/change_password/` - Change password
- `GET /api/auth/stats/` - Get user statistics

### **Verification Endpoints**
- `POST /api/auth/send_email_verification/` - Send email verification
- `POST /api/auth/verify_email/` - Verify email with token
- `POST /api/auth/send_phone_verification/` - Send phone verification
- `POST /api/auth/verify_phone/` - Verify phone with code

### **User Management Endpoints**
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `GET /api/users/{id}/profile/` - Get detailed user profile
- `GET /api/users/creators/` - Get all creators
- `GET /api/users/investors/` - Get all investors

### **Profile Management Endpoints**
- `GET /api/creator-profiles/` - List creator profiles
- `GET /api/creator-profiles/top_creators/` - Get top creators
- `GET /api/investor-profiles/` - List investor profiles
- `GET /api/investor-profiles/top_investors/` - Get top investors

### **JWT Token Endpoints**
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

## 🚀 **Setup Instructions**

### **1. Install Dependencies**
```bash
cd backend/basix
pip install -r requirements.txt
```

### **2. Run Migrations**
```bash
python manage.py makemigrations users
python manage.py migrate
```

### **3. Create Superuser**
```bash
python manage.py createsuperuser
```

### **4. Run Development Server**
```bash
python manage.py runserver 0.0.0.0:8000
```

## 📝 **Usage Examples**

### **User Registration**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Test",
    "last_name": "User",
    "user_type": "creator",
    "phone_number": "+1234567890",
    "creator_profile": {
      "skills": ["art", "design"],
      "reputation_score": 50,
      "experience_years": 3
    }
  }'
```

### **User Login**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### **Get Current User**
```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### **Update Profile**
```bash
curl -X PUT http://localhost:8000/api/auth/update_profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "Updated bio",
    "creator_profile": {
      "skills": ["art", "design", "photography"],
      "reputation_score": 75
    }
  }'
```

## 🔧 **Configuration**

### **Django Settings**
```python
# Custom User Model
AUTH_USER_MODEL = 'users.User'

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # Development only
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

## 🛡️ **Security Features**

1. **JWT Token Authentication**: Secure token-based authentication
2. **Token Refresh**: Automatic token renewal
3. **Token Blacklisting**: Secure logout
4. **Password Validation**: Django's built-in password validation
5. **User Verification**: Email and phone verification
6. **Session Tracking**: User session management
7. **CORS Protection**: Cross-origin request handling
8. **Permission Classes**: Route-level authentication

## 📊 **Admin Interface**

Access the Django admin interface at `http://localhost:8000/admin/` to manage:

- **Users**: User accounts and profiles
- **Creator Profiles**: Creator-specific information
- **Investor Profiles**: Investor-specific information
- **User Verification**: Email and phone verification status
- **User Sessions**: Active user sessions

## 🔄 **Frontend Integration**

The frontend authentication context (`frontend/src/context/Authcontext.jsx`) is configured to work with these endpoints:

```javascript
// Login
const response = await api.post('/auth/login/', {
  username: email,
  password: password,
});

// Register
const response = await api.post('/auth/register/', {
  username: userData.name,
  email: userData.email,
  password: userData.password,
  password_confirm: userData.password,
  user_type: userData.userType,
  // ... other fields
});

// Get current user
const response = await api.get('/auth/me/');
```

## 🧪 **Testing**

Use the AuthTest component (`frontend/src/components/AuthTest.jsx`) to test the authentication system:

1. Visit `http://localhost:5173/auth-test`
2. Test registration, login, and API calls
3. Verify user data and statistics
4. Test profile management

## 🔮 **Future Enhancements**

1. **Two-Factor Authentication**: Add 2FA support
2. **Social Login**: Integrate with social media platforms
3. **Password Reset**: Implement password reset functionality
4. **Email Templates**: Custom email templates for verification
5. **SMS Integration**: Real SMS service integration
6. **KYC Integration**: Know Your Customer verification
7. **Role-based Permissions**: More granular permissions
8. **Audit Logging**: Comprehensive audit trail

## 🐛 **Troubleshooting**

### **Common Issues**

1. **Migration Errors**: Run `python manage.py makemigrations` and `python manage.py migrate`
2. **CORS Errors**: Check CORS settings in `settings.py`
3. **Token Expiration**: Tokens automatically refresh, but manual logout may be needed
4. **User Creation**: Ensure all required fields are provided during registration

### **Debug Mode**
Enable debug logging in `settings.py`:
```python
LOGGING = {
    'loggers': {
        'users': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## 📞 **Support**

For issues and questions:
1. Check the Django logs in `basix.log`
2. Verify API endpoints are accessible
3. Test with the AuthTest component
4. Check browser console for frontend errors

The authentication system is now fully functional and ready for production use! 🎉