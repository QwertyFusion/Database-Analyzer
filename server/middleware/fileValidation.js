import Ajv from 'ajv';

const ajv = new Ajv();

const schemaValidationSchema = {
  type: 'object',
  properties: {
    columns: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          type: { type: 'string', enum: ['integer', 'string', 'date', 'float'] }
        },
        required: ['name', 'type'],
        additionalProperties: false
      }
    }
  },
  required: ['columns'],
  additionalProperties: false
};

export function fileValidation(req, res, next) {
  const databaseFile = req.files['databaseFile'][0];
  const schemaFile = req.files['schemaFile'][0];

  const errors = [];

  if (databaseFile.mimetype !== 'text/csv') {
    errors.push('Database file must be a CSV.');
  }

  if (schemaFile.mimetype !== 'application/json') {
    errors.push('Schema file must be a JSON.');
  } else {
    const schemaContent = schemaFile.buffer.toString();
    let schemaJson;
    try {
      schemaJson = JSON.parse(schemaContent);
    } catch (e) {
      errors.push('Schema file contains invalid JSON.');
    }

    const validate = ajv.compile(schemaValidationSchema);
    const valid = validate(schemaJson);

    if (!valid) {
      errors.push('Schema file is not in the correct format.');
    }
  }

  if (errors.length > 0) {
    req.fileValidationErrors = errors.join(' ');
  }

  next();
}
