import { userStore, type User, type CreateUserInput, type UpdateUserInput } from './user.store.js';
import { HttpError } from '../../errors/HttpError.js';

export const userService = {
  list(): User[] {
    return userStore.list();
  },
  get(id: string): User {
    const user = userStore.get(id);
    if (!user) throw HttpError.notFound(`User ${id} not found`);
    return user;
  },
  create(data: CreateUserInput): User {
    if (userStore.findByEmail(data.email)) {
      throw HttpError.conflict(`Email ${data.email} already in use`);
    }
    return userStore.create(data);
  },
  update(id: string, patch: UpdateUserInput): User | null {
    this.get(id);
    if (patch.email) {
      const existing = userStore.findByEmail(patch.email);
      if (existing && existing.id !== id) throw HttpError.conflict('Email already in use');
    }
    return userStore.update(id, patch);
  },
  remove(id: string): void {
    this.get(id);
    userStore.delete(id);
  },
};
