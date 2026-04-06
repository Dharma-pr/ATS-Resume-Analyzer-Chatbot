const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Routes
app.get('/', (req, res) => {
    res.send('Welcome to the ATS Resume Analyzer Chatbot API!');
});

// Example route
app.post('/analyze', (req, res) => {
    const resumeData = req.body;
    // Perform analysis on resumeData
    res.json({ message: 'Resume analyzed!', data: resumeData });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
