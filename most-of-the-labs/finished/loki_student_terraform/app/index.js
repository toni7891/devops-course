const http = require("http");
const os = require("os");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 8080;
const LOG_FILE = path.join(__dirname, "app.log");
const HOST = os.hostname();
const PID = process.pid;

const ROUTES = ["/users", "/products", "/orders", "/login", "/cart", "/checkout"];
const METHODS = ["GET", "GET", "GET", "POST", "PATCH", "DELETE"];
const CODES = ["200", "201", "300", "400", "401", "404", "500"];
const LEVELS = [30, 30, 30, 40, 50, 60];

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function writeLog(entry) {
  fs.appendFile(LOG_FILE, JSON.stringify(entry) + "\n", () => {});
}

function logRequest({ method, route, code }) {
  writeLog({
    level: pick(LEVELS),
    time: Date.now(),
    pid: PID,
    hostname: HOST,
    method,
    route,
    code,
  });
}

const server = http.createServer((req, res) => {
  const code = req.url === "/health" ? "200" : pick(CODES);
  logRequest({ method: req.method, route: req.url, code });
  res.writeHead(Number(code), { "Content-Type": "application/json" });
  res.end(JSON.stringify({ hostname: HOST, method: req.method, route: req.url, code }));
});

server.listen(PORT, () => {
  writeLog({ level: 30, time: Date.now(), pid: PID, hostname: HOST, msg: `api server listening on port ${PORT}` });
});

setInterval(() => {
  logRequest({ method: pick(METHODS), route: pick(ROUTES), code: pick(CODES) });
}, 1000);
