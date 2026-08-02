# Add Mongoose Model

Create a Mongoose model with TypeScript types and Zod validation for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Server/src/types/usersTypes.ts`
- `Server/src/models/userModel.ts`
- `Server/src/zod/usersZod.ts`

## Steps

### 1. TypeScript types in `Server/src/types/<feature>Types.ts`
- `I<Feature>` — plain interface with business fields
- `I<Feature>Doc extends I<Feature>, Document` — Mongoose document interface
- `I<Feature>Model extends Model<I<Feature>Doc>` — model interface with static methods
- Export all as named exports

### 2. Mongoose model in `Server/src/models/<feature>Model.ts`
- Import types from `@/types/<feature>Types`
- Define schema: `new Schema<I<Feature>Doc>({...}, { timestamps: true })`
- Add field validations: required, unique, enum, default values
- Add static methods on `schema.statics` for common queries
- Enable virtuals in toJSON/toObject: `{ virtuals: true }`
- Export: `mongoose.model<I<Feature>Doc, I<Feature>Model>("<Feature>", schema)`

### 3. Zod validation in `Server/src/zod/<feature>Zod.ts`
- `create<Feature>Schema` — z.object() with all required fields and validators
- `update<Feature>Schema` — use `.partial()` or `.pick()` for optional update fields
- Use appropriate validators: `z.string().min(1)`, `z.string().email()`, `z.number().int()`, `z.enum([...])`, `z.string().optional()`
- Export as named exports

## Output
List the created files and their exports so the developer can import them in controllers and routes.
