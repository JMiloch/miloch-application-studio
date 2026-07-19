# Changelog

All notable releases of Miloch Application Studio.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: `2.<yy>.<m>.<dd>` — every build self-documents its release date.

---

## [2.26.7.18] — 2026-07-19

**First public release of MAS 2.0.**

### The pivot

MAS 2.0 is a full re-launch as closed-source freeware for the single-machine packager. Every paid-tier feature from the pre-Sunset roadmap (Single / Site licences, headless AutoMode service, EV-cert procurement, sales funnel) stays retired. What ships here is the single-machine tool refined to release quality: everyone gets the full version, no licence key, no trial, no cloud.

The full timeline from wrapper (2018) through the WinUI attempt (2025 – 2026), the sunset (June 2026), and the July 2026 pivot lives at [miloch.dev/mas/roadmap](https://miloch.dev/mas/roadmap/).

### Added

- Full Capture → Build → Pre-Ship → Rollout pipeline in one WinUI 3 desktop app.
- **Ship queue** — atomic, resumable, audit-tracked delivery to SCCM (ConfigurationManager module) or Intune (Microsoft Graph).
- **Per-package detection editor** on the Pre-Ship page — six modes (Profile default / MSI ProductCode / PSADT-Inventory / Registry / File / Custom script).
- **Intune auto-assignments** — pre-defined AAD groups + intent from the active profile land automatically after the Win32App is created.
- **MAS Catalog full-text search** on the Capture page's Parameter Library tab — type an app name, get the matching silent switches on the clipboard.
- Single active profile — one profile carries both SCCM site and Intune tenant configuration. Tab enablement in Pre-Ship / Rollout is driven by which platform fields the profile actually has.
- Cancel / Clear-history dialogs on the MAS Premium Body standard.
- Live profile switching — Settings changes take effect without an app restart.

### SCCM

- **Revision minimisation** — every property (Publisher, Version, LocalizedName, Description, IconLocationFile, AppCategory) packs into a single `New-CMApplication` call. Fresh apps now land on **CIVersion = 2** instead of the previous 4.
- Phantom-category injection guard — categories are re-verified after `New-CMCategory`; a silent create-failure no longer poisons the `New-CMApplication` call.
- Atomicity fallback on icon rejection — the retry path detects a half-created app and switches to `Set-CMApplication` update instead of a second `New-CMApplication` that would fail with "name already exists".

### Freeware pivot

- All licensing UI collapsed (Settings → License, activation flow, licence key entry).
- Payment provider integration removed.
- SQL-Server backend hidden behind a feature flag; SQLite (WAL) is the only user-visible database provider.
- AutoMode / watch-folder pipeline archived out of the solution.
- About page — new **Support the project** panel with Ko-fi and GitHub Sponsors, visible but non-intrusive (no popup, no reminder).

### Quality

- Test suite: 316 passing, 0 warnings, 0 errors on build.
- Full independent code review pass with three confirmed fixes applied (dead ternary, phantom-category, PreCheck race guard).
- End-to-end backup taken before the release cut.

### Documentation

- Nine new user-doc chapters written from scratch: Installation, Vocabulary, Your First Package, Workflow Steps, Required Settings, PSADT Template Basics, What the Memory-DB Remembers, GDPR Export, Common Issues.
- Full re-launch of [miloch.dev/mas](https://miloch.dev/mas/) — landing, story, feedback, docs, updates all rebuilt for the freeware line.

---

*Earlier internal builds (MAS 1.x, PowerShell wrapper `M.Packager`) are not published. Their history lives in the story page: [miloch.dev/mas/roadmap](https://miloch.dev/mas/roadmap/).*
