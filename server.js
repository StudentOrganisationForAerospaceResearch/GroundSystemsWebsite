const { spawn } = require('child_process'); 
const express = require('express')
const app = express()

app.use(express.static("public"))
const PORT = 80;

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


//------------- Workday 10th Feb-----------------
const { spawn } = require('child_process'); 
const express = require('express')
const app = express()

app.use(express.static("public"))
const PORT = 80;

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

var dataToSend, newDataToSend, IMU_DATA_ACCEL, IMU_DATA_GYRO, COMPLETE_DATA;
app.get('/time', (req, res) => {
    const python = spawn('python', ['rs232.py']);
    python.stdout.on('data', (data) => {
        dataToSend = data.toString();
        newDataToSend = dataToSend.split('~ ')
        IMU_DATA_ACCEL = newDataToSend[0];
        IMU_DATA_GYRO = newDataToSend[1];
    });
   
    python.on('close', (code) => {
        console.log(`The child process closed with code ${code}`);
        // Send data to browser
        res.json({'test1' : IMU_DATA_ACCEL, 'test2': IMU_DATA_GYRO});
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
