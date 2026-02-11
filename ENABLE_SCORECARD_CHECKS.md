# Fix OpenSSF Scorecard (DevNet Security Score)

Scorecard only looks at the **default branch** of your GitHub repo. If your local `main` was never pushed to GitHub, or the default branch on GitHub is different, you get zeros. Follow these steps in order.

**Quick path:** A branch `scorecard-fixes` with all needed files has been pushed. **Merge this PR** so that `main` gets SECURITY.md, dependabot, CodeQL, and CI workflows, then do Step 2 (and Step 3 if CI-Tests is still -1):
→ **https://github.com/wboudaa/ic3000_automation/pull/new/scorecard-fixes**

---

## Step 1: Push everything to GitHub default branch (or merge the PR above)

1. **Check GitHub default branch**
   - Open: https://github.com/wboudaa/ic3000_automation
   - Click **Settings** → **General** → scroll to **Default branch**
   - Note the name (usually `main` or `master`)

2. **Push this repo to that branch**
   ```bash
   cd /path/to/ic3000_automation   # or ic3000-toolkit
   git status
   git add .
   git commit -m "chore: add SECURITY.md, dependabot, CodeQL, CI workflows for Scorecard"
   git push github main
   ```
   If GitHub default branch is `master` instead of `main`:
   ```bash
   git push github main:master
   ```
   Or set GitHub default to `main`: Settings → Default branch → switch to `main` → Update.

3. **Confirm these exist on the default branch on GitHub**
   - Root: `SECURITY.md`, `requirements.txt`, `LICENSE`
   - `.github/dependabot.yml`
   - `.github/workflows/codeql-analysis.yml`
   - `.github/workflows/python-tests.yml` (or `status-check.yml` with "test" in name)

---

## Step 2: Enable branch protection (Branch-Protection: 0 → 10)

**You must do this in the GitHub UI.** No file in the repo can enable it.

1. Go to: https://github.com/wboudaa/ic3000_automation/settings/branches
2. Click **Add branch protection rule** (or **Add rule**)
3. **Branch name pattern:** `main` (or `master` if that’s your default)
4. Enable:
   - **Require a pull request before merging** → set **1** approval
   - **Require status checks to pass before merging** → select **CI Tests - Repository Check** (or your CI workflow)
   - **Do not allow bypassing the above settings**
5. Click **Create** (or **Save**)

After this, Scorecard should give **Branch-Protection** a non-zero score (often 6–10 depending on options).

---

## Step 3: Get CI-Tests to pass (CI-Tests: -1 → 10)

Scorecard looks at **recent commits** and only gives points if it sees **CI runs on a pull request**. Direct pushes don’t count.

1. **Create a branch and open a PR**
   ```bash
   git checkout -b chore/scorecard-ci
   git push github chore/scorecard-ci
   ```
   Then on GitHub: **Compare & pull request** into `main`.

2. **Wait for CI** (Actions tab) to finish and turn green.

3. **Merge the PR** (Merge pull request).

4. After a few minutes, run Scorecard again or wait for the next run. It should see a merged PR with CI and give **CI-Tests** a positive score.

---

## Step 4: Security-Policy and SAST

- **Security-Policy (0):** Scorecard looks for **SECURITY.md in the root of the default branch**. After Step 1, it should be detected. If it still says "not detected", confirm in the repo root on GitHub: https://github.com/wboudaa/ic3000_automation/blob/main/SECURITY.md (or `.../master/...`).
- **SAST (0):** It looks for **CodeQL** (or similar) on the default branch. After Step 1, `codeql-analysis.yml` on the default branch should be enough. If still 0, trigger the CodeQL workflow once (e.g. push a small commit or run the workflow manually from the Actions tab).

---

## Step 5: Dependency-Update-Tool (0)

Scorecard looks for **.github/dependabot.yml** on the default branch. After Step 1 it should be there. Confirm: https://github.com/wboudaa/ic3000_automation/blob/main/.github/dependabot.yml

---

## Quick checklist

| Check                | Fix                                                                 |
|----------------------|---------------------------------------------------------------------|
| Branch-Protection    | Enable in GitHub: Settings → Branches → Add rule for `main`        |
| CI-Tests             | Merge at least one PR that ran CI (Steps 1 + 3)                    |
| Security-Policy      | SECURITY.md in repo root on **default branch** (Step 1)              |
| SAST                 | codeql-analysis.yml on **default branch** + run once (Step 1)      |
| Dependency-Update-Tool | .github/dependabot.yml on **default branch** (Step 1)            |

---

## Re-run Scorecard

- Public viewer: https://securityscorecards.dev/viewer/?uri=github.com/wboudaa/ic3000_automation  
- DevNet report (login): https://developer.cisco.com/codeexchange/github/repo/wboudaa/ic3000_automation/report/

Scorecard may cache; wait a bit or trigger a new run (e.g. push a commit or use the Scorecard workflow if you have it).
