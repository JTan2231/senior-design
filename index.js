const http = require('http');
const fs = require('fs');
const qs = require('querystring');

http.createServer(function (request, response) {
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
                }
            });
        });
    }
}).listen(3000);
