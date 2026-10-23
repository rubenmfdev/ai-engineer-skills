# Manifest notes

- `permissions`: API access (`storage`, `alarms`, `tabs`, `scripting`, `sidePanel`, `declarativeNetRequest`). Requested at install.
- `host_permissions`: Site access for `fetch`, `scripting` and cookies. Prefer narrow patterns.
- `optional_permissions` / `optional_host_permissions`: Requested at runtime with `chrome.permissions.request` from a user gesture. Use these for non-core features.
- `activeTab`: Temporary access to the current tab after a user gesture (click on the action, shortcut). Often replaces broad host access.
- `web_accessible_resources`: Files a web page may load. Restrict `matches` tightly.
- `content_security_policy.extension_pages`: Default `script-src 'self'; object-src 'self'` is the strictest allowed. Do not loosen.
- `commands`: Keyboard shortcuts. Users can rebind them at `chrome://extensions/shortcuts`.
- `side_panel.default_path`: Side panel page, requires the `sidePanel` permission.
- `minimum_chrome_version`: Set it when you rely on newer APIs.
- `key`: Pin a stable extension ID in development.
