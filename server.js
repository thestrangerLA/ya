// ==========================================
// Local Web Server for Chicken Farm Health Guide
// Standard Node.js HTTP server (No external npm packages required)
// ==========================================

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  // Normalize URL path
  let reqPath = decodeURI(req.url.split('?')[0]);

  // API Endpoint for saving and reading self-service orders
  const ordersFile = path.join(PUBLIC_DIR, 'orders.json');
  if (reqPath === '/api/orders' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const newOrder = JSON.parse(body);
        let orders = [];
        if (fs.existsSync(ordersFile)) {
          orders = JSON.parse(fs.readFileSync(ordersFile, 'utf8') || '[]');
        }
        orders.unshift(newOrder);
        fs.writeFileSync(ordersFile, JSON.stringify(orders, null, 2), 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ ok: true, orderId: newOrder.orderId }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }

  if (reqPath === '/api/orders' && req.method === 'GET') {
    let orders = [];
    if (fs.existsSync(ordersFile)) {
      try { orders = JSON.parse(fs.readFileSync(ordersFile, 'utf8') || '[]'); } catch (e) {}
    }
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(orders));
    return;
  }

  if (reqPath === '/' || reqPath === '') {
    reqPath = '/index.html';
  }

  const filePath = path.join(PUBLIC_DIR, reqPath);

  // Security check: ensure within public dir
  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache'
    });

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
  });
});

// Helper to get local network IP
function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

server.listen(PORT, () => {
  const localIP = getLocalIP();
  console.log('========================================================');
  console.log(' 🐔 คู่มือโรคและพยาธิในไก่ (Chicken Farm Guide) เปิดทำงานแล้ว!');
  console.log('========================================================');
  console.log(` • บนเครื่องนี้:   http://localhost:${PORT}`);
  console.log(` • บนมือถือในฟาร์ม (Wi-Fi เดียวกัน): http://${localIP}:${PORT}`);
  console.log('========================================================');
  console.log(' กด Ctrl+C เพื่อหยุดการทำงานของเซิร์ฟเวอร์');
});
