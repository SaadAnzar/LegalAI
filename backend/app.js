const express = require('express');
const app = express();
const fs = require('fs');
var path = require('path')
const cors = require('cors');
var download = require('download-pdf');
const axios = require('axios');

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors(
    {
        origin: '*',
        credentials: true
    }
));

app.get('/', (req, res) => {
    res.json({ message: 'Welcome to Legal AI backend' });
});

app.post('/pdf', (req, res) => {
    let pdf = req.body.pdfURL;
    let fileName = 'pdf-' + Date.now() + '.pdf';
    let filePath = path.join('./pdfs/', fileName);

    let options = {
        directory: "./pdfs/",
        filename: fileName
    }

    download(pdf, options, function (err) {
        if (err) {
            console.log(err);
            return res.status(500).json({ message: 'Error while downloading PDF' });
        }
        console.log("Done");

        axios.post('http://127.0.0.1:5000/', {
            fileName: fileName,
        })
            .then(function (response) {
                console.log(response);
                return res.status(200).json({ message: 'PDF fileName sent' });
            })
            .catch(function (error) {
                console.log(error);
                return res.status(500).json({ message: 'Error while sending PDF fileName' });
            });
    })

});

app.listen(8800, () => {
    console.log('Legal AI Backend listening on Port 8800!');
});