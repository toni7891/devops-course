import { Router, type Request, type Response, type NextFunction, type RequestHandler } from 'express';
import { userController } from './user.controller.js';
import { validate } from '../../middleware/validate.js';
import { createUserSchema, updateUserSchema, idParamSchema } from './user.schema.js';

const asyncH = (fn: RequestHandler): RequestHandler =>
  (req: Request, res: Response, next: NextFunction) =>
    Promise.resolve(fn(req, res, next)).catch(next);

const router = Router();

router.get('/', asyncH(userController.list));
router.post('/', validate(createUserSchema), asyncH(userController.create));
router.get('/:id', validate(idParamSchema, 'params'), asyncH(userController.get));
router.patch('/:id', validate(idParamSchema, 'params'), validate(updateUserSchema), asyncH(userController.update));
router.delete('/:id', validate(idParamSchema, 'params'), asyncH(userController.remove));

export default router;
