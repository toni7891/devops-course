# Add Component

Create a reusable component: $ARGUMENTS

Specify the Atomic Design level in the arguments (Atom, Molecule, or Organism). If not specified, determine the level based on complexity:
- **Atom**: Single-purpose UI element (button, badge, input, spinner)
- **Molecule**: Composition of atoms (card with title+text, form field with label+input)
- **Organism**: Complex section with logic (sidebar, header, data table, form)

Read these files before generating code to match exact patterns:
- `Client/src/lib/utils.ts` (cn utility for class merging)
- `Client/src/components/ui/button-variants.ts` (CVA variant pattern)
- Existing component at the same level for pattern reference:
  - Atom: `Client/src/components/Atoms/Badge.tsx` or `Client/src/components/Atoms/Card.tsx`
  - Molecule: `Client/src/components/Molecules/FeatureCard.tsx` or `Client/src/components/Molecules/Hero.tsx`
  - Organism: `Client/src/components/Organisms/Sidebar.tsx`

## Steps

### 1. Create component file
- **Atom**: `Client/src/components/Atoms/<Name>.tsx`
- **Molecule**: `Client/src/components/Molecules/<Name>.tsx`
- **Organism**: `Client/src/components/Organisms/<Name>.tsx`

### 2. Component structure
```typescript
import { cn } from "@/lib/utils";
// import atoms/molecules if composing
// import from lucide-react for icons
// import { motion } from "framer-motion" if animated

interface <Name>Props {
  // typed props with JSDoc comments for complex ones
  className?: string;  // always allow className override
}

const <Name> = ({ className, ...props }: <Name>Props) => {
  return (
    <div className={cn("base-classes", className)}>
      {/* content */}
    </div>
  );
};

export default <Name>;
```

### 3. If the component has variants, use CVA
```typescript
import { cva, type VariantProps } from "class-variance-authority";

const <name>Variants = cva("base-classes", {
  variants: {
    variant: {
      default: "...",
      primary: "...",
      secondary: "...",
    },
    size: {
      sm: "...",
      md: "...",
      lg: "...",
    },
  },
  defaultVariants: {
    variant: "default",
    size: "md",
  },
});

interface <Name>Props extends VariantProps<typeof <name>Variants> {
  className?: string;
}
```

### 4. Styling guidelines
- Use Tailwind CSS v4 utility classes
- Use `cn()` from `@/lib/utils` for conditional/merged classes
- Use `tailwind-merge` compatible patterns (cn handles this)
- For animations, use Framer Motion `motion` components
- For icons, use `lucide-react`
- Keep colors consistent with existing theme (check existing components)

### 5. Export
- Use `export default <Name>` (consistent with existing components)
