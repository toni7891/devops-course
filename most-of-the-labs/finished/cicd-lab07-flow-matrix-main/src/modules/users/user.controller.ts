import type { Request, Response } from 'express';
import { userService } from './user.service.js';

export const userController = {
  list: (_req: Request, res: Response) => res.json(userService.list()),
  get: (req: Request, res: Response) => res.json(userService.get(req.params.id)),
  create: (req: Request, res: Response) => res.status(201).json(userService.create(req.body)),
  update: (req: Request, res: Response) => res.json(userService.update(req.params.id, req.body)),
  remove: (req: Request, res: Response) => {
    userService.remove(req.params.id);
    res.status(204).end();
  },
};
