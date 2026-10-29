# Fail-closed GitHub Pages release process

**Prepared:** October 28, 2026 · **Scope:** Public-only static Open Biomedical Resource Center

## Summary

The existing GitHub Pages configuration publishes directly from `main`. In that mode, GitHub's automated Pages build runs independently of the repository's `Validate public directory` workflow: a failing check **does not prevent** the old branch publisher from releasing the new commit.

The revised `.github/workflows/validate.yml` is designed to **replace** that pattern once the website owner explicitly switches the Pages publishing source to **GitHub Actions**. It keeps the original validation job, creates a strict allowlist-based site artifact with same-site link checks, and places deployment in a separate job with `needs: validate`. If any test fails, the deployment job cannot run.

**Important:** This is **prepared, not yet activated**. Until GitHub Pages Source is changed in repository settings, direct branch publishing continues. Do not report that release gating has been fully enforced before verifying the settings and a deployed run.

## What is checked?

1. Resource catalog schema, IDs, URL shapes and review dates.
2. Human-readable catalog and agent-discovery endpoint consistency.
3. Site source links, story files, tool routes and the safety wording in public contribution pages.
4. JavaScript syntax for the resource directory, lab, story and guide.
5. Absence of designated patient-data directories.
6. **New:** `python3 scripts/prepare_pages.py` creates `dist/` from **only** approved site HTML, CSS, JavaScript, public JSON, XML and `.nojekyll`.
7. **New:** Check that every local asset/page link in the published HTML has a target in that artifact; check static HTML fragment anchors, including links between nested story pages.
8. **New:** Prevent paths that escape the public site and symbolic links in the asset manifest.

We deliberately exclude GitHub Actions files, internal documentation, issue templates, Python scripts, local config, and other repo files from the new Pages artifact. The repository is publicly accessible independently of the site, so **do not put secrets or patient records in the repository at all**.

## One-time activation by repository owner (required)

The current GitHub connector cannot change the repository's Pages Source or configure GitHub repository variables. The following is an intentional owner-controlled activation; do not attempt to simulate it with a filename or a commit.

1. Open [repository settings](https://github.com/davidwpace/open-biomedical-resource-center/settings).
2. Choose **Secrets and variables → Actions → Variables → New repository variable**. Name: `PAGES_ACTIONS_READY` (exact capitalization); value: `true`.
3. Choose **Pages → Build and deployment → Source: GitHub Actions**. This discontinues publication from the `main` branch source.
4. Go to **Actions → Validate public directory → Run workflow** on the `main` branch. It will run all checks, upload the approved artifact, then deploy it to `github-pages`.
5. Confirm both **Catalog & syntax checks** and **Deploy approved site** succeed. Open the homepage, `start.html`, `stories.html`, `contribute.html`, `catalog.html`, and `data/resources.json`; check a source link from a phone.
6. In the **github-pages** environment settings, restrict deployment to `main` if not already protected.

**Until step 5 is verified, treat the switchover as incomplete.** To roll back, set `PAGES_ACTIONS_READY` to `false` and restore **Pages → Deploy from a branch → main → /(root)**. Verify that the old branch publisher deploys successfully after rollback.

## Future release discipline

- Work on feature branches, open a pull request, and require a passing **Catalog & syntax checks** status before merging.
- GitHub reports the `main` branch is currently **unprotected**, so an admin should set branch rules requiring PRs and the exact check name; do this carefully, as an incorrectly specified required check can block merges.
- The new workflow supports `workflow_dispatch` for a controlled redeployment of the current verified `main` revision.
- It uses minimal default permissions: validation has `contents:read`; deployment has `pages:write` and `id-token:write` only in that job.
- Jobs are linked by `needs: validate`, and deployment is suppressed entirely when the readiness variable is not `true` or the event is a pull request.
- Prefer full commit-SHA pinning for actions in a later security update after auditing their official releases.
- Browser rendering, keyboard navigation and real-device testing still require a separate smoke test; static checks are valuable but not equivalent.

## Negative test (do not do this on the production branch)

Use a temporary feature branch to intentionally introduce a missing internal link or invalid `data/resources.json` record, then open a draft PR. The validation must fail. With Pages Source configured for Actions, such a failing PR cannot be deployed; the protected `main` rule should prevent merging until corrected.

## Official documentation

- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments

**Safeguard:** No backend, license change, patient-data intake, public health claims or additional commercial service is introduced by this update.
