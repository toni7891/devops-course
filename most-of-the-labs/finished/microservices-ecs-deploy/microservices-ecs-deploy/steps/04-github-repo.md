# Step 04 — Prepare the GitHub repo

**Goal:** get your code into a standalone GitHub repo and wire up the one piece
of configuration the OIDC pipeline needs — the deploy role ARN, stored as a
repo **variable** (not a secret).

---

## A. Create the repo and publish it from VS Code

Your lab folder should already hold both `*-service/` folders (with the
`Dockerfile`s you wrote), your `docker-compose.yml`, and `.gitignore` at its
root. You'll turn that folder into a Git repo and push it to GitHub **entirely
from the VS Code UI** — no `git` or `gh` commands needed.

1. **Open the lab folder in VS Code** (`File → Open Folder…`) so it's the root
   of your workspace.

2. **Initialize the repo.** Open the **Source Control** view (the branch icon in
   the activity bar, or `Ctrl+Shift+G`). Click **Initialize Repository**. VS Code
   creates the `.git` folder and lists every file as a pending change.

3. **Sanity-check what's staged.** In the **Changes** list, confirm you do **not**
   see `.venv/`, `__pycache__/`, or `.pytest_cache/`. If you do, your
   `.gitignore` isn't being picked up — fix it before committing. Only your
   source, `Dockerfile`s, `docker-compose.yml`, and `.gitignore` should appear.

4. **Make the first commit.** Type a message like
   `feat: initial microservices-ecs-deploy` in the box at the top, then click the
   **✓ Commit** button. When VS Code asks to stage all changes, accept.

5. **Publish to GitHub.** Click **Publish Branch** (it replaces the commit
   button after your first commit). VS Code prompts you to sign in to GitHub the
   first time, then asks for a repo name and **public vs. private** — choose
   **private** and confirm. VS Code creates the GitHub repo and pushes `main` for
   you in one step.

> **Why publish from VS Code?** The built-in GitHub integration creates the
> remote repo *and* pushes your branch in a single action, so you skip
> `gh repo create`, setting the remote, and the first `git push` by hand. After
> this, the **Sync Changes** button push/pulls for you.

> Confirm in the Source Control view that the working tree is clean (no pending
> changes) after publishing — that means everything committed and pushed.

---

## B. Set up keyless AWS auth (OIDC) — you build this yourself

Nothing is handed to you here. You create the AWS-side trust **from scratch in
the AWS Console** so GitHub Actions can deploy without any stored access keys.
The pipeline authenticates using **GitHub OIDC**: GitHub issues a short-lived
identity token, AWS verifies it against a trust policy you define, and hands back
temporary credentials. Nothing long-lived is ever stored in GitHub.

You'll do this in three parts, all in the **AWS Management Console**. Sign in,
and confirm the **Region** selector (top-right) shows the region you'll use for
the whole lab (e.g. `eu-west-1`) — IAM is global, but staying consistent avoids
confusion in later steps.

### B.1 — Register GitHub as an OIDC identity provider

This tells your AWS account to trust identity tokens issued by GitHub Actions.
It's a one-time, account-wide registration.

1. Open the **IAM** console → in the left navigation, choose **Identity
   providers**.
2. Choose **Add provider**.
3. Under **Provider type**, select **OpenID Connect**.
4. In **Provider URL**, enter:
   ```
   https://token.actions.githubusercontent.com
   ```
   Then choose **Get thumbprint**. (AWS retrieves and trusts GitHub's CA
   automatically; the button confirms the endpoint is reachable.)
5. In **Audience**, enter:
   ```
   sts.amazonaws.com
   ```
6. Choose **Add provider**.

> You now have a provider listed as `token.actions.githubusercontent.com`. This
> only says "trust tokens GitHub signs" — it does **not** yet say *which* repo
> may act. That scoping happens in the role's trust policy next.

### B.2 — Create the deploy role for GitHub Actions

1. In the **IAM** console, choose **Roles** → **Create role**.
2. For **Trusted entity type**, select **Web identity**.
3. Under **Web identity**:
   - **Identity provider:** choose `token.actions.githubusercontent.com`
     (the one you created in B.1).
   - **Audience:** choose `sts.amazonaws.com`.
   - **GitHub organization:** enter your GitHub username or org
     (e.g. `<your-username>`).
   - **GitHub repository** *(optional field, but set it):* `microservices-ecs-deploy`
   - **GitHub branch** *(optional field, but set it):* `main`

   > Filling in the org/repo/branch fields makes the console generate a trust
   > policy already scoped to your repo and `main`. If you leave them blank, the
   > policy trusts your **whole org** — you'd then have to tighten it by hand in
   > step 6 below.
4. Choose **Next** to go to the **Add permissions** screen. Search for and
   select the check boxes next to both managed policies:
   - **`AmazonEC2ContainerRegistryPowerUser`** — lets the pipeline push images to ECR
   - **`AmazonECS_FullAccess`** — lets it register task definitions and update services

   > These are intentionally broad so the lab's deploy "just works." In a real
   > account you'd replace them with a least-privilege policy. The ECS-managed
   > policy already allows the `iam:PassRole` the deploy needs to pass
   > `ecsTaskExecutionRole`.
5. Choose **Next**. Set **Role name** to `github-actions-deploy`, then choose
   **Create role**.
6. **Verify the trust policy.** Open the new role → **Trust relationships** tab →
   **Edit trust policy**. The full document should look like this — substitute
   your account ID and GitHub username:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
           },
           "StringLike": {
             "token.actions.githubusercontent.com:sub": "repo:<your-username>/microservices-ecs-deploy:ref:refs/heads/main"
           }
         }
       }
     ]
   }
   ```
   Confirm the `Principal.Federated` ARN points at the provider you created in
   B.1, and that the `sub` value pins **your repo** *and* the `main` branch. If
   it's missing or set to something broad like `repo:<your-org>/*`, fix it and
   choose **Update policy**.

   > The console sometimes lists the `sub` value **twice** inside an array (once
   > for the org, once for the repo). That's harmless — it's an OR list, so a
   > duplicate matches the same thing — but you can collapse it to the single
   > string above to keep it clean.
7. **Copy the _role_ ARN** (you need it in B.3). Go to the role's **Summary**
   page — the **ARN** at the top contains **`:role/`**:
   ```
   arn:aws:iam::<ACCOUNT_ID>:role/github-actions-deploy
   ```

   > **Copy the role ARN, NOT the provider ARN.** The trust policy you just looked
   > at in step 6 contains a *different* ARN with **`:oidc-provider/`** in it
   > (`arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com`).
   > That is the identity provider, **not** the role. If you store the
   > `oidc-provider/...` ARN in B.3, `role-to-assume` can't assume it — STS
   > rejects it, the deploy step prints **"Assuming role with OIDC"** over and over
   > and then fails. The value you want has **`:role/`** in it.

> **Why scope the `sub`?** Without the `StringLike` on `sub`, *any* GitHub repo
> that can reach AWS could assume your role. The condition pins it to your repo
> **and** the `main` branch, so only your deploy workflow can authenticate.

### B.3 — Store the role ARN as a GitHub repo variable

The role ARN is **not a secret** — it's just an identifier — so store it as a
repo **variable**.

1. In your GitHub repository, go to **Settings** → in the left sidebar,
   **Secrets and variables** → **Actions**.
2. Select the **Variables** tab → **New repository variable**.
3. **Name:** `AWS_DEPLOY_ROLE_ARN`
4. **Value:** the **role** ARN from B.2 step 7 — it must contain **`:role/`**
   (e.g. `arn:aws:iam::050752632489:role/github-actions-deploy`). If it contains
   `:oidc-provider/`, you copied the wrong ARN — go back to B.2 step 7.
5. Choose **Add variable**.

> If you store it as a *secret* instead, `vars.AWS_DEPLOY_ROLE_ARN` in the
> workflow resolves empty and the credentials step fails. Use a **variable**.

*Self-check questions:*
- Why is a role ARN safe to store as a *variable* and not a secret?
- What does OIDC give you that a stored `AWS_ACCESS_KEY_ID` / `SECRET` pair
  does not?
- What exactly does the `sub` condition stop someone else from doing?

---

## What you learned

- OIDC replaces long-lived AWS access keys with short-lived, per-run tokens —
  nothing secret-shaped ever lives in GitHub. You registered GitHub as an
  identity provider, created a deploy role scoped by trust policy to your repo
  and branch, and stored its ARN as a plain repo variable.

## Checklist

- [ ] A standalone GitHub repo exists with the lab contents at its root
- [ ] No `.venv/`, `__pycache__/`, or `.pytest_cache/` committed
- [ ] GitHub is registered as an **OIDC identity provider** in IAM
- [ ] A deploy role exists whose trust policy `sub` pins your repo **and** `main`
- [ ] **No AWS access keys** stored as GitHub secrets — OIDC only
- [ ] `AWS_DEPLOY_ROLE_ARN` is set as a repo **variable**

## Next

→ [Step 05 — Provision the AWS infrastructure](05-provision-aws-infra.md)
