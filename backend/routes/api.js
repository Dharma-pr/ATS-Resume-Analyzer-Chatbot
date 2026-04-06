const express = require('express');
const router = express.Router();
const resumeController = require('../controllers/resumeController');
const jobController = require('../controllers/jobController');

// Resume routes
router.post('/upload', resumeController.uploadResume);
router.get('/analyze/:id', resumeController.analyzeResume);

// Job recommendation routes
router.get('/jobs', jobController.getJobRecommendations);

module.exports = router;