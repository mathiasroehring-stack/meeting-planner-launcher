# Meeting Planner Launcher

Open the **[live app](https://mathiasroehring-stack.github.io/meeting-planner-launcher/)** to type any location, resolve its timezone, and launch [timeanddate.com Meeting Planner](https://www.timeanddate.com/worldclock/meeting.html) with your city and theirs pre-filled.

## Fix 404 — enable GitHub Pages (required once)

A 404 means Pages is **not turned on** for this repo yet. The code is already on `main`; you only need to flip the switch:

1. Open **[Settings → Pages](https://github.com/mathiasroehring-stack/meeting-planner-launcher/settings/pages)** (you must be signed in as `mathiasroehring-stack`).
2. Under **Build and deployment → Source**, pick **Deploy from a branch** (not “GitHub Actions” unless you also approve the `github-pages` environment).
3. Set **Branch:** `main` and **Folder:** `/ (root)`.
4. Click **Save**.
5. Wait 1–2 minutes, then open: **https://mathiasroehring-stack.github.io/meeting-planner-launcher/**

You should see a green banner on that settings page saying “Your site is live at …” once it works.

### If you prefer `/docs` instead of root

Use **Folder:** `/docs` — the same files are duplicated there.

### If you prefer GitHub Actions

1. On the Pages settings page, set Source to **GitHub Actions**.
2. Go to **[Actions](https://github.com/mathiasroehring-stack/meeting-planner-launcher/actions)** → open the latest **Deploy GitHub Pages** run.
3. If it asks to approve the **`github-pages`** environment, click **Review deployments** → **Approve**.
4. Re-run the workflow if needed (**Run workflow** on the workflow page).

## Local development

From the main project (Vite app), open `http://127.0.0.1:3022/meeting-planner.html` after `npm run dev`.
