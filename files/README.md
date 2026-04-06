# ATS Resume Analyzer with AI Chatbot

An intelligent resume analysis platform that combines ATS-style keyword matching with semantic understanding and an LLM-powered chatbot to provide job seekers with actionable feedback on resume rejections.

## 🎯 Features

- **Resume Parsing**: Extract and structure resume content from PDF, DOCX, or TXT files
- **Keyword Matching**: Compare resume keywords with job description requirements
- **Semantic Analysis**: Understand the meaning and categorization of resume content
- **Match Score**: Get an overall match percentage between resume and job description
- **AI Feedback**: Receive detailed, human-friendly feedback explaining rejection reasons
- **Smart Recommendations**: Get actionable suggestions to improve your resume
- **Interactive Chatbot**: Ask follow-up questions and get personalized guidance
- **Chat History**: Maintain conversation history for each analysis

## 🏗️ Architecture

```
Frontend (React + TypeScript)
        ↓
Backend API (Flask)
        ↓
Database (PostgreSQL)
        ↓
NLP Engine (spaCy) + LLM (OpenAI/Anthropic)
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- OpenAI API Key (or Anthropic API Key)

### Setup with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ATS-Resume-Analyzer-Chatbot
   ```

2. **Create environment file**
   ```bash
   cp backend/.env.example backend/.env
   ```

   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=sk-your-key
   ANTHROPIC_API_KEY=your-key
   ```

3. **Start services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Database: localhost:5432

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spacy model
python -m spacy download en_core_web_sm

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/ats_db"
export OPENAI_API_KEY="sk-your-key"

# Run server
python app.py
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📚 API Endpoints

### Upload Endpoints

- **POST** `/api/upload/resume` - Upload resume file
- **POST** `/api/upload/job-description` - Upload job description

### Analysis Endpoints

- **POST** `/api/analysis/analyze` - Analyze resume against job description

### Chatbot Endpoints

- **POST** `/api/chatbot/message` - Send chat message
- **GET** `/api/chatbot/history/<analysis_id>` - Get chat history

## 🔄 Workflow

1. **Upload Resume**: PDF, DOCX, or TXT format
2. **Paste Job Description**: Add job title and description text
3. **Analyze**: System processes and generates match score, keyword analysis, and initial feedback
4. **Chat**: Ask questions about why you were rejected and get recommendations
5. **Improve**: Implement suggestions and re-analyze with updated resume

## 🛠️ Technologies

### Backend
- Flask & Flask-CORS
- SQLAlchemy (ORM)
- PostgreSQL
- spaCy (NLP)
- OpenAI / Anthropic APIs

### Frontend
- React 18
- TypeScript
- Axios
- Lucide Icons
- React Markdown

### Deployment
- Docker & Docker Compose
- Cloud platforms (AWS, GCP, Azure)

## 📊 System Flow

```
Resume File → Text Extraction → Parsing → Keyword Extraction
                                              ↓
                                        Semantic Analysis
                                              ↓
Job Description → Keyword Extraction → Matching Engine
                                              ↓
                                        Similarity Scoring
                                              ↓
                                      LLM Feedback Generation
                                              ↓
                                        Chatbot Response
```

## 🤖 LLM Configuration

### OpenAI (Default)
```python
OPENAI_API_KEY=sk-your-key
LLM_MODEL=gpt-3.5-turbo
```

### Anthropic Claude
```python
ANTHROPIC_API_KEY=your-key
LLM_PROVIDER=anthropic
```

## 📈 Sample Output

```
Match Score: 65%

Matched Keywords: [Python, Flask, SQL, Docker]
Missing Keywords: [Kubernetes, AWS, Microservices]

Feedback:
Your resume shows good foundational skills in Python and web development.
However, the position requires Kubernetes and AWS experience which isn't 
clearly demonstrated in your current resume.

Recommendations:
1. Add Kubernetes project experience
2. Mention any AWS cloud experience
3. Highlight microservices architecture work
```

## 🔐 Security

- Environment variables for sensitive data
- Input validation and sanitization
- Secure file upload handling
- CORS configuration
- Database connection pooling

## 🐛 Troubleshooting

**Port Already in Use**
```bash
# Change ports in docker-compose.yml or .env
```

**Database Connection Error**
```bash
# Ensure PostgreSQL is running
# Check DATABASE_URL environment variable
```

**API Key Issues**
```bash
# Verify keys in .env file
# Check API usage limits
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

- Documentation: [docs/](./docs/)
- Issues: GitHub Issues
- Email: support@atsanalyzer.com

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] PDF export of analysis
- [ ] Resume templates
- [ ] Job board integration
- [ ] Analytics dashboard
- [ ] Video feedback
- [ ] Mobile app
- [ ] Real-time collaboration