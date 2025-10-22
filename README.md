# WorkMate - Job Matching Platform

A comprehensive web-based job matching platform that connects students with local job opportunities using advanced algorithms for optimal matching.

## 🚀 Features

### Core Functionality
- **User Registration/Login**: Separate registration for students and service providers
- **Job Posting**: Service providers can post job opportunities
- **Job Browsing**: Students can browse and filter available jobs
- **Smart Recommendations**: AI-powered job suggestions based on location using Dijkstra's Algorithm
- **Rating System**: Students can be rated by service providers
- **Job History**: Complete tracking of student job history and performance

### Advanced Algorithms
- **Linear Search**: Efficient job lookup and search functionality
- **Sorting Algorithms**: Jobs sorted by pay, distance, and other criteria
- **Dijkstra's Algorithm**: Find nearest jobs based on student location
- **Hungarian Algorithm**: Optimal job-student assignment for fair distribution

## 🛠️ Technology Stack

### Backend
- **Python Flask**: RESTful API server
- **CSV Storage**: No database required - uses CSV files for data persistence
- **Flask-CORS**: Cross-origin resource sharing for frontend integration

### Frontend
- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Vite**: Fast build tool and development server

## 📁 Project Structure

```
Workmate/
├── Backend/
│   ├── app.py                 # Flask application with all API endpoints
│   ├── algorithms.py          # Implementation of all algorithms
│   ├── test_algorithms.py    # Algorithm testing suite
│   ├── requirements.txt      # Python dependencies
│   └── data/
│       ├── jobs.csv          # Job postings data
│       ├── students.csv      # Student profiles
│       └── providers.csv     # Service provider profiles
├── Frontend/
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── contexts/         # React context for state management
│   │   ├── pages/            # Main application pages
│   │   ├── services/         # API service layer
│   │   └── main.jsx          # Application entry point
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js       # Vite configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- npm or yarn (package manager)

### Backend Setup

1. **Navigate to Backend directory**:
   ```bash
   cd Backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask server**:
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to Frontend directory**:
   ```bash
   cd Frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

## 🧪 Testing Algorithms

Run the algorithm test suite to verify all algorithms are working correctly:

```bash
cd Backend
python test_algorithms.py
```

Expected output:
```
Testing Job Matching Platform Algorithms
==================================================
Testing Linear Search Algorithm...
Linear Search Algorithm: PASSED

Testing Sorting Algorithm...
Sorting Algorithm: PASSED

Testing Dijkstra's Algorithm...
Dijkstra's Algorithm: PASSED

Testing Hungarian Algorithm...
Hungarian Algorithm: PASSED

All algorithms are working correctly!
==================================================
```

## 📊 Sample Data

The platform comes with pre-populated sample data:

### Students (10 profiles)
- Various locations: New York, Brooklyn, Manhattan, Queens, Bronx
- Different specializations: Computer Science, Engineering, Business, Art, etc.
- Ratings and job completion history

### Service Providers (10 companies)
- Diverse companies: Education Services, Tech Solutions, Creative Agency, etc.
- Multiple job postings across different categories

### Jobs (15+ opportunities)
- Various job types: Tutoring, Web Development, Graphic Design, Event Staff, etc.
- Different pay rates and locations
- Mix of available and assigned jobs

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Jobs
- `GET /api/jobs` - Get all available jobs
- `POST /api/jobs` - Create new job
- `GET /api/jobs/provider/<id>` - Get provider's jobs
- `POST /api/jobs/<id>/apply` - Apply for job
- `GET /api/jobs/suggested/<student_id>` - Get suggested jobs (Dijkstra's)
- `GET /api/jobs/search?q=<query>` - Search jobs (Linear Search)
- `GET /api/jobs/sort?by=<field>&order=<asc/desc>` - Sort jobs

### Students
- `GET /api/students/<id>` - Get student profile
- `POST /api/students/<id>/rate` - Rate student

### Providers
- `GET /api/providers/<id>` - Get provider profile

### Advanced Features
- `POST /api/assignments/optimal` - Optimal job assignment (Hungarian Algorithm)

## 🎨 User Interface

### Student Dashboard
- **Profile Section**: Personal information, rating, job history
- **Suggested Jobs**: AI-powered recommendations based on location
- **Job Browser**: Search, filter, and sort available jobs
- **Application Management**: Track applied jobs

### Provider Dashboard
- **Job Management**: Create, edit, and delete job postings
- **Student Ratings**: Rate students after job completion
- **Analytics**: View job performance and student feedback

### Responsive Design
- Mobile-first approach with Tailwind CSS
- Clean, modern interface
- Intuitive navigation and user experience

## 🔍 Algorithm Details

### Linear Search (O(n))
- Used for job search functionality
- Searches through job titles, descriptions, and locations
- Case-insensitive matching

### Sorting Algorithms (O(n log n))
- Sort jobs by pay, location, or other criteria
- Supports both ascending and descending order
- Used for job filtering and organization

### Dijkstra's Algorithm (O(V + E log V))
- Finds nearest jobs based on student location
- Uses string similarity as distance proxy
- Optimized for location-based recommendations

### Hungarian Algorithm (O(n³))
- Optimal job-student assignment
- Considers location match and student ratings
- Ensures fair distribution of opportunities

## 🚀 Deployment

### Backend Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables if needed
3. Run: `python app.py`
4. Configure reverse proxy (nginx) for production

### Frontend Deployment
1. Build for production: `npm run build`
2. Serve static files from `dist/` directory
3. Configure web server (nginx, Apache) to serve React app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the algorithm test suite
2. Verify all dependencies are installed
3. Ensure both backend and frontend servers are running
4. Check browser console for any errors

## 🎯 Future Enhancements

- Real-time notifications
- Advanced filtering options
- Mobile app development
- Integration with payment systems
- Enhanced analytics dashboard
- Machine learning for better matching
