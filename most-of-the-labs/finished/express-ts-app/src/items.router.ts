import { Router, Request, Response } from 'express'

export interface Item {
  id: number
  name: string
}

const items: Item[] = []
let nextId = 1

export const itemsRouter = Router()

// list
itemsRouter.get('/', (_req: Request, res: Response) => {
  res.json(items)
})

// read one
itemsRouter.get('/:id', (req: Request, res: Response) => {
  const item = items.find((i) => i.id === Number(req.params.id))
  if (!item) return res.status(404).json({ error: 'not found' })
  res.json(item)
})

// create
itemsRouter.post('/', (req: Request, res: Response) => {
  const name = req.body?.name
  if (typeof name !== 'string' || name.trim() === '') {
    return res.status(400).json({ error: 'name is required' })
  }
  const item: Item = { id: nextId++, name }
  items.push(item)
  res.status(201).json(item)
})

// update
itemsRouter.put('/:id', (req: Request, res: Response) => {
  const item = items.find((i) => i.id === Number(req.params.id))
  if (!item) return res.status(404).json({ error: 'not found' })
  const name = req.body?.name
  if (typeof name !== 'string' || name.trim() === '') {
    return res.status(400).json({ error: 'name is required' })
  }
  item.name = name
  res.json(item)
})

// delete
itemsRouter.delete('/:id', (req: Request, res: Response) => {
  const idx = items.findIndex((i) => i.id === Number(req.params.id))
  if (idx === -1) return res.status(404).json({ error: 'not found' })
  const [removed] = items.splice(idx, 1)
  res.json(removed)
})
