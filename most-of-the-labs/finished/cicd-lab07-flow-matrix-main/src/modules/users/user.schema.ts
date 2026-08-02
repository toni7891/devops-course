import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

export const updateUserSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  email: z.string().email().optional(),
}).refine((v) => Object.keys(v).length > 0, { message: 'At least one field required' });

export const idParamSchema = z.object({
  id: z.string().uuid(),
});

export type CreateUserDto = z.infer<typeof createUserSchema>;
export type UpdateUserDto = z.infer<typeof updateUserSchema>;
