import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { extname, join, normalize } from 'node:path'

const PORT = process.env.PORT || 8080
const ROOT = join(process.cwd(), 'dist')

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
}

async function sendFile(res, path) {
  const body = await readFile(path)
  res.writeHead(200, { 'content-type': MIME[extname(path)] || 'application/octet-stream' })
  res.end(body)
}

const server = createServer(async (req, res) => {
  try {
    const urlPath = decodeURIComponent((req.url || '/').split('?')[0])
    const safe = normalize(urlPath).replace(/^(\.\.[/\\])+/, '')
    const target = join(ROOT, safe === '/' ? 'index.html' : safe)
    try {
      await sendFile(res, target)
    } catch {
      // SPA fallback
      await sendFile(res, join(ROOT, 'index.html'))
    }
  } catch (err) {
    res.writeHead(500)
    res.end('Internal Server Error')
    console.error(err)
  }
})

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Serving dist/ on http://0.0.0.0:${PORT}`)
})
