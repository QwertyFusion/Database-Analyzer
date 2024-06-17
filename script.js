document.getElementById('upload-database').addEventListener('click', function() {
    const databaseFile = document.getElementById('database-file').files[0];
    if (databaseFile) {
        uploadFile(databaseFile, 'database');
    } else {
        alert('Please select a database file.');
    }
});

document.getElementById('upload-schema').addEventListener('click', function() {
    const schemaFile = document.getElementById('schema-file').files[0];
    if (schemaFile) {
        uploadFile(schemaFile, 'schema');
    } else {
        alert('Please select a schema file.');
    }
});

function uploadFile(file, type) {
    const formData = new FormData();
    formData.append(type, file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(`${type} upload successful:`, data);
        alert(`${type.charAt(0).toUpperCase() + type.slice(1)} upload successful.`);
    })
    .catch(error => {
        console.error(`${type} upload error:`, error);
        alert(`Failed to upload ${type}.`);
    });
}
