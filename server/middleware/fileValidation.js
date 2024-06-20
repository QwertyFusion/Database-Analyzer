export function fileValidation(req, res, next) {
    const databaseFile = req.files['databaseFile'][0];
    const schemaFile = req.files['schemaFile'][0];

    const errors = [];

    if (databaseFile.mimetype !== 'text/csv') {
        errors.push('Database file must be a CSV.');
    }

    if (schemaFile.mimetype !== 'application/json') {
        errors.push('Schema file must be a JSON.');
    }

    if (errors.length > 0) {
        req.fileValidationErrors = errors.join(' ');
    }

    next();
}
