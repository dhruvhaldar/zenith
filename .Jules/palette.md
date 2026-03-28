## 2024-05-24 - HTML Structural Semantics & Keyboard A11y
**Learning:** Adding a `<main>` tag around the primary content instantly improves screen reader navigation and provides semantic structure, which is crucial for accessibility. Furthermore, defining robust `:focus-visible` styles on interactive elements like links ensures keyboard users have clear visual feedback without compromising mouse user experience.
**Action:** When reviewing simple HTML templates, prioritize wrapping core content in semantic landmarks (like `<main>`) and verifying that focus states are distinct and visible against the background.

## 2026-03-25 - External Links & Target Blank Navigation Context
**Learning:** API demo links that return raw JSON payloads break the user's flow and context if they navigate in the same tab, forcing them to use the back button. Adding `target="_blank"` solves this, but for accessibility and clarity, it must be accompanied by an indicator (e.g., "↗") and screen-reader only text (e.g., "(opens in a new tab)") so all users are informed of the behavior change.
**Action:** Whenever introducing links to raw API endpoints or external resources in documentation pages, ensure they open in a new tab and explicitly indicate this behavior to screen readers. If strict styling rules forbid custom CSS (like `.sr-only`), use the native `aria-label` attribute on the `<a>` element to provide this context seamlessly.

## 2026-03-27 - Linking Tooltips to ARIA Labels for Sighted Users
**Learning:** While `aria-label` effectively provides context to screen reader users about links opening in a new tab (e.g., "(opens in a new tab)"), mouse and keyboard-sighted users may not intuitively understand icon-only indicators like "↗". Adding a native `title="Opens in a new tab"` attribute to the link ensures all users, regardless of assistive technology, receive the same clarifying context on hover or focus without introducing new UI elements.
**Action:** Whenever using icon-only indicators for external links with `aria-label` for screen readers, pair them with a `title` attribute so sighted users also benefit from the explanation seamlessly.

## 2026-03-28 - Semantic Landmarks for List-like Content Blocks
**Learning:** Generic list-like content blocks (e.g., repeating groups of images, titles, and descriptions) built with `<div>` are largely invisible structurally to screen reader users, who must wade through them sequentially. By converting these `<div>` wrappers into `<section>` elements and explicitly labeling them with `aria-labelledby` referencing their internal headings, we transform arbitrary blocks into discoverable and navigable landmark regions.
**Action:** When creating repeating blocks of complex content (like article previews, artifact displays, or cards) that have internal headings, use `<section>` instead of `<div>` and tie the heading to the section via `aria-labelledby`.
