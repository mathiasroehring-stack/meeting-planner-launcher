# Meeting Planner Launcher

Open the **[live app](https://mathiasroehring-stack.github.io/meeting-planner-launcher/)** to type any location, resolve its timezone, and launch [timeanddate.com Meeting Planner](https://www.timeanddate.com/worldclock/meeting.html) with your city and theirs pre-filled.

## Enable GitHub Pages (one-time)

If the live link returns 404:

1. Open [Repository Settings → Pages](https://github.com/mathiasroehring-stack/meeting-planner-launcher/settings/pages)
2. Under **Build and deployment → Source**, choose **Deploy from a branch**
3. **Branch:** `main` · **Folder:** `/docs`
4. Click **Save**

The site will be live at:

**https://mathiasroehring-stack.github.io/meeting-planner-launcher/**

Alternatively, set Source to **GitHub Actions** to use the automated workflow in `.github/workflows/deploy-pages.yml`.
