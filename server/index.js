import express from 'express';
import multer from 'multer';
import path from 'path';
import { fileURLToPath } from 'url';
import { fileValidation } from './middleware/fileValidation.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

// Set storage engine to memory storage
const storage = multer.memoryStorage();

// Initialize upload
const upload = multer({
  storage: storage,
  limits: { fileSize: 25 * 1024 * 1024 }, // limit file size to 25MB
  fileFilter: (req, file, cb) => {
    checkFileType(file, cb);
  }
}).fields([
  { name: 'databaseFile', maxCount: 1 },
  { name: 'schemaFile', maxCount: 1 }
]);

// Check file type
function checkFileType(file, cb) {
    const filetypes = /csv|json/;
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = filetypes.test(file.mimetype);

    if (mimetype && extname) {
        return cb(null, true);
    } else {
        cb('Error: Only CSV and JSON files are allowed!');
    }
}

// Set EJS as templating engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Static folder
app.use(express.static(path.join(__dirname, '../public')));

// Route for file upload form
app.get('/', (req, res) => res.render('index'));

// Handle file uploads with validation middleware
app.post('/upload', upload, fileValidation, (req, res) => {
    const errors = req.fileValidationErrors;
    if (errors) {
        return res.json({ success: false, message: errors });
    }
    res.json({ success: true });
});

app.get('/chat', (req, res) => {
    res.send('Chat Page - Work in Progress');
});

app.listen(port, () => console.log(`Server started on port ${port}`));
