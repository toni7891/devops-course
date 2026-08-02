import express, { Request, Response } from 'express'
import { itemsRouter } from './items.router'

const app = express()
const PORT = Number(process.env.PORT) || 3000

app.use(express.json())

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' })
})

app.use('/items', itemsRouter)

app.listen(PORT, '0.0.0.0', () => {
  console.log(`express-ts-app listening on http://0.0.0.0:${PORT}`)
})
