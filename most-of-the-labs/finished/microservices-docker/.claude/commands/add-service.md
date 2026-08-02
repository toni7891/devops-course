# Add API Service with TanStack Query

Create an API service layer with TanStack Query hooks for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Client/src/services/api.ts` (axios instance)
- `Client/src/services/users.ts` (service function pattern)
- `Client/src/main.tsx` (QueryClientProvider setup)

## Steps

### 1. Service functions in `Client/src/services/<resource>.ts`
- Import the shared axios instance: `import api from './api'`
- Named async functions for each operation:
  ```typescript
  export const get<Resources> = async () => {
    const { data } = await api.get("/api/<resources>");
    return data.data;
  };

  export const get<Resource>ById = async (id: string) => {
    const { data } = await api.get(`/api/<resources>/${id}`);
    return data.data;
  };

  export const create<Resource> = async (payload: Create<Resource>Payload) => {
    const { data } = await api.post("/api/<resources>", payload);
    return data.data;
  };

  export const update<Resource> = async (id: string, payload: Update<Resource>Payload) => {
    const { data } = await api.patch(`/api/<resources>/${id}`, payload);
    return data.data;
  };

  export const delete<Resource> = async (id: string) => {
    const { data } = await api.delete(`/api/<resources>/${id}`);
    return data.data;
  };
  ```
- Auth token is already set globally by `AppInitializer.tsx` — no manual headers needed
- Response format: server returns `{ success: true, data: ... }`, so always `return data.data`

### 2. TanStack Query hook in `Client/src/hooks/use<Resource>.ts`
- Import from `@tanstack/react-query`
- Import service functions
- Create typed hooks:
  ```typescript
  import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

  const QUERY_KEY = "<resources>";

  export const use<Resources> = () => {
    return useQuery({
      queryKey: [QUERY_KEY],
      queryFn: get<Resources>,
    });
  };

  export const use<Resource> = (id: string) => {
    return useQuery({
      queryKey: [QUERY_KEY, id],
      queryFn: () => get<Resource>ById(id),
      enabled: !!id,
    });
  };

  export const useCreate<Resource> = () => {
    const queryClient = useQueryClient();
    return useMutation({
      mutationFn: create<Resource>,
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      },
    });
  };

  export const useUpdate<Resource> = () => {
    const queryClient = useQueryClient();
    return useMutation({
      mutationFn: ({ id, payload }: { id: string; payload: Update<Resource>Payload }) =>
        update<Resource>(id, payload),
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      },
    });
  };

  export const useDelete<Resource> = () => {
    const queryClient = useQueryClient();
    return useMutation({
      mutationFn: delete<Resource>,
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      },
    });
  };
  ```

### 3. TypeScript types
- Define payload types in `Client/src/types/<resource>Types.ts` or reuse from server types if shared
- Add to `Client/src/types/index.ts` re-exports

## Usage in components
```typescript
const { data, isLoading, error } = use<Resources>();
const createMutation = useCreate<Resource>();
createMutation.mutate(payload);
```
