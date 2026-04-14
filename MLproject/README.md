
# Skin Disease Prediction & Telemedicine Platform

A comprehensive Django-based web application that leverages artificial intelligence to predict skin diseases through symptom analysis and image recognition, connecting patients with healthcare professionals.

## 🏥 Overview

This platform provides an intelligent medical consultation system that combines AI-powered disease prediction with real-time doctor-patient communication. Users can either describe their symptoms or upload skin images for preliminary disease assessment, then connect with verified doctors for comprehensive treatment plans.

## ✨ Key Features

### 🤖 AI-Powered Disease Prediction
- **Symptom-Based Analysis**: Advanced ML model analyzes user-reported symptoms to predict potential skin conditions
- **Image Recognition**: CNN-based deep learning model analyzes uploaded skin images
- **Confidence Scoring**: Provides confidence levels for all predictions
- **Doctor Specialization**: Automatically recommends appropriate specialist based on predicted condition

### 👥 Multi-User System
- **Patients**: Register, get predictions, consult doctors, view history
- **Doctors**: Manage profile, handle consultations, provide diagnoses
- **Admins**: Monitor system, manage users, view analytics

### 💬 Telemedicine Features
- **Real-time Chat**: Secure messaging between patients and doctors
- **Consultation Management**: Track active and completed consultations
- **Rating & Reviews**: Doctor rating system based on patient feedback
- **Consultation History**: Complete records of all medical interactions

### 📊 Analytics & Dashboard
- **Disease Analytics**: Track prediction trends and common conditions
- **Performance Metrics**: Doctor performance and patient activity statistics
- **Health Scoring**: Personalized health scores based on user activity

## 🛠️ Technology Stack

### Backend
- **Django 4.2**: Robust web framework
- **Python**: Core programming language
- **PostgreSQL/SQLite**: Database management
- **Joblib**: Machine learning model deployment
- **TensorFlow 2.15**: Deep learning for image analysis

### Frontend
- **Bootstrap 4**: Responsive UI framework
- **jQuery**: Interactive JavaScript
- **HTML5/CSS3**: Modern web standards
- **Real-time WebSockets**: Live chat functionality

### AI/ML Components
- **Scikit-learn**: Symptom prediction model
- **TensorFlow/Keras**: CNN for image classification
- **PIL/OpenCV**: Image processing
- **NumPy/Pandas**: Data manipulation

## 📁 Project Structure

```
Skin/
├── accounts/                 # User authentication & management
│   ├── views.py             # Login/signup logic
│   ├── models.py            # User models
│   └── urls.py              # Account routing
├── main_app/                # Core application logic
│   ├── views.py             # Main application views
│   ├── models.py            # Disease prediction models
│   └── urls.py              # Application routing
├── chats/                   # Real-time communication
│   ├── views.py             # Chat functionality
│   ├── models.py            # Chat & feedback models
│   └── urls.py              # Chat routing
├── templates/               # HTML templates
│   ├── homepage/            # Landing page
│   ├── patient/             # Patient interface
│   ├── doctor/              # Doctor interface
│   ├── admin/               # Admin dashboard
│   └── consultation/        # Chat interface
├── static/                  # Static assets
├── models/                  # Trained ML models
├── disease_prediction/      # Django project settings
└── manage.py               # Django management script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Ankit-Anku07/MLproject.git
cd Skin
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Load Trained Models
Ensure the following files are present in the `models/` directory:
- `trained_model` - Symptom prediction model
- `skin_cnn.h5` - CNN image classification model
- `skin_cnn_labels.json` - Model labels

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 👤 User Roles & Features

### Patient Features
- **Registration & Authentication**: Secure account creation
- **Symptom Checker**: AI-powered symptom analysis
- **Image Scanner**: Upload and analyze skin images
- **Doctor Consultation**: Book appointments with specialists
- **Real-time Chat**: Communicate with doctors
- **Health Dashboard**: Track predictions and consultations
- **History & Reviews**: View past consultations and rate doctors

### Doctor Features
- **Professional Registration**: Verified medical credentials
- **Profile Management**: Specialization and experience details
- **Consultation Dashboard**: Manage patient consultations
- **Real-time Chat**: Respond to patient queries
- **Patient History**: Access consultation records
- **Rating System**: Receive patient feedback and ratings

### Admin Features
- **User Management**: Monitor and manage all users
- **System Analytics**: View platform usage statistics
- **Feedback Monitoring**: Review patient feedback
- **Model Management**: Monitor AI prediction accuracy

## 🤖 AI Models

### Symptom Prediction Model
- **Input**: Array of symptoms (binary)
- **Output**: Predicted disease with confidence score
- **Training**: Machine learning algorithm trained on medical datasets
- **Accuracy**: High precision for common skin conditions

### Image Classification Model
- **Architecture**: Convolutional Neural Network (CNN)
- **Input**: Skin lesion images (224x224 RGB)
- **Output**: Disease classification with confidence
- **Classes**: Various skin conditions and diseases

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Model Configuration
Update model paths in `main_app/views.py`:
```python
CNN_MODEL_PATH = 'models/skin_cnn.h5'
CNN_LABELS_PATH = 'models/skin_cnn_labels.json'
SYMPTOM_MODEL_PATH = 'models/trained_model'
```

## 📱 Usage Examples

### Patient Workflow
1. **Register/Login**: Create account or sign in
2. **Choose Prediction Method**: Symptoms or image upload
3. **Get AI Prediction**: Receive preliminary diagnosis
4. **Select Doctor**: Choose from recommended specialists
5. **Start Consultation**: Begin real-time chat
6. **Receive Treatment**: Get professional medical advice

### Doctor Workflow
1. **Professional Signup**: Register with medical credentials
2. **Profile Setup**: Configure specialization and availability
3. **Receive Consultations**: Handle patient requests
4. **Provide Diagnosis**: Share professional medical opinion
5. **Follow-up**: Continue patient care through platform

## 🏥 Medical Disclaimer

⚠️ **Important**: This application is for educational and preliminary assessment purposes only. It should not replace professional medical diagnosis, treatment, or advice. Always consult with qualified healthcare professionals for medical concerns.

## 🔒 Security Features

- **User Authentication**: Secure login system
- **Session Management**: Protected user sessions
- **Data Validation**: Input sanitization and validation
- **CSRF Protection**: Cross-site request forgery prevention
- **Image Validation**: Medical image authenticity checks

## 📊 API Endpoints

### Authentication
- `POST /signup_patient/` - Patient registration
- `POST /signup_doctor/` - Doctor registration
- `POST /sign_in_patient/` - Patient login
- `POST /sign_in_doctor/` - Doctor login

### Disease Prediction
- `POST /checkdisease/` - Symptom-based prediction
- `POST /scan_image/` - Image-based prediction

### Consultation
- `GET /consult_a_doctor/` - View available doctors
- `POST /make_consultation/<doctor_username>/` - Start consultation
- `POST /chat/` - Send chat message

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Setup
1. **Environment Configuration**:
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   ```

2. **Database Migration**:
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   ```

3. **Web Server** (Using Gunicorn):
   ```bash
   gunicorn disease_prediction.wsgi:application --bind 0.0.0.0:8000
   ```

### Docker Deployment
```dockerfile
FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Email**: skinprediction@gmail.com
- **Phone**: 0123456789
- **Address**: Ranchi, India

## 🙏 Acknowledgments

- Medical dataset contributors
- Open source community
- Healthcare professionals for domain expertise
- AI/ML research community

---

**Made with ❤️ for better healthcare accessibility**

*Note: This application is intended for educational purposes. Always consult healthcare professionals for medical advice.*

