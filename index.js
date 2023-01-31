const http = require('http');
const fs = require('fs');
const qs = require('querystring');

http.createServer(function (request, response) {
    if (request.method === 'GET' && request.url === '/') {
        const path = '/home/joey/js/senior-design/index.html';
        response.writeHead(200);
        fs.createReadStream(path).pipe(response);
    }
    else if (request.method === 'POST' && request.url === '/save-config') {
        let body = '';
        let post;
        request.on('data', data => body += data);
        request.on('end', () => {
            const path = '/home/joey/js/senior-design/config.json';
            fs.writeFile(path, body, (err) => {
                if (err) {
                    console.log(err);
                    response.writeHead(400);
                }
                else {
                    console.log('config updated');
                    response.writeHead(200);
                }
            });
        });
    }
}).listen(3000);
