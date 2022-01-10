const { spawn } = require('child_process'); 
const express = require('express')
const app = express()

app.use(express.static("public"))
const PORT = process.env.PORT || 5000;

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

app.get('/time', (req, res) => {
    var dataToSend;
    const python = spawn('python', ['time.py']);
    python.stdout.on('data', (data) => {
        dataToSend = data.toString();
    });
    python.on('close', (code) => {
        console.log(`The child process closed with code ${code}`);
        // Send data to browser
        res.json({'time' : dataToSend});
        });
})

// const http = require('http');
// const path = require('path');
// const fs = require('fs');

// const server = http.createServer((req, res) => {
//     if(req.url === '/') {
//         fs.readFile(path.join(__dirname, 'public', 'index.html', ), (err, content) => {
//             if(err) throw err;
//             res.writeHead(200, {'Content-Type': 'text/html'});
//             res.end(content)
//         })
//     }
// });

app.listen(PORT, () => console.log(`The application is running on the following port ${PORT}`));