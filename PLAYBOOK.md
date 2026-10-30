# Daily Reel playbook — @pureorganiczone

Every scheduled run follows this file. Read it fully before making anything.

## Accounts
- Metricool brand id (blogId / brandId): `7649578`, timezone `Asia/Calcutta`.
- Instagram: @pureorganiczone (Business, linked via Facebook page).
- Every Reel posts to ALL connected networks (owner's standing instruction, 26 Oct 2026): Instagram, Facebook (page), YouTube (channel), LinkedIn (owner's personal profile), Pinterest (from 30 Oct 2026, board "pure organic zone products"). Check `getBrandSettings` > `networksData` at the start of each run; if a network is added or removed there, post to whatever is connected.
- Videos are hosted publicly from this repo:
  `https://raw.githubusercontent.com/gjsgopi-dev/pureorganiczone-reels/main/reels/<file>.mp4`

## Daily run, step by step
1. Today's date is in IST. Look for `specs/<YYYY-MM-DD>_*.json`.
2. If no spec exists for today, write one (see "Writing a new spec"). Pick the next item from the rotation, skipping any product used in the last 10 days (check `log.csv`).
3. Build: `tools/make_reel.sh specs/<file>.json reels/<same-name>.mp4`.
4. Look at 3 frames (start, middle, end) to check text fits and nothing overlaps or shows a missing-glyph box.
5. Commit the spec and video, push to `main`.
6. Wait until `raw.githubusercontent.com` serves the file (check with `gh api repos/gjsgopi-dev/pureorganiczone-reels/contents/reels/<file>.mp4`).
7. Schedule in Metricool with `createScheduledPost`: Instagram type from the spec's `ig_type` field, or if missing, from "Growth strategy > Weekly cadence" below (REEL or TRIAL_REEL); always set `isAiGenerated: false` for our own generated text-and-graphics Reels, `showReelOnFeed: true` (REEL only), `autoPublish: true`, `draft: false`, media = the raw URL, `videoCoverMilliseconds: 1500`, caption from the spec, time = spec `post_time` (default 17:45 IST) today. If that time has passed, use the next free hour from Metricool's best-times.
   One post, all networks: `providers` = instagram, facebook, youtube, linkedin, pinterest, with
   - `facebookData`: `{"type": "REEL"}`
   - `youtubeData`: `{"type": "short", "title": <spec title, or the caption's first line without emoji, max 100 chars>, "privacy": "public", "madeForKids": false, "category": "HOWTO_STYLE", "tags": <5–7 search phrases from the caption>, "isAiGeneratedContent": <same as Instagram isAiGenerated>}`
   - `linkedinData`: `{"type": "post", "previewIncluded": true, "publishImagesAsPDF": false}`
   - `pinterestData`: `{"boardId": "895372038356868033", "pinTitle": <same as the YouTube title>, "pinLink": <spec `product_url`>, "isAiGenerated": <same as Instagram isAiGenerated>}` (video pin). Board id 895372038356868033 = "pure organic zone products" (verified 30 Oct 2026 with a test pin).
   Owner-made Reels with realistic AI people (e.g. from Muse) get `isAiGenerated: true` on Instagram and `isAiGeneratedContent: true` on YouTube.
   If one network rejects the post, retry once without that network, then tell the owner which one failed and the exact error.
8. Before scheduling, call `getScheduledPosts` for today so you never double-post. Only a post that includes Instagram counts as today's Reel. Pinterest-only pins (e.g. the 30 Oct 07:20 test pin, post id 410733741) are NOT the daily Reel: ignore them in this check and in the task prompt's "already scheduled or published" check, and schedule the Reel as normal.
9. Clean up: Metricool copies the video to its own storage when the post is created. Only if the `createScheduledPost` response's `media` URL starts with `https://static.metricool.com/`, delete the video from the repo (`git rm reels/<file>.mp4`). If the media URL still points at GitHub, keep the video and say so in the owner message.
10. Append to `log.csv`: date, slug, product, mood, metricool post id, planner URL. Commit the cleanup and the log row together and push.
11. Send the owner one short message: what was scheduled, when, and the planner link.

The `reels/` folder should normally be empty between runs; specs stay in `specs/` as the record of what was posted.

If any step fails (build, push, Metricool error), stop, do not retry in a loop, and message the owner with the exact error and what is needed.

## Growth strategy — win shoppers who already buy organic elsewhere
Goal: reach people who already buy A2 ghee, millets, cold-pressed oils and organic staples from national D2C brands, quick-commerce apps and other Hyderabad organic stores, and give them a clear reason to switch to us. Every Reel must do one of three jobs: **reach** new people, **convince** them we're the better choice, or **convert** them to an order.

### Weekly cadence
- **Tue, Thu, Sat: TRIAL_REEL.** Instagram shows Trial Reels only to non-followers, so these are for reaching new shoppers. Use the strongest hook formats (myth vs fact, "did you know", label check). Leave out `showReelOnFeed`.
- **Mon, Wed, Fri, Sun: REEL** (normal, shown to followers and on the feed). Use convince/convert formats (why it costs more, how to use, offer).
- If a Trial Reel's views beat our 7-day Reel average, the weekly report lists it so the owner can share it to the main feed from the Instagram app.

### Formats that pull in shoppers who buy elsewhere (no competitor names, ever)
- **Label check:** "3 things to check on your ghee/oil/millet pack" (method, ingredients list, single origin). Shoppers check their current pack and see why ours is better.
- **"Is your ___ really ___?":** e.g. "Is your ghee really bilona?", "Is your oil really cold-pressed?" Explain how to tell, then show ours.
- **Price-value:** our offer price against our own MRP, with what's inside a combo and the cost per day or per serving. Never quote or guess other brands' prices.
- **Local advantage (Hyderabad):** fresh produce and country chicken delivered the same day in three slots, a store in Madhapur, and you can walk in and see the products. National brands can't match this, so use it in every Hyderabad post.
- **Swap series:** "Swap of the Day": one everyday product and our better alternative.
Name the series in captions ("Swap of the Day #4", "Label Check") so people follow to see the next one.

### Make Reels easier to find (search reaches people who don't know us)
- Scene 1 shows the search phrase on screen, e.g. "A2 GHEE" or "MILLET NOODLES FOR KIDS".
- The caption's first line includes the phrase people search: product + benefit or place ("A2 bilona ghee Hyderabad", "millet noodles for kids").
- Hashtags: 2 broad category tags (#OrganicFood #HealthyEating), 3 product tags (#A2Ghee #BilonaGhee #MilletNoodles), 1–2 Hyderabad tags on local posts, then #PureOrganicZone. 6–8 total.

### Shorter Reels (for specs written from 2 Nov 2026)
- 4 scenes, 11–14 seconds total. Scene 1 at most 2.0 s, a hook with a question or a surprising fact. People should finish and replay it.

### Captions that sell
- End every caption with one clear action, rotating between: "Follow for a healthy swap every day", "Send this to someone who still buys ___", "Save this for your next grocery order".
- Always include the offer price and `🛒 pureorganiczone.com (link in bio)`.
- If `catalog.md` has an "Active offers" section with a first-order code, add it to convert posts. Never invent a code or discount.

### What the owner does (the weekly report reminds them)
- Add 5–8 competitor Instagram accounts in Metricool (Competitors section) so the weekly report can learn from their best Reels.
- Collab posts with Hyderabad food, mom and fitness creators. When a collab is agreed, add the handle to the spec as `collaborators` and pass it in `instagramData.collaborators`.
- Reply to every comment and DM in the first hour after a post.
- Paid boost: the weekly report recommends one Reel to boost and an audience (Hyderabad + 25 km, age 25–50, interests: organic food, ghee, millets, healthy eating, fitness, parenting). **Scheduled runs never spend money or create boosts.** The owner decides.

## Paid audiences — show our best Reels to the right buyers (Meta ads)
Organic posting reaches followers and Instagram's own picks. To choose WHO sees a Reel (region, budget, health interest, buying history, competitors' audiences) the Reel must run as a Meta ad (Instagram + Facebook). Ad account: `act_892451579536419`.
**Rule: scheduled runs never create, launch or change paid ads. They only recommend. Every rupee is approved by the owner in chat.**

### Audiences (build once in Meta Ads Manager, reuse every week)
| # | Audience | Who | Targeting | Lead with |
|---|---|---|---|---|
| A1 | Hyderabad health-conscious | Near us, can get fresh delivery | Hyderabad + 15 km (Madhapur, Gachibowli, Kondapur, Kukatpally, Jubilee Hills, Banjara Hills, Manikonda, Miyapur), age 25–55, interests: organic food, healthy diet, Ayurveda, yoga, fitness, vegetarian cooking; behaviour: engaged shoppers | Fresh produce, country chicken, same-day slots, Telugu line |
| A2 | Competitor shoppers (pan-India) | Already buy organic/A2/millets elsewhere | Metros: Hyderabad, Bengaluru, Chennai, Pune, Mumbai, Delhi NCR; age 25–55; interests: A2 milk, ghee, millets, organic food, plus organic-brand interests where Meta lists them (e.g. Organic India, 24 Mantra Organic, Two Brothers Organic Farms, Akshayakalpa; check each exists in Ads Manager's interest search); behaviour: engaged shoppers, online shoppers | Label Check / "Is it really?" Reels, then the price-value offer |
| A3 | Value seekers | Healthy but price-conscious | Same regions as A1 + A2, age 22–45, interests: healthy diet, home cooking, parenting, budget cooking | Low-price entry products: millet noodles ₹54, mustard oil ₹90, sabja ₹99, moringa ₹199 |
| A4 | Parents | Kids' snacks and breakfast swaps | Same regions, age 26–45, interests: parenting, toddlers/school-age children, healthy snacks | Millet noodles, snack hamper, ragi pancake mix |
| W1 | Warm: our engagers | Watched or interacted but haven't bought | Custom audience: Instagram account engagers (90 days) + people who watched ≥50% of our Reels | Offer Reels with price and pureorganiczone.com |
| W2 | Warm: site visitors | Visited the site, didn't buy | Custom audience from the Meta pixel on pureorganiczone.com (30 days), excluding purchasers | The product they viewed, combos, any active offer |
| B1 | Actual buyers | Past customers | Custom audience from our customer list (phone/email from website and store orders, only customers who agreed to marketing) | New products, refills (ghee, oil), festive combos |
| L1 | Lookalike of buyers | New people who resemble our buyers | 1–3% India lookalike of B1 (needs 100+ matched customers) | Best-performing Reel of the week |

Exclude B1 (past buyers) from A1–A4 and L1 so acquisition money isn't spent on existing customers.

### Launch plan v1 (decided 26 Oct 2026, owner to approve budget)
- Clean-up: owner archives all 28 old campaigns in Ads Manager (archiving keeps their history, so Meta can still learn from past results). Pop Wash (the only active one) is turned off.
- Campaign 1 "POZ Reels Sales": objective Sales, pixel `1219471509602200` event Purchase (fall back to Traffic → landing page views if Events Manager shows no Purchase events), Advantage campaign budget ₹300/day, placements Instagram + Facebook Reels, Feed, Stories. Ad sets:
  1. Hyderabad 15 km, 25–55, Organic food + Healthy diet + Yoga, narrowed to Engaged Shoppers. Ads: ghee "Is your ghee really bilona?" Reel, Hyderabad veggie box Reel. Landing: the product page.
  2. Metros (Bengaluru, Chennai, Pune, Mumbai, Delhi NCR, Hyderabad), 25–55, Organic food + Organic product + Organic food stores, narrowed to Engaged Shoppers. Ads: ghee Reel, oil Label Check Reel. (The "competitor shoppers" ad set.)
  3. Parents in the same cities, 26–45, Parenting + Baby food. Ad: millet noodles Reel.
  Exclude a "Purchasers 180 days" pixel audience once it exists.
- Campaign 2 "POZ Followers": objective Traffic, destination Instagram profile, ₹100/day, metros + Hyderabad, Organic food + Healthy diet. Ads: the best Label Check / Trial Reel of the week. Purpose: follows from people who buy organic elsewhere.
- Review after 7 days: keep the ad set with the lowest cost per purchase (Campaign 1) and per profile visit (Campaign 2); swap in that week's best Reel.

### Verified Meta setup (checked via Adspirer, 26 Oct 2026)
- Ad account `act_892451579536419` (currency INR). Facebook Page: Pure Organic Zone. Instagram for ads: @pureorganiczone, id `17841471100992317`.
- Pixel to use: **Pure organic zone** `1219471509602200` (firing). The other pixel "pure organic sales" `1888524538550211` has never fired; ignore it.
- Custom audiences: none yet (W1, W2, B1, L1 must be created in Ads Manager first).
- Location: Hyderabad city key `1027234` (type city, Telangana); use radius 15 km.
- Interest ids that exist: Organic food `6002868910910`, Organic product `6004002883706`, Organic food stores `6805147143063`, Organic farming `6003322650741`, Healthy diet `6003382102565`, Human nutrition `6002933862573`, Yoga `6003306084421`, Parenting `6003232518610`, Baby food `6003704126313`. Behaviour: Engaged Shoppers `6071631541183`.
- **Not available in Meta**: ghee, millet, Ayurveda, BigBasket, Organic India, Patanjali (and likely other Indian organic brands). So "competitor shoppers" = people interested in organic food/products/stores + engaged shoppers, and the Label Check / "Is it really?" creative does the competitor-switching work.
- Adspirer free plan: 15 actions per month (reset on the 25th). Use them for creating campaigns, not exploring.
- Existing campaign still ACTIVE: "Post: Pop Wash home care essentials now available" `120245407649150654` (engagement, since Apr 2026). Ask the owner whether it should keep running.

### Health targeting rules (Meta policy)
- Do not target or imply medical conditions (diabetes, BP, PCOS, weight). Meta removed these targeting options, and ad text must not say "you have diabetes" or similar. Target wellness interests only (healthy diet, fitness, Ayurveda, organic food).
- Diabetes/weight-kit Reels can run as ads only with the doctor line and no promise of results.

### Starting budget (owner to approve)
- ₹300/day (~₹9,000/month) in week 1: ₹100 A1 Hyderabad, ₹100 A2 competitor shoppers, ₹50 A3 value, ₹50 W1 warm engagers.
- After 7 days, move money to the audience with the lowest cost per landing-page view or purchase; pause any ad set whose cost is 2x the best.
- Add W2, B1 and L1 once the pixel and customer list are set up.

### What the weekly report adds
- From Metricool Meta Ads metrics (network `metaAds`), report spend, reach, cost per result and purchases by audience if ads are running.
- Pick the week's best Reel (highest saves+shares per view) and recommend which audience above to run it to, with a budget. Never launch it.

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
- `ig_type` ("REEL" or "TRIAL_REEL", by weekday per Growth strategy), optional `series` (e.g. "Label Check #2", "Swap of the Day"), optional `collaborators` (list of Instagram handles agreed by the owner).
- `date`, `post_time` ("17:45"), `music` (`warm` | `bright` | `calm`), `title`, `caption`, `handle` ("@pureorganiczone"), `scenes`.
- 5 scenes, 17–19 seconds total. Scene 1 is the hook (dark theme, a tag + a question or bold claim). Last scene is the offer: tag, product name, `price` item with `now`/`was`, the `pureorganiczone.com` button, and a `small` line ("Delivered all over India" or the Hyderabad note).
- Scene item types: `tag`, `title` (optional `size`), `big`, `body`, `bullets`, `price`, `button`, `small`. Keep bullets to 3–4 items of under 6 words.
- Only use characters in the Poppins font. Do not use arrows (→), emoji or Indian scripts in scenes. Emoji and Telugu/Hindi are fine in captions.
- Prices come from `catalog.md` (round to whole rupees on screen, e.g. ₹1,391).

## Captions
- First line is the hook, then 2–4 short lines of value, then `👉 price`, `🛒 pureorganiczone.com`, a save/share/tag prompt, then 6–8 hashtags ending with `#PureOrganicZone`.
- Hyderabad posts: add one Telugu line and local hashtags (#Hyderabad #Madhapur #Gachibowli #Kondapur).
- Product link (from 27 Oct): add the product's own page URL (e.g. `https://pureorganiczone.com/product/combo-dry-fruits-9gPxn2`) on the `🛒` line instead of the bare domain. It is clickable on Facebook, YouTube and LinkedIn; on Instagram it is plain text, so the caption also says "link in bio" or "Comment <WORD> and we'll DM you the link". Find the URL by fetching the homepage with curl (WebFetch is blocked for this domain) and matching `/product/<slug>`; check the page returns 200 and shows "Add to cart" before using it.
- Every caption asks for one comment ("Comment GIFT", "1 or 2?", "Tag a friend who…"): comment-asking posts are what drive comments for competitors (see Learnings, 27 Oct).

## Health and claims rules (strict)
- Describe nutrients and traditional use; never claim a food cures, treats or prevents a disease.
- Anything about diabetes, blood sugar, weight, BP or medicine ends with: "Always follow your doctor's advice and medication." (or "Not a substitute for medical advice.")
- Organic produce: say "grown without synthetic pesticides", not "chemical-free".
- Never invent certifications, farm names, founder stories, customer reviews or numbers.
- Never use competitors' videos, images, music or brand names in the Reel.

## Weekly report (Mondays)
Pull the last 7 days of Instagram Reels metrics (IGRE01 date, IGRE03 content, IGRE11 reach, IGRE23 views, IGRE12 saves, IGRE21 shares, IGRE08 engagement, IGRE27 retention) and competitor metrics (IGCO02, IGCO07, IGCO10, IGCO12). Rank our Reels, name the top topic and format, compare with competitors' engagement, and write 2–3 concrete changes into the "Learnings" section below so daily runs use them.
Also:
- Competitor Reels (IGCR01 competitor, IGCR03 text, IGCR05 date, IGCR09 interactions, IGCR10 engagement): list their top 5 Reels by interactions and name the topic and format of each. Turn what works into our own original ideas. Never copy their scripts, video, music or claims.
- Compare Trial Reels with normal Reels (views, reach, follows if available). List Trial Reels worth sharing to the feed.
- Recommend one Reel to boost and the audience (see Growth strategy). Do not spend.
- If no competitors are set up in Metricool, remind the owner to add them.

## Learnings
- 26 Oct report (19–26 Oct): only 2 Reels in Metricool, both owner-made Hyderabad meat posts on 25 Oct. Country chicken: reach 43, views 70, 1 save, 0 shares, engagement 4.7%. Goat meat: reach 35, views 79, 0 saves, 1 share, engagement 8.6%. Retention not reported. Sample is too small to judge topics; treat these as the baseline to beat (reach ~40, views ~75 per Reel).
- Both meat Reels had no on-screen search phrase, no price and no save/share action, and got 1 save+share each. On every Hyderabad fresh-produce/meat spec: scene 1 shows the search phrase ("COUNTRY CHICKEN HYDERABAD"), the offer scene shows the price from `catalog.md`, and the caption ends with "Send this to someone in Hyderabad who still buys ___". Keep the "60–90 min delivery, Hyderabad only" line; it is the local advantage.
- No competitors in Metricool yet (IGCO returned nothing), so there is no engagement benchmark. Until they are added, compare each week against our own previous week. Owner-made Reels are not in `log.csv`; daily runs should add a row (slug "owner_<product>", mood "owner") for any Reel found in Metricool that is missing from the log, so the weekly report can match it to a topic.
- 26 Oct: an owner-made Millet Noodles Reel was posted at 07:15 IST (AI-generated label on). Skip millets/noodles until 2 Nov.
- 27 Oct sales review (full plan: Docs "Pure Organic Zone: Sales Growth Plan"): Hyderabad fresh-meat Reels reached 242 and 184 vs 34–98 for packaged Reels (3.7x on average), so schedule a Hyderabad fresh-food Reel at least twice a week. No Reel reached 1% of the 44,419 followers, and the account lost 113 and gained 9 followers 21–24 Oct; the weekly report tracks reach per Reel (baseline 120) and follower change. Website blockers found: homepage 15 MB / ~40 s on 4G, forced login at checkout, city popup, WhatsApp link wa.me/9177203162 missing country code, Meta pixel sends only PageView. Until the owner confirms these are fixed, link captions to product pages, never the homepage, and recheck them in each weekly report.
