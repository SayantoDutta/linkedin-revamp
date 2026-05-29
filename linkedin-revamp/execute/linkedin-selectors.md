# LinkedIn selectors

Stable references to the LinkedIn UI elements this skill touches. Use these when `find` is too ambiguous or when you need to navigate by URL.

LinkedIn's DOM class names change weekly. Use the natural-language `find` tool first. Use URL paths and ARIA labels as fallbacks. Only use raw CSS selectors as a last resort — they will break.

---

## Direct URLs (most stable)

| Purpose | URL |
|---------|-----|
| Profile (own) | `https://www.linkedin.com/in/{slug}/` |
| Edit intro modal | `https://www.linkedin.com/in/{slug}/edit/intro/` |
| Add About section (new) | `https://www.linkedin.com/in/{slug}/edit/forms/summary/new/` |
| Public profile settings (vanity URL) | `https://www.linkedin.com/public-profile/settings` |
| Profile visibility settings | `https://www.linkedin.com/mypreferences/d/categories/profile-visibility` |
| Notify network settings | `https://www.linkedin.com/mypreferences/d/settings/notify-network-for-updates` |
| Experience details page | `https://www.linkedin.com/in/{slug}/details/experience/` |
| Skills details page | `https://www.linkedin.com/in/{slug}/details/skills/` |
| Featured details page | `https://www.linkedin.com/in/{slug}/details/featured/` |
| Add Featured link | `https://www.linkedin.com/in/{slug}/edit/forms/featured-media/new/?type=link` |
| Contact info modal | `https://www.linkedin.com/in/{slug}/overlay/contact-info/` |
| Add skill flow | `https://www.linkedin.com/in/{slug}/skills/edit/forms/new/` |

---

## Natural-language `find` queries that work

These have been confirmed against LinkedIn's accessibility tree. Use these phrasings when calling `find`.

### Top-of-profile actions
| Query | Returns |
|-------|---------|
| `"Edit pencil button on profile intro card"` | Pencil to open Edit intro modal |
| `"Add background image button on profile banner"` | Camera icon on banner |
| `"Add cover image option in the banner dropdown"` | Submenu item after camera click |
| `"Upload single photo button in cover image modal"` | File picker trigger |

### Edit intro modal
| Query | Returns |
|-------|---------|
| `"Headline text field in edit intro"` | Headline input |
| `"Save button in edit intro modal"` | Save button at modal bottom |
| `"Show current company in my intro checkbox"` | Toggle to disable company chip in header |

### Add about modal
| Query | Returns |
|-------|---------|
| `"About description textarea"` | Main textarea |
| `"Save button in add about modal"` | Save button |

### Edit experience modal
| Query | Returns |
|-------|---------|
| `"Edit pencil button next to {role title} {company} experience"` | Pencil for that entry |
| `"Title field in edit experience modal"` | Title input |
| `"Description textarea in edit experience modal"` | Main description textarea |
| `"Notify network toggle in edit experience modal"` | Toggle inside the modal |
| `"Save button in edit experience modal"` | Save |
| `"Delete option at bottom of edit experience modal"` | Delete option |

### Skill edit modal
| Query | Returns |
|-------|---------|
| `"Edit pencil button next to {skill name} skill"` | Pencil for that skill |
| `"Delete skill button in skill edit modal"` | Delete option |
| `"Delete confirmation button in delete-skill modal"` | Confirm Delete |
| `"Skill search input in add skill modal"` | Add skill text field |
| `"Add more skills button after saving a skill"` | Loop button to keep adding |

### Featured edit modal
| Query | Returns |
|-------|---------|
| `"Plus button to add a new Featured tile"` | + on Featured section |
| `"Add a link option in the Featured add menu"` | Add a link submenu |
| `"URL input field in the Add a Link Featured modal"` | URL field |
| `"Add button next to URL field in Featured modal"` | Triggers OG fetch |
| `"Title field in Featured link modal"` | Editable title |
| `"Description field in Featured link modal"` | Editable description |
| `"Save button in Featured link modal"` | Save |

### Settings — visibility
| Query | Returns |
|-------|---------|
| `"Share profile updates row in visibility settings"` | Toggle for notify-network |
| `"Discoverable on the web toggle in SEO settings"` | SEO toggle |

### Common popups
| Query | Returns |
|-------|---------|
| `"Skip button on People you may know modal"` | Auto-decline after save |
| `"Skip button on Notify your network popup"` | Auto-decline after save |
| `"Close button on Premium upsell modal"` | X on upsell |

---

## ARIA-based fallback selectors

When `find` fails, use these JS-callable selectors via the `javascript_tool`.

### Headline field
```js
document.querySelector('input[name="headline"]')
document.querySelector('input[aria-label*="Headline"]')
```

### About textarea
```js
document.querySelector('textarea[aria-label*="About"]')
document.querySelector('div[data-test-modal-id*="profile-about"] textarea')
```

### Experience description textarea
```js
const modal = document.querySelector('[role="dialog"][aria-label*="experience"]');
modal?.querySelector('textarea')
```

### Skill add input
```js
document.querySelector('input[placeholder*="Skill"]')
document.querySelector('div[role="combobox"][aria-label*="Skill"]')
```

### Featured link URL input
```js
document.querySelector('input[name="url"]')
document.querySelector('input[placeholder*="article, file"]')
```

### Save button (generic in any modal)
```js
const modal = document.querySelector('[role="dialog"]');
modal?.querySelector('button[type="submit"]')
modal?.querySelector('button[aria-label="Save"]')
```

### Notify network toggle (in edit experience modal)
```js
document.querySelector('label[for*="notify-network"] input')
```

---

## What to do when selectors break

LinkedIn ships a UI refresh every 2-4 weeks. Class names rotate; structure mostly stays.

When a `find` query stops returning results:

1. Take a screenshot. Confirm the element still exists visually.
2. Use `read_page` to get the accessibility tree of the area. Find the new aria-label or role.
3. Update the query in this file.
4. If `read_page` shows the element is genuinely gone (LinkedIn removed it), document the workaround in this file with the new flow.

The skill author commits to maintaining this file. If a selector breaks during a real user session, the user should be told: "LinkedIn changed something. I'll work around it for you, but please file an issue at github.com/SayantoDutta/linkedin-revamp/issues so the skill author can patch it." Then attempt the recovery using the fallback selectors above.

---

## Reserved future selectors

These features are not yet implemented but listed here so future versions don't duplicate work:

- Recommendations (request + write)
- Volunteer experience
- Honors and awards
- Publications
- Patents
- Languages
- Pronouns
- Name pronunciation
- Open to work / Open to providing services frames

When adding these to the skill, add the natural-language `find` queries here first.
