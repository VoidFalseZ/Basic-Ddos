const http = require('http');

const requestLog = {}; // Stores request count per IP

const server = http.createServer((req, res) => {
    const ip = req.socket.remoteAddress; // Get the client's IP address
    const now = Date.now();

    // Initialize request log for the IP if not present
    if (!requestLog[ip]) {
        requestLog[ip] = { count: 1, startTime: now };
    } else {
        requestLog[ip].count += 1;
    }

    // Calculate the time difference from the first request
    const timeElapsed = now - requestLog[ip].startTime;

    // If within 10 seconds, check for flood attack
    if (timeElapsed < 10000 && requestLog[ip].count > 50) { // Adjust threshold as needed
        console.log(`⚠️ Possible flood attack detected from ${ip}: ${requestLog[ip].count} requests in ${timeElapsed / 1000}s`);
    } else if (timeElapsed >= 10000) {
        // Reset count every 10 seconds
        requestLog[ip] = { count: 1, startTime: now };
    }

    // Log each request
    console.log(`[${new Date().toISOString()}] ${ip} -> ${req.method} ${req.url}`);

    // Send response
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Server is running!\n');
});

const port = 3000;
server.listen(port, () => {
    console.log(`Server running on port ${port}`);
});