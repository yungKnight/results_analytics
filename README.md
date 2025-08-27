# EduNalytica 📊🎓

A comprehensive academic performance analysis Django web application that provides intelligent insights into student academic performance using advanced statistical methods and predictive analytics.

**🌐 Live Demo:** [edunalytica.onrender.com](https://edunalytica.onrender.com)

## Overview

EduNalytica is a monolithic Django web application that wraps around custom academic analytics logic to deliver deep insights into student performance patterns. The system analyzes grade data across semesters and course branches to provide actionable recommendations for academic improvement.

## Key Features

### 🎯 Core Analytics Engine
- **Grade Data Processing**: Automatically collects and processes student grade data
- **Semester Organization**: Intelligently groups courses by semester with robust carryover handling
- **Course Branch Analysis**: Categorizes courses by academic branches (vital for performance logic)
- **GPA/CGPA Calculations**: Computes standard and weighted GPAs for comprehensive performance metrics

### 📈 Advanced Statistical Analysis
- **Exponential Moving Averages (EMAs)**: Identifies performance divergence and convergence points
- **Correlation Analysis**: Examines relationships between performance and key factors:
  - Total units per semester
  - Number of courses
  - GPA/CGPA trends
- **Partial Correlation**: Measures weighted impact of each course branch on overall performance
- **Unit Tracking**: Monitors total units offered per semester and course branch

### 🔍 Intelligent Insights Generation

The system generates three comprehensive analysis sections:

#### 1. Semester Performance Analysis
- Detailed breakdown of performance metrics per semester
- Identification of performance patterns and trends
- Semester-by-semester comparison and growth tracking

#### 2. In-Depth Performance Analysis
- Uses divergence/convergence analysis with configurable thresholds
- Determines overall academic performance quality
- Highlights critical performance inflection points

#### 3. Strategic Recommendations
- Combines correlation and partial correlation results
- Provides data-driven course selection guidance:
  - **Course Branch Optimization**: Which subjects to focus more/less on
  - **Unit Load Management**: Optimal number of units to take
  - **Course Load Balancing**: Ideal number of courses per semester

## Technical Architecture

### Backend
- **Framework**: Django (Python)
- **Database**: PostgreSQL hosted on Supabase
- **Deployment**: Render.com hosting platform
- **Data Storage**: Demo environment includes pre-loaded student result data
- **Processing Engine**: Custom EduNalytica logic handles all statistical computations
- **Views**: Django class-based and function-based views for data presentation

### Analytics Pipeline
1. **Data Ingestion**: Grade data collection and validation
2. **Preprocessing**: Semester grouping and carryover resolution
3. **Statistical Computing**: EMA, correlation, and partial correlation calculations
4. **Insight Generation**: Threshold-based performance evaluation
5. **Recommendation Engine**: Strategic academic guidance synthesis

## Demo Environment

The application includes sample student data for demonstration purposes, showcasing:
- Multi-semester grade tracking
- Various course branch representations
- Carryover scenarios and handling
- Complete statistical analysis pipeline

## Statistical Methodologies

### Exponential Moving Averages (EMAs)
- Tracks performance momentum over time
- Identifies trend reversals and acceleration points
- Provides early warning systems for academic intervention

### Correlation Analysis
- Pearson correlation coefficients for linear relationships
- Multi-factor analysis including units, courses, and GPA metrics
- Statistical significance testing for reliable insights

### Partial Correlation
- Controls for confounding variables in performance analysis
- Isolates true impact of individual course branches
- Enables precise academic strategy formulation

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL (for local development)
- Modern web browser

### Installation
```bash
# Clone the repository
git clone https://github.com/yungKnight/results_analytics.git

# Navigate to project directory
cd results_analytics

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (choose one)
# For basic usage:
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### Usage
1. Visit [edunalytica.onrender.com](https://edunalytica.onrender.com) for the live demo
2. For local development, launch the Django development server
3. The demo data will be automatically loaded from the PostgreSQL database
4. Navigate through the analysis sections to explore insights
5. Review recommendations in the strategic guidance section

## Database Schema

The application uses a PostgreSQL database with optimized tables for:
- Student grade records
- Course and semester management

## Analysis Output Structure

### Performance Metrics
- Semester-wise GPA calculations
- Cumulative CGPA tracking
- Course branch performance indices
- Unit completion rates

### Statistical Indicators
- EMA-based trend analysis
- Correlation matrices
- Partial correlation coefficients
- Performance divergence scores

### Actionable Insights
- Course selection recommendations
- Optimal unit load suggestions
- Academic strategy optimization
- Performance improvement pathways

## Contributing

Contributions are welcome! Please ensure any statistical methodologies added are academically sound and properly documented.

## License

MIT License

Copyright (c) 2025 EduNalytica

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

*EduNalytica - Transforming academic data into actionable insights for educational excellence.*