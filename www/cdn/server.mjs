import { createServer } from 'node:http';
import { readFile, statSync, readdirSync } from 'node:fs';
import { extname, join, relative } from 'node:path';

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
  let urlPath = decodeURIComponent(req.url);
  let filePath = join(PUBLIC_DIR, urlPath);

  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=UTF-8' });
    return res.end('Access Denied.');
  }

  try {
    const stats = statSync(filePath);

    // Ако е директория – генерираме HTML списък със съдържанието ѝ
    if (stats.isDirectory()) {
      const files = readdirSync(filePath, { withFileTypes: true });
      
      // Изчисляваме относителния път спрямо public за линковете
      let relativePath = relative(PUBLIC_DIR, filePath);
      if (relativePath && !relativePath.endsWith('/')) relativePath += '/';
      const parentPath = relativePath ? '/' + relativePath.split('/').slice(0, -2).join('/') : null;

      let listHtml = '';
      
      // Бутон за нагоре (ако не сме в корена)
      if (relativePath) {
        const upLink = parentPath === '' || parentPath === '/' ? '/' : parentPath;
        listHtml += `<li>📁 <a href="${upLink}">.. [Нагоре]</a></li>`;
      }

      files.forEach(file => {
        const isDir = file.isDirectory();
        const fileName = file.name;
        const fileHref = '/' + join(relativePath, fileName).replace(/\\/g, '/');
        const icon = isDir ? '📁' : '📄';
        
        listHtml += `<li style="margin: 0.4rem 0;">${icon} <a href="${fileHref}">${fileName}${isDir ? '/' : ''}</a></li>`;
      });

      res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
      return res.end(`
        <!DOCTYPE html>
        <html lang="bg">
        <head>
            <meta charset="UTF-8">
            <title>Index of /${relativePath}</title>
            <link rel="stylesheet" href="/css/style.css">
            <style>
                body { font-family: sans-serif; padding: 2rem; background: #f9f9f9; }
                .box { max-width: 700px; margin: 0 auto; background: #fff; padding: 2rem; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
                ul { list-style: none; padding: 0; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="box">
                <h2>Index of /${relativePath}</h2>
                <ul>${listHtml}</ul>
            </div>
        </body>
        </html>
      `);
    }

    // Ако е нормален файл – четем го и го връщаме
    readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
        return res.end('Not Found.');
      }

      const ext = extname(filePath).toLowerCase();
      const contentType = mimeTypes[ext] || 'application/octet-stream';

      res.writeHead(200, { 'Content-Type': contentType });
      res.end(data);
    });

  } catch (err) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
    res.end('Not Found.');
  }
}

const server = createServer(httpHandler);

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Listening on 127.0.0.1:${PORT}`);
});