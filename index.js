const http = require('http');
const { spawn } = require('node:child_process');
const fs = require('fs');

const API_KEY = 'AIzaSyCyJ9L9hv_VvDEWYmOkRfmxEeZgwYUauWI';

function findPlace(place) {
    const url = `https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=${place}&inputtype=textquery&key=${API_KEY}`;

    fetch(url, {
        method: 'GET',
        headers: {},
    }).then(res => res.json()).then(res => {
        console.log(`findPlace(${place}): `, res);
        getPlaceDetails(res.candidates[0].place_id);
    });
}

function getPlaceDetails(placeID) {
    const url = `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeID}&key=${API_KEY}`;

    fetch(url, {
        method: 'GET',
        headers: {},
    }).then(res => res.json()).then(res => {
        const location = res.result.geometry.location;
        const demo = spawn('python', ['engine/demo.py', location.lat.toString(), location.lng.toString()]);
        demo.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        demo.on('close', (code) => {
            console.log(`child process exited with code ${code}`);

            const run = spawn('python', ['engine/run.py'])

            run.stdout.on('data', (data) => console.log(`stdout: ${data}`));

            run.on('close', (code2) => {
                console.log(`child process exited with code ${code2}`);
            })
        });
    });
}

http.createServer(function(request, response) {
    if (request.method === 'GET' && request.url === '/') {
        response.writeHead(200);

        const path = '/home/joey/js/senior-design/index.html';
        fs.createReadStream(path).pipe(response);
    }
    else if (request.method === 'POST' && request.url === '/save-config') {
        let body = '';
        request.on('data', data => body += data);
        request.on('end', () => {
            const path = '/home/joey/js/senior-design/config.json';
            fs.writeFile(path, body, (err) => {
                if (err) {
                    console.log(err);
                }
                else {
                    console.log('config updated');
                    const jsonReq = JSON.parse(body);
                    const place = jsonReq.location;

                    findPlace(place);
                }
            });
        });
    }
}).listen(3000);
