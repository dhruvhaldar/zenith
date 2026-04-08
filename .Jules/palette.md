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

## 2026-03-29 - Domain-Specific Abbreviations in ARIA Labels
**Learning:** Technical abbreviations (like "SNR", "Mag", "Mpc") within link text or standard aria-labels are often mispronounced or spelled out letter-by-letter by screen readers, stripping the user of the intended context. Providing full, natural-language expansions in the `aria-label` attribute bridges this gap and ensures that domain-specific terminology is accessible to all.
**Action:** When encountering domain-specific abbreviations in UI text, override the screen reader pronunciation by providing the expanded, natural-language version (e.g., "Signal-to-Noise Ratio" instead of "SNR") in the element's `aria-label`.

## 2026-04-01 - Link Color Contrast & Default Underlines (WCAG 1.4.1)
**Learning:** Using only color (like `#0056b3`) to distinguish links from surrounding text (`#000000`) fails WCAG 1.4.1 (Use of Color) if the contrast ratio between the link and the text is less than 3:1. Because this specific color combination fails that ratio, the links must have an additional visual cue, such as a default underline, to ensure they are perceivable to users with color vision deficiencies.
**Action:** Always ensure inline links have an underline by default unless the link color achieves at least a 3:1 contrast ratio with the surrounding body text AND has a distinct focus/hover state. Utilizing `text-decoration-thickness` and `text-underline-offset` allows for an aesthetically pleasing default underline.## 2026-04-02 - Abbreviation Tooltips and Screen Reader Pronunciation in Alt Text
**Learning:** Sighted users often miss tooltips on abbreviations if there isn't a visual indicator like a dotted underline. Furthermore, domain-specific abbreviations in image `alt` text are frequently mispronounced by screen readers (e.g., 'SNR' read as 'snurr').
**Action:** Always add a visual cue for abbreviations (e.g., `abbr[title] { text-decoration: underline dotted; cursor: help; }`) and explicitly expand abbreviations into full words when writing `alt` text for images to ensure consistent accessibility for both sighted and screen-reader users.

## 2026-04-07 - Abbreviation Tooltips Keyboard Accessibility
**Learning:** Native `<abbr title="...">` elements provide helpful tooltips for mouse users on hover, but they are completely invisible to keyboard-only users who navigate via the Tab key, creating a hidden accessibility barrier. Adding a simple `tabindex="0"` along with clear `:focus-visible` outline styles ensures these elements enter the tab order and their titles become accessible.
**Action:** When using standalone `<abbr>` tags to provide acronym definitions outside of already-focusable elements (like links), always include `tabindex="0"` and define `:focus-visible` styling so keyboard users can access the tooltips.
## 2026-04-08 - Native Intra-page Navigation
**Learning:** Using native HTML `<nav>` and in-page anchor links provides highly accessible semantic landmarks and "skip-to" navigation for screen-reader/keyboard users, entirely without custom CSS dependency or javascript.
**Action:** Always implement semantic intra-page links (Table of Contents and Back to Top) on long static pages to immediately improve keyboard and screen-reader accessibility.
