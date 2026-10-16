import { createServer } from 'node:http';
import { readFile } from 'node:fs';
import { extname, join } from 'node:path';

const PORT = 3000;
const PUBLIC_DIR = join(process.cwd(), 'public');

const mimeTypes = {
  '.html': 'text/html; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.js': 'text/javascript; charset=UTF-8',
  '.jpg': 'image/jpeg',
  '.png': 'image/png',
  '.txt': 'text/plain; charset=UTF-8',
  '.xml': 'application/xml; charset=UTF-8'
};

function httpHandler(req, res) {
  let urlPath = req.url === '/' ? '/index.html' : req.url;
  let filePath = join(PUBLIC_DIR, urlPath);

  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=UTF-8' });
    return res.end('Access Denied.');
  }

  readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
      res.end('Not Found.');
      return;
    }

    const ext = extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
 }
const server = createServer(httpHandler);

// starts a simple http server locally on port 3000
server.listen(PORT, '0.0.0.0', () => {
  console.log('Listening on 127.0.0.1:3000');
});