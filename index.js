const http = require('http');
const fs = require('fs');

const API_KEY = '';

function findPlace(place) {
    const url = `https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=${place}&inputtype=textquery&key=${API_KEY}`;

    fetch(url, {
        method: 'GET',
        headers: {},
    }).then(res => res.json()).then(res => {
        getPlaceDetails(res.candidates[0].place_id);
    });
}

function getPlaceDetails(placeID) {
    const url = `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeID}&key=${API_KEY}`;

    fetch(url, {
        method: 'GET',
        headers: {},
    }).then(res => res.json()).then(res => {
        console.log(res.result.geometry.location);
        getGeocoding(encodeURIComponent(res.result.formatted_address))
    });
}

function getGeocoding(address) {
    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${API_KEY}`;

    console.log(url);

    fetch(url, {
        method: 'GET',
        headers: {},
    }).then(res => res.json()).then(res => console.log(res));
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
