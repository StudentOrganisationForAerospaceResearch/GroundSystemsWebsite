const { spawn } = require('child_process'); 
const express = require('express');
const app = express();

app.use(express.static("public"));
const PORT = 80;

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

var dataToSend, newDataToSend, IMU_DATA_ACCEL, IMU_DATA_GYRO, BAR_DATA_PRESS, BAR_DATA_TEMP,
GPS_DATA_TIME, GPS_DATA_LAT_DEG, GPS_DATA_LAT_MINS, GPS_DATA_LONG_DEGS, GPS_DATA_LONG_MINS, GPS_DATA_ALT_METERS, OXI_DATA_PRESS_PSI, CMB_DATA_PRESS_PSI, PHS_DATA;
app.get('/time', (req, res) => {
    const python = spawn('python', ['rs232.py']);
    python.stdout.on('data', (data) => {
        dataToSend = data.toString();
        newDataToSend = dataToSend.split('~ ');
        IMU_DATA_ACCEL = newDataToSend[0];
        IMU_DATA_GYRO = newDataToSend[1];
        BAR_DATA_PRESS = newDataToSend[2];
        BAR_DATA_TEMP = newDataToSend[3];
        GPS_DATA_TIME = newDataToSend[4];
        GPS_DATA_LAT_DEG = newDataToSend[5];
        GPS_DATA_LAT_MINS = newDataToSend[6];
        GPS_DATA_LONG_DEGS = newDataToSend[7];
        GPS_DATA_LONG_MINS = newDataToSend[8];
        GPS_DATA_ALT_METERS = newDataToSend[9];
        OXI_DATA_PRESS_PSI = newDataToSend[10];
        CMB_DATA_PRESS_PSI = newDataToSend[11];
        PHS_DATA = newDataToSend[12];
    });
   
    python.on('close', (code) => {
        console.log(`The child process closed with code ${code}`);
        // Send data to browser
        res.json({'test1' : IMU_DATA_ACCEL, 'test2': IMU_DATA_GYRO, 'test3': BAR_DATA_PRESS, 
    "test4": BAR_DATA_TEMP, "test5": GPS_DATA_TIME, "test6": GPS_DATA_LAT_DEG, "test7": GPS_DATA_LAT_MINS, "test8": GPS_DATA_LONG_DEGS,
    "test9": GPS_DATA_LONG_MINS,"test10": GPS_DATA_ALT_METERS,"test11": OXI_DATA_PRESS_PSI, "test12": CMB_DATA_PRESS_PSI, "test13": PHS_DATA });
        });
});

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
