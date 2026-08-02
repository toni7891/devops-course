import { randomUUID } from 'node:crypto';

export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

export interface CreateUserInput {
  name: string;
  email: string;
}

export type UpdateUserInput = Partial<CreateUserInput>;

const users = new Map<string, User>();

export const userStore = {
  list(): User[] { return [...users.values()]; },
  get(id: string): User | undefined { return users.get(id); },
  findByEmail(email: string): User | undefined {
    return [...users.values()].find((u) => u.email === email);
  },
  create({ name, email }: CreateUserInput): User {
    const user: User = { id: randomUUID(), name, email, createdAt: new Date().toISOString() };
    users.set(user.id, user);
    return user;
  },
  update(id: string, patch: UpdateUserInput): User | null {
    const existing = users.get(id);
    if (!existing) return null;
    const updated: User = { ...existing, ...patch };
    users.set(id, updated);
    return updated;
  },
  delete(id: string): boolean { return users.delete(id); },
  _reset(): void { users.clear(); },
};
