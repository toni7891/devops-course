# Add Test

Create tests for: $ARGUMENTS

Determine if this is a Server or Client test based on the file path or context.

Read the source file to test before writing the test. Read the relevant vitest config to confirm settings.

## Server Tests

**Config**: `Server/vitest.config.ts` — node environment, `@/` path alias, globals enabled
**Test location**: Co-located with source as `<filename>.test.ts`

### Controller test pattern
```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { Request, Response } from "express";

// Mock dependencies before imports
vi.mock("@/models/<resource>Model");

import <Resource>Controller from "@/controllers/<resource>Controllers";
import <Resource> from "@/models/<resource>Model";

describe("<Resource>Controller", () => {
  let controller: <Resource>Controller;
  let mockReq: Partial<Request>;
  let mockRes: Partial<Response>;

  beforeEach(() => {
    controller = new <Resource>Controller();
    mockReq = { body: {}, params: {} };
    mockRes = {
      status: vi.fn().mockReturnThis(),
      json: vi.fn().mockReturnThis(),
    };
    vi.clearAllMocks();
  });

  describe("get<Resources>", () => {
    it("should return all resources with 200", async () => {
      const mockData = [{ _id: "1", name: "Test" }];
      vi.mocked(<Resource>.find).mockResolvedValue(mockData);

      await controller.get<Resources>(mockReq as Request, mockRes as Response);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ success: true, data: mockData });
    });
  });

  describe("get<Resource>ById", () => {
    it("should return 404 when resource not found", async () => {
      mockReq.params = { id: "nonexistent" };
      vi.mocked(<Resource>.findById).mockResolvedValue(null);

      await expect(
        controller.get<Resource>ById(mockReq as Request, mockRes as Response)
      ).rejects.toThrow();
    });
  });
});
```

### Zod schema test pattern
```typescript
import { describe, it, expect } from "vitest";
import { create<Resource>Schema, update<Resource>Schema } from "@/zod/<resource>Zod";

describe("create<Resource>Schema", () => {
  it("should validate correct data", () => {
    const validData = { /* all required fields */ };
    const result = create<Resource>Schema.safeParse(validData);
    expect(result.success).toBe(true);
  });

  it("should reject missing required fields", () => {
    const result = create<Resource>Schema.safeParse({});
    expect(result.success).toBe(false);
  });

  it("should reject invalid field values", () => {
    const invalidData = { /* field with wrong type/format */ };
    const result = create<Resource>Schema.safeParse(invalidData);
    expect(result.success).toBe(false);
  });
});

describe("update<Resource>Schema", () => {
  it("should allow partial updates", () => {
    const partialData = { /* only one field */ };
    const result = update<Resource>Schema.safeParse(partialData);
    expect(result.success).toBe(true);
  });
});
```

### Middleware test pattern
```typescript
import { describe, it, expect, vi } from "vitest";
import { Request, Response, NextFunction } from "express";

import { myMiddleware } from "@/middleware/myMdw";

describe("myMiddleware", () => {
  it("should call next() on valid request", () => {
    const req = { /* mock request */ } as Partial<Request>;
    const res = {} as Partial<Response>;
    const next = vi.fn() as NextFunction;

    myMiddleware(req as Request, res as Response, next);

    expect(next).toHaveBeenCalled();
  });
});
```

## Client Tests

**Config**: `Client/vitest.config.ts` — jsdom environment, globals enabled
**Setup file**: `Client/src/test/setup.ts` — imports `@testing-library/jest-dom/vitest`
**Test location**: Co-located with source as `<filename>.test.tsx` (or `.test.ts` for non-component code)

### Component test pattern
```typescript
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import <Component> from "@/components/<Level>/<Component>";

describe("<Component>", () => {
  it("should render correctly", () => {
    render(<<Component> />);
    expect(screen.getByText("expected text")).toBeInTheDocument();
  });

  it("should handle className prop", () => {
    const { container } = render(<<Component> className="custom" />);
    expect(container.firstChild).toHaveClass("custom");
  });

  it("should handle click events", async () => {
    const user = userEvent.setup();
    const onClick = vi.fn();
    render(<<Component> onClick={onClick} />);

    await user.click(screen.getByRole("button"));
    expect(onClick).toHaveBeenCalledOnce();
  });
});
```

### Component with providers (Auth0, Redux, Router)
```typescript
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import { configureStore } from "@reduxjs/toolkit";

import <Component> from "@/pages/<Component>";
import userReducer from "@/redux/slices/userSlice";

const renderWithProviders = (ui: React.ReactElement) => {
  const store = configureStore({
    reducer: { user: userReducer },
    preloadedState: {
      user: { user: null, loading: false, error: null },
    },
  });

  return render(
    <Provider store={store}>
      <MemoryRouter>{ui}</MemoryRouter>
    </Provider>
  );
};

describe("<Component>", () => {
  it("should render", () => {
    renderWithProviders(<<Component> />);
    expect(screen.getByText("expected text")).toBeInTheDocument();
  });
});
```

### TanStack Query hook test pattern
```typescript
import { describe, it, expect, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { use<Resources> } from "@/hooks/use<Resource>";

vi.mock("@/services/<resource>", () => ({
  get<Resources>: vi.fn().mockResolvedValue([{ _id: "1", name: "Test" }]),
}));

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};

describe("use<Resources>", () => {
  it("should fetch resources", async () => {
    const { result } = renderHook(() => use<Resources>(), { wrapper });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(1);
  });
});
```

## Steps

1. Read the source file to understand its interface and dependencies
2. Determine Server or Client based on file path
3. Create test file as `<filename>.test.ts` (or `.test.tsx` for React components) next to the source
4. Follow the appropriate pattern above
5. Cover: happy path, edge cases, error handling, boundary conditions
6. Run the test to verify it passes
