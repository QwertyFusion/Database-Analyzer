import axios from 'axios';
import FormData from 'form-data';

export async function processQuestion(question, csvData) {
    try {
        const formData = new FormData();
        formData.append('question', question);
        formData.append('csvData', JSON.stringify(csvData));

        const response = await axios.post('http://localhost:5000/process', formData, {
            headers: formData.getHeaders()
        });

        // Handle different response formats
        let responseData = response.data;

        if (Array.isArray(responseData)) {
            // If response is an array, join elements into a string
            responseData = responseData.map(item => JSON.stringify(item)).join(', ');
        } else if (typeof responseData === 'object') {
            // If response is an object, stringify it
            responseData = JSON.stringify(responseData);
        }

        console.log('Answer:', responseData);
        return { answer: responseData };
    } catch (error) {
        console.error('Error processing question:', error);
        return { error: error.message };
    }
}
