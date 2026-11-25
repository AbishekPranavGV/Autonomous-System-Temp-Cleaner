const https = require('https');

const BACKEND_HOST = 'margaret-operate-chemistry-zshops.trycloudflare.com';

module.exports = (req, res) => {
  let path = req.url || '/';

  // If Vercel rewrote to query parameter 'path'
  if (path.includes('/[...path]')) {
    if (req.query && req.query.path) {
      const qPath = Array.isArray(req.query.path) ? req.query.path.join('/') : req.query.path;
      path = '/api/' + qPath;
    } else {
      path = '/api';
    }
  }

  if (!path.startsWith('/api')) {
    path = '/api' + (path.startsWith('/') ? path : '/' + path);
  }

  const options = {
    hostname: BACKEND_HOST,
    port: 443,
    path: path,
    method: req.method,
    headers: {
      ...req.headers,
      host: BACKEND_HOST,
    },
  };

  const proxyReq = https.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res);
  });

  proxyReq.on('error', (err) => {
    res.writeHead(502, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: err.message, backend: BACKEND_HOST }));
  });

  req.pipe(proxyReq);
};
