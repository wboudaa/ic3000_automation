# Scorecard Still Not Changed – Force a Refresh

Your repo **main** already has SECURITY.md, dependabot, CodeQL, and CI workflows. If the score still shows old results, do the following.

---

## 1. Run Scorecard from GitHub (updates public score)

This sends the latest score to the OpenSSF API so the viewer and DevNet can see it.

1. Open: **https://github.com/wboudaa/ic3000_automation/actions**
2. In the left sidebar, click **"OpenSSF Scorecard"**.
3. Click **"Run workflow"** (right side) → **"Run workflow"** again.
4. Wait until the run is **green** (about 2–5 minutes).
5. After 5–10 minutes, check:
   - **https://securityscorecards.dev/viewer/?uri=github.com/wboudaa/ic3000_automation**

If the run is **red**, open the run, click the **Scorecard** job, and read the error (e.g. permissions or API). Fix that and run again.

---

## 2. DevNet Code Exchange report

The **Cisco DevNet report** may use a cached score or run Scorecard on their own schedule.

- **Re-submit** the project:  
  https://developer.cisco.com/codeexchange/github/submit  
  Use the same repo URL so they re-evaluate.
- Or use **Report / Edit** and see if there is a “Refresh” or “Re-run” option:  
  https://developer.cisco.com/codeexchange/github/repo/wboudaa/ic3000_automation/report/

If the report still shows the old score after 24–48 hours, contact DevNet support and ask them to refresh the security score for the repo.

---

## 3. See the score locally (optional)

To see what Scorecard reports **right now** for your repo (without waiting for the viewer):

```bash
# Needs a GitHub token with public repo read (no special permissions)
export GITHUB_AUTH_TOKEN=ghp_xxxx

docker run -e GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN \
  gcr.io/openssf/scorecard:latest \
  --repo=github.com/wboudaa/ic3000_automation
```

Create a token at: https://github.com/settings/tokens (scope: `public_repo` or no scopes for public repos).

---

## 4. If some checks are still 0

| Check                | What to do |
|----------------------|------------|
| **Branch-Protection** | Scorecard may need an admin token to see it. Ensure in GitHub: Settings → Branches → rule for `main` with “Require a pull request” and “Require status checks”. |
| **CI-Tests**         | Scorecard only counts **merged PRs** that had CI. Merge at least one PR that ran “CI Tests - Repository Check” (or similar). |
| **Security-Policy**  | Must have **SECURITY.md** in repo root on **main**. Confirm: https://github.com/wboudaa/ic3000_automation/blob/main/SECURITY.md |
| **SAST**             | Must have **CodeQL** (or similar) workflow on **main**. Confirm: https://github.com/wboudaa/ic3000_automation/tree/main/.github/workflows |
| **Dependency-Update-Tool** | Must have **.github/dependabot.yml** on **main**. Confirm: https://github.com/wboudaa/ic3000_automation/blob/main/.github/dependabot.yml |

---

**Summary:** Run the **OpenSSF Scorecard** workflow manually from the Actions tab, wait for it to succeed, then re-check the viewer and DevNet report. If DevNet still shows the old score, re-submit or contact DevNet to refresh.
