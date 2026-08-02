# Step 01 – Explore the React Application

## Goal

Before writing any infrastructure, understand what you are deploying.  
You do **not** need to modify any application code.

---

## What You Have

You have been provided with a GitHub repository containing a working React application.  
The expected structure looks like this:

```
app/
│
├── src/              ← Application source code
├── public/           ← Static assets
├── package.json      ← Dependencies and scripts
├── vite.config.ts    ← Build configuration (TypeScript)
└── README.md
```

---

## Tasks

### 1. Clone the Repository

Clone the provided GitHub repository to your local machine.

> Think about where you want to store this project on your filesystem.

---

### 2. Inspect the Build Process

Open `package.json` and look at the `scripts` section.

- Which command builds the application for production?
- What folder does the build output go to? (this is usually `dist/` or `build/`)

> This output folder is what you will later upload to S3.

---

### 3. Run the Application Locally (Optional but Recommended)

Install the dependencies and run the app locally to confirm it works before you do anything else.

> If it doesn't run locally, it won't run in production either.

---

### 4. Build the Application Locally

Run the production build command.

- Confirm that the output folder is created.
- Open `index.html` from the output folder and inspect its contents.

> Note: you will not commit the build output to the repository. The CI/CD pipeline will build it automatically.

---

## Questions to Answer Before Continuing

- What is the name of the build output folder?
- Which `npm` script triggers the production build?
- Is there a `.gitignore` file? Does it exclude the build folder?

---

**Previous:** [00 – Overview](00-overview.md)  
**Next:** [Step 02 – Set Up Your Terraform Project Structure](02-terraform-project-structure.md)
