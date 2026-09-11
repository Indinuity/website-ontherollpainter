# ontherollpainter.ca

A single-page static site. No build step — the whole site is one HTML file, so you can
edit it in GitHub's web editor and the change is live in about a minute.

```
index.html          the whole site
404.html            what a visitor sees if they follow a bad link
CNAME               tells GitHub which domain to serve
images/             your logo and photos go here (web-ready copies only — see section 2)
tools/prep-photo.py makes a web-ready copy of a photo: resized, and location data removed
robots.txt          tells search engines they may index the site
sitemap.xml         tells search engines the one page that exists
.nojekyll           tells GitHub to serve the files as-is
.htmlvalidate.json  settings for the HTML checker (see "Maintenance")
.gitignore          keeps stray files (originals, OS clutter) out of the repo
```

---

## 1. Things to fill in

Open `index.html` and search for `FILL:` — every spot that still needs your attention is
marked. The short list:

| What | Where it appears | Currently says |
|---|---|---|
| Project captions | four photos in "Previous work" | describe what's visible in each photo; add what only you know |
| Before & after | the paragraph and caption under the Swan kitchen photos | same — confirm it matches how the job went |
| Services | the eight items in "What gets done" | matched to your business card; edit if that changes |
| Stats bar | three panels under the hero | add insurance once you have it |
| About | four paragraphs | names Lexis Carter; read them and make sure they're true |
| Reviews | commented out until you have real ones | see the block above the quote section |
| Formspree ID | the `<form action="...">` | YOUR_FORM_ID |
| Structured data | the `application/ld+json` block in the `<head>` | add logo and image URLs once the files exist |

Already filled in, as requested:

- Business name: **On The Roll Painters** (the domain stays ontherollpainter.ca)
- Services: the list from the business card — rooms, kitchen cabinets, deck staining, stairs
  and railings, closets, furniture, drywall and mudding, backsplash installation
- Tagline: **Affordable Professional Quality Painting** (header, hero, footer, social previews)
- Service area: **Barrie, Innisfil, Orillia, Springwater** (hero, quote section, footer, page title, structured data)
- Email: **ontherollpainter@gmail.com** (quote section and footer)
- Owner: **Lexis Carter** (About section)

**No phone number or address appears anywhere on the site, by request.** The contact
routes are the form and the email address. If that changes later, the places to add a
phone are the header, the quote section lead, the footer contact list, and the
`"telephone"` field in the structured data. Don't add one without asking first.

## 2. Logo and photos

**In place**, made from the photos you sent (web-sized, location data removed):

| File | Made from | Where it shows |
|---|---|---|
| `hero.jpg` | IMG_6147 (white kitchen, dark counters) | top of the page, under the headline |
| `og-image.jpg` | the same photo, cropped 1200×630 | link previews on social and in messages |
| `work-01.jpg` | IMG_6948 (log-home staircase) | Previous work, first pair |
| `work-02.jpg` | IMG_6139 (tall stairwell) | Previous work, first pair |
| `work-03.jpg` | IMG_6826 (two-tone deck) | Previous work, second pair |
| `work-04.jpg` | Barbs kitchen after (5) | Previous work, second pair |
| `before.jpg` | Swan house b4 | Before & after |
| `after.jpg` | Swan house after (2) | Before & after |

Visitors can click or tap any of those to see it full-size. To swap one, run the prep
script (below) on a different original with the same slot name.

**Still needed:**

- `logo.svg` — or `logo.png` with a transparent background. A white or single-colour
  version reads best on the olive header bar. Aim for something legible at 40px tall.
  (The logo on the business card would work, but as the actual artwork file, not a photo
  of the card.)
- `portrait.jpg` — you, working, mid-job, portrait orientation. Not posed against a van.
  For a new business this photo does more work than any other on the page. The About
  section shows a labelled placeholder until it exists.
- `favicon.png` — 512×512. Used for the browser tab and the home-screen icon on phones.

Photos not used: the business-card shots (they show the phone number), "Swan door b4"
(the house number and name plaque are in frame), and "Barbs kitchen" #8 (family photos on
the fridge). Everything else is still on your machine in `images/`, ignored by git.

**Never upload a photo straight from a phone.** Two reasons:

1. They're 3–6 MB each and will make the site crawl. 1600px on the long edge and under
   300 KB is plenty.
2. **Phone photos carry the GPS coordinates of where they were taken** — the customer's
   house — inside the file. Anyone who downloads the photo from the site can read them.
   The `.gitignore` only lets the file names listed above into the repo for exactly this
   reason; a raw `IMG_1234.jpg` dropped into `images/` will be ignored, not published.

`tools/prep-photo.py` does both jobs in one step and leaves the original untouched:

```
python3 tools/prep-photo.py "path/to/original.jpg" work-01
```

That writes `images/work-01.jpg` at web size with all metadata stripped. Use `hero`,
`portrait`, `work-01` … `work-04`, `before`, `after` or `og-image` as the second word.
The four `work-` slots are portrait pairs; a landscape photo dropped into one is shown
centre-cropped on the page and in full when clicked.
(Needs Python with Pillow: `python3 -m pip install pillow`. squoosh.app in the browser
also works — it re-encodes the image, which drops the metadata — but name the output
file yourself.)

Also look at what's *in* the frame before publishing: house numbers, name plaques, mail,
family photos on the fridge, and anything with a licence plate. Crop or skip those.

Once your logo is in, send me the hex codes from it and I'll retune the palette to match —
all the colours live in one `:root` block at the top of the file.

## 3. Making the form work

GitHub Pages only serves files, so the form needs an outside service to deliver mail.

1. Sign up at formspree.io with **ontherollpainter@gmail.com** (free tier: 50 submissions
   a month).
2. Create a form, copy the endpoint — it looks like `https://formspree.io/f/xzyabcde`.
3. Paste it over `https://formspree.io/f/YOUR_FORM_ID` in `index.html`.
4. Submit the form once yourself and confirm the verification email.

Submissions land in your Gmail with the subject "Quote request from ontherollpainter.ca",
and the sender's email is set as reply-to so you can answer directly. The page shows a
confirmation without navigating away. Until the ID is in, the form politely says it isn't
connected yet rather than sending anywhere.

The form asks the customer for their phone number so you can call them back. That's
theirs, not yours — it never appears on the site.

## 4. Publishing

The repository is `github.com/Indinuity/website-ontherollpainter`. Once the files are
pushed to `main`:

1. **Settings → Pages → Source: Deploy from a branch → `main` / `root`.** Save.
2. Same page, under Custom domain, enter `ontherollpainter.ca` and save.
3. Tick **Enforce HTTPS** once it becomes available (can take up to an hour after DNS
   is right).

After that, any edit committed to `main` is live in about a minute.

## 5. DNS

At your domain registrar, delete any existing A or CNAME records for the root, then add:

**A records** for `@`:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**AAAA records** for `@`:
```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

**CNAME** for `www` → `indinuity.github.io.`

GitHub will redirect `www.ontherollpainter.ca` to `ontherollpainter.ca` on its own once
both records resolve.

Then forward the `.com` at its own registrar: a 301 redirect from `ontherollpainter.com`
(and `www`) to `https://ontherollpainter.ca`. Do not point the `.com` at the GitHub IPs —
GitHub Pages serves one custom domain per site and will 404 anything else.

Propagation is usually under an hour but can take a day. Verify these against GitHub's
current docs before you paste them — the IPs change rarely, but they do change:
docs.github.com → Pages → Managing a custom domain.

## 6. The voice

The copy is deliberately blunt. Short sentences, contractions, opinions stated flatly
("painting over old paper never holds"), and no charm. That reads as competent rather
than salesy, and it's easier to live up to in person than a smooth voice would be.

Things to avoid if you rewrite any of it: headings that sound meaningful without saying
anything ("The part you don't see", "Where quality meets care"), everything arranged in
neat threes, and sentences with the contractions stripped out to sound professional.
Those are what make copy read as generic.

The best version of this page is in your own words. If writing isn't your thing, talk
through one of your jobs out loud — what the room looked like, what was wrong with it,
what you did first — and send me that. Rough speech edits into good copy far more easily
than good copy gets written from scratch.

## 7. A note on claims

Nothing on this site claims experience you don't have. There are no years-in-business
figures, no invented reviews, no crew. Keep it that way. A homeowner who catches one
inflated claim discounts everything else on the page, and the honest version is a
stronger pitch anyway: you do the work yourself, you take one job at a time, and you
have availability that booked-out painters don't.

The copy is written in third person, using the business name rather than "we". That is
deliberate: "we" implies staff you don't have, and a homeowner who arrives expecting a
crew and meets one person has been misled before the job starts. One painter is the
selling point, so the site says so plainly.

Project labels are generalised on purpose — "Four rooms" rather than a town and a
duration. That keeps you from publishing specifics you'd have to reconstruct later.
Resist the temptation to go further and reach for the filler every painter's site uses:
years of experience, trusted across the region, a track record of quality. None of it is
checkable, which is exactly why homeowners skim past it. Four honestly described jobs
persuade harder than any amount of it.

Things to verify before this goes live:

- **Insurance.** The site does not say you are insured anywhere, because you aren't yet.
  General liability for a sole-operator painter usually runs a few hundred dollars a
  year, and "are you insured?" is one of the first questions a careful homeowner asks —
  some won't hire without it. When you have a policy: the stats bar has a commented-in
  panel ready, and the footer line has a note showing where "Fully insured" goes.
- **The warranty line in the About section.** It's a promise to come back and fix your
  own failures. Only leave it in if you mean it.
- **The project captions.** They describe only what's visible in each photo. Read them
  against your memory of the job and correct anything that's off. Wallpaper removal was
  dropped from the services list because it isn't on your card — say so if you do it.

## 8. Worth doing after launch

- **Google Business Profile.** For a local trade this drives more calls than the website
  does. The site's job is to make people trust you once the profile sends them here.
  (A Business Profile can be set up as a service-area business with the address hidden,
  which matches how the site is set up.)
- Link the profile in the reviews section once you have a few.
- Add real customer photos as you finish jobs — a gallery that grows is the strongest
  signal you're working.

## 9. Maintenance

For whoever is editing the HTML directly:

- **Check the markup** after any structural edit:
  `npx html-validate index.html 404.html` — should print nothing. The one rule that is
  switched off (`tel-non-breaking`) doesn't apply since there is no phone number.
- **Sitemap.** `sitemap.xml` has a `<lastmod>` date. Bump it when the page content changes
  meaningfully; it's a hint to search engines, not a requirement.
- **Adding pages.** If the site ever grows past one page, each new page needs a `<url>`
  entry in `sitemap.xml`, and the header nav in `index.html` will need real links instead
  of anchors.
- **Colours.** Every colour is a variable in the `:root` block at the top of `index.html`.
  The grey (`--grey`) is tuned to pass WCAG AA contrast on both the off-white and the
  limestone backgrounds; if you lighten it, small caption text stops passing.
- **Adding a new image slot.** If `index.html` gains a new `<img src="images/...">`, add a
  matching `!images/name.jpg` line to `.gitignore` or git will refuse to see the file.
  `work-05.jpg`, `work-06.jpg` and so on are already allowed.
- **Raw originals** left in `images/` on your machine are harmless — git ignores them —
  but keep the real originals somewhere safer than a website folder.
