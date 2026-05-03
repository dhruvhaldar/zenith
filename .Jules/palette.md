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

## 2026-04-09 - Intra-Page Links and Target Element Focus
**Learning:** Adding smooth scrolling (via `@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }`) provides crucial spatial context when using intra-page links (like a Table of Contents). However, clicking an anchor link only visually scrolls the page; it does not automatically move screen reader or keyboard focus to the target element if that element (like a `<body>` or `<h2>`) is not natively focusable. This leaves keyboard users stranded at the top of the page while visually they are at the bottom.
**Action:** When implementing intra-page navigation (e.g., `<a href="#target">`), always add `tabindex="-1"` to the target element (e.g., `<h2 id="target" tabindex="-1">`) so that focus is correctly transferred without adding the element to the normal tab order. Additionally, remove the outline for these programmatically focused elements (via `[tabindex="-1"]:focus { outline: none; }`) to maintain a clean visual appearance for mouse users.

## 2026-04-10 - Skip to Content Links
**Learning:** For keyboard and screen reader users, navigating past repeated header and navigation elements on every page reload is tedious. Adding a "Skip to main content" link at the very top of the document provides a direct mechanism to bypass this. When operating within strict classless constraints, these can be effectively hidden visually (but kept accessible) using attribute selectors like `a[href="#main-content"]` combined with `position: absolute; left: -9999px;` and revealed on focus with `:focus-visible`.
**Action:** Always implement a skip-to-content link as the very first interactive element in the `<body>` on any page with a header/navigation, and ensure the target `<main>` element has `tabindex="-1"` so it properly receives focus when the link is activated.

## 2026-04-12 - Semantic Image Captions with Figure and Figcaption
**Learning:** Using generic `<p>` tags below an `<img>` tag to provide a caption leaves the description semantically detached from the image for assistive technologies. Wrapping both elements in `<figure>` and `<figcaption>` natively groups them, ensuring screen readers and other assistive tools announce the image and its caption together as a unified piece of content.
**Action:** When displaying artifacts, diagrams, or meaningful images accompanied by descriptive text, always encapsulate them within `<figure>` and `<figcaption>` tags instead of relying on loose proximity with `<p>` tags.

## 2026-04-13 - Target Highlight Animations for Intra-Page Navigation
**Learning:** Even with smooth scrolling and proper focus management, jumping to an intra-page link (like a Table of Contents entry) can leave users momentarily disoriented, particularly on text-heavy pages or if the target is near the bottom and doesn't align to the top edge. Providing a brief, non-intrusive background flash on the destination element helps the eye immediately locate the new point of interest.
**Action:** When implementing intra-page navigation, utilize the `:target` CSS pseudo-class paired with a subtle, fading background-color `@keyframes` animation. This enhances spatial context and cognitive ease without requiring JavaScript.

## 2026-04-14 - Target Highlights and Body Elements
**Learning:** Indiscriminately styling the `:target` pseudo-class can cause massive visual disruption (like full-screen flashing) if the target of an intra-page link (like a 'Back to top' link) is the document `body` or `html`.
**Action:** Always restrict `:target` styling using `:not(body)` or specifically target semantic content elements to avoid jarring UX.

## 2026-04-14 - Skip Link Layout Shifts
**Learning:** Revealing hidden accessibility links (like skip-to-content) by switching them from `position: absolute` to `position: static` on focus causes undesirable layout shifts, abruptly pushing the rest of the page down.
**Action:** Keep hidden accessibility links `position: absolute` when focused, instead adjusting `top`/`left` properties and adding background/padding to display them as a clean overlay.

## 2026-04-15 - Orphaned External Link Icons on Mobile
**Learning:** Using regular spaces between link text and external link indicator icons (like `↗`) can lead to the icon dangerously wrapping to a new line by itself on constrained mobile viewports. This creates an awkward "orphaned" visual artifact that breaks the connection between the icon and the text.
**Action:** When appending indicator icons to text elements, particularly external link indicators, use a non-breaking space (`&nbsp;`) instead of a regular space (e.g., `Link Text&nbsp;<span aria-hidden="true">↗</span>`). This binds the icon to the last word, ensuring they wrap together as a unified block and maintain visual polish across all device widths.

## 2026-04-21 - Explicit API Endpoint Documentation
**Learning:** Providing interactive API demo links is helpful, but if users have to hover over or click the link to discover the actual endpoint URL and HTTP method, it slows down developer exploration. Displaying the endpoint structure and HTTP method (e.g., `GET /api/...`) explicitly in text or `<code>` blocks on the UI provides immediate, transparent documentation, significantly improving the developer experience.
**Action:** When providing interactive API demo links, always explicitly display the endpoint structure and HTTP method directly on the UI using `<code>` blocks to improve developer experience and transparency.

## 2026-04-24 - Screen Reader Auditory Clutter from Non-Semantic Separators
**Learning:** To prevent auditory clutter for screen reader users, always wrap non-semantic text characters used purely for visual separation (like `|`, `•`, or `-` in footers or breadcrumbs) in an inline element (like `<span>`) with `aria-hidden="true"`. This hides the separator from assistive technologies while allowing custom CSS spacing and styling.
**Action:** When adding text-based visual separators between links or items, always wrap them in `<span aria-hidden="true">` to keep the screen reader experience clean.

## 2026-04-30 - One-Click Select for API Endpoints
**Learning:** Forcing developers to manually highlight and drag to select API endpoints from documentation is a tedious micro-friction. By wrapping the endpoint path in a span styled with `user-select: all; -webkit-user-select: all; cursor: copy;` and providing a tooltip like `title="Click to select"`, users can instantly copy the entire path with a single click.
**Action:** When displaying literal API endpoints or code snippets intended for copying in documentation, apply `user-select: all` to provide a frictionless copy interaction without relying on custom JavaScript clipboards.

## 2026-04-30 - Machine Translation of Code Snippets
**Learning:** Browser-level machine translation (like Google Translate) aggressively translates text within `<code>` blocks, which can destructively alter technical HTTP methods (e.g., translating "GET" to "OBTENER") or literal endpoint paths, rendering the documentation unusable for non-native readers relying on translation tools.
**Action:** Always add the standard HTML `translate="no"` attribute to `<code>` tags (or other literal technical blocks) to protect them from destructive auto-translation and maintain their utility across all localizations.

## 2026-05-01 - Interactive Hover States for Copyable Elements
**Learning:** Inline `user-select: all` lacks interactive feedback (hover/focus states), making it less discoverable as a clickable element, and that animations triggered by `:target` should respect `prefers-reduced-motion`.
**Action:** Extract these to CSS classes to enable interactive states and always wrap animations in reduced-motion media queries.

## 2026-05-02 - Keyboard Shortcut Hints for Copyable Elements
**Learning:** While `user-select: all` makes copying text easier by selecting everything with one click, its functionality isn't always immediately obvious to users. Adding explicit, visual keyboard shortcut hints using `<kbd>` tags provides clear instruction and improves discoverability of this micro-interaction.
**Action:** When implementing one-click copyable text (via `user-select: all`), accompany it with brief instructional text utilizing styled `<kbd>` tags (e.g., `<kbd>Ctrl</kbd> + <kbd>C</kbd>`) to guide the user on how to complete the action.

## 2026-05-15 - Decorative Emojis and Screen Readers
**Learning:** Sprinkling standalone emojis (like 💡, ✨, or 🚀) as visual decorations or icons can create annoying auditory clutter for screen reader users, as the screen reader will literally read out the emoji name (e.g., "light bulb tip:").
**Action:** Always wrap decorative emojis used in a purely visual context inside a `<span aria-hidden="true">` to preserve visual delight without degrading the auditory experience.
