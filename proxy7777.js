const net = require('net');

const server = net.createServer(src => {
  const dst = net.connect(8000, '127.0.0.1');
  src.pipe(dst);
  dst.pipe(src);
  src.on('error', () => dst.destroy());
  dst.on('error', () => src.destroy());
});

server.listen(7777, '0.0.0.0', () => {
  console.log('🚀 Javis OS Port Forwarder: http://localhost:7777 -> http://localhost:8000 active!');
});
