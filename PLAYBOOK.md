# Daily Reel playbook — @pureorganiczone

Every scheduled run follows this file. Read it fully before making anything.

## Accounts
- Metricool brand id (blogId / brandId): `7649578`, timezone `Asia/Calcutta`.
- Instagram: @pureorganiczone (Business, linked via Facebook page).
- Videos are hosted publicly from this repo:
  `https://raw.githubusercontent.com/gjsgopi-dev/pureorganiczone-reels/main/reels/<file>.mp4`

## Daily run, step by step
1. Today's date is in IST. Look for `specs/<YYYY-MM-DD>_*.json`.
2. If no spec exists for today, write one (see "Writing a new spec"). Pick the next item from the rotation, skipping any product used in the last 10 days (check `log.csv`).
3. Build: `tools/make_reel.sh specs/<file>.json reels/<same-name>.mp4`.
4. Look at 3 frames (start, middle, end) to check text fits and nothing overlaps or shows a missing-glyph box.
5. Commit the spec, video and `log.csv` row, push to `main`.
6. Wait until `raw.githubusercontent.com` serves the file (check with `gh api repos/gjsgopi-dev/pureorganiczone-reels/contents/reels/<file>.mp4`).
7. Schedule in Metricool with `createScheduledPost`: Instagram REEL, `showReelOnFeed: true`, `autoPublish: true`, `draft: false`, media = the raw URL, `videoCoverMilliseconds: 1500`, caption from the spec, time = spec `post_time` (default 17:45 IST) today. If that time has passed, use the next free hour from Metricool's best-times.
8. Before scheduling, call `getScheduledPosts` for today so you never double-post.
9. Append to `log.csv`: date, slug, product, mood, metricool post id, planner URL.
10. Send the owner one short message: what was scheduled, when, and the planner link.

If any step fails (build, push, Metricool error), stop, do not retry in a loop, and message the owner with the exact error and what is needed.

## Content rotation (one per day, repeat the cycle)
1. A2 bilona ghee or a ghee combo — tradition and method
2. Millets / breakfast swap (noodles, dosa mix, upma, jowar poha, cookies)
3. Hyderabad fresh produce or country chicken/mutton — local, Telugu line in caption
4. Oils — cold-pressed education, regional use (mustard North, groundnut/sesame South)
5. Health kit (diabetes, weight-loss, breakfast) — food swaps, always with the doctor line
6. Superfood daily habit (moringa, wheatgrass, seeds, green tea)
7. Rare or regional (Meghalaya spices, mushrooms, honey, podis) or vendor spotlight
Rotate formats too: myth vs fact, 3 quick swaps, how to use, why it costs more, comparison, "did you know".

## Writing a new spec
Copy the structure of an existing spec in `specs/`. Fields:
- `date`, `post_time` ("17:45"), `music` (`warm` | `bright` | `calm`), `title`, `caption`, `handle` ("@pureorganiczone"), `scenes`.
- 5 scenes, 17–19 seconds total. Scene 1 is the hook (dark theme, a tag + a question or bold claim). Last scene is the offer: tag, product name, `price` item with `now`/`was`, the `pureorganiczone.com` button, and a `small` line ("Delivered all over India" or the Hyderabad note).
- Scene item types: `tag`, `title` (optional `size`), `big`, `body`, `bullets`, `price`, `button`, `small`. Keep bullets to 3–4 items of under 6 words.
- Only use characters in the Poppins font. Do not use arrows (→), emoji or Indian scripts in scenes. Emoji and Telugu/Hindi are fine in captions.
- Prices come from `catalog.md` (round to whole rupees on screen, e.g. ₹1,391).

## Captions
- First line is the hook, then 2–4 short lines of value, then `👉 price`, `🛒 pureorganiczone.com`, a save/share/tag prompt, then 6–8 hashtags ending with `#PureOrganicZone`.
- Hyderabad posts: add one Telugu line and local hashtags (#Hyderabad #Madhapur #Gachibowli #Kondapur).

## Health and claims rules (strict)
- Describe nutrients and traditional use; never claim a food cures, treats or prevents a disease.
- Anything about diabetes, blood sugar, weight, BP or medicine ends with: "Always follow your doctor's advice and medication." (or "Not a substitute for medical advice.")
- Organic produce: say "grown without synthetic pesticides", not "chemical-free".
- Never invent certifications, farm names, founder stories, customer reviews or numbers.
- Never use competitors' videos, images, music or brand names in the Reel.

## Weekly report (Mondays)
Pull the last 7 days of Instagram Reels metrics (IGRE01 date, IGRE03 content, IGRE11 reach, IGRE23 views, IGRE12 saves, IGRE21 shares, IGRE08 engagement, IGRE27 retention) and competitor metrics (IGCO02, IGCO07, IGCO10, IGCO12). Rank our Reels, name the top topic and format, compare with competitors' engagement, and write 2–3 concrete changes into the "Learnings" section below so daily runs use them.

## Learnings
- (none yet — first report due Monday 2 Nov 2026)
