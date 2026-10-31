# Daily Reel playbook — @pureorganiczone

Every scheduled run follows this file. Read it fully before making anything.

## Accounts
- Metricool brand id (blogId / brandId): `7649578`, timezone `Asia/Calcutta`.
- Instagram: @pureorganiczone (Business, linked via Facebook page).
- Every Reel posts to ALL connected networks (owner's standing instruction, 26 Oct 2026): Instagram, Facebook (page), YouTube (channel), LinkedIn (owner's personal profile), Pinterest (from 30 Oct 2026, board "pure organic zone products"). Check `getBrandSettings` > `networksData` at the start of each run; if a network is added or removed there, post to whatever is connected.
- **App (owner, 31 Oct 2026):** the "Pure Organic Zone" app is on the App Store and Google Play. Ordering in the app gets better prices than elsewhere, and customers can subscribe for daily, weekly or monthly delivery. Every Reel's narration and caption sends people to the website or the app (see "Captions"). Never state a discount percentage or app-only price unless the owner gives it.
- Owner brand clips (photoreal AI, 10 s, end on a red brand card with WhatsApp 9704518572 and "60–90 min delivery"), hosted on HeyGen for the story Reels' last scene:
  - natu kodi / country chicken: `https://resource2.heygen.ai/video/ec7865a5ce94495883cb5d70c3f7095e/original.mp4`
  - goat meat (shop, curry, family, app map): `https://resource2.heygen.ai/video/602adc35f67d4b7db3b2496fd5b0d515/original.mp4`
  - goat meat delivery (packing, rider, doorstep): `https://resource2.heygen.ai/video/5e19c60048d64b0c81841d8e3736c3e5/original.mp4`
  - organic store (vegetables, packed meat, rider, website card): `https://resource2.heygen.ai/video/1c1b805c3a7d44cfabe28ec83637cc10/original.mp4`
- Videos are hosted publicly from this repo:
  `https://raw.githubusercontent.com/gjsgopi-dev/pureorganiczone-reels/main/reels/<file>.mp4`

## Daily run, step by step
1. Today's date is in IST. Look for `specs/<YYYY-MM-DD>_*.json`.
2. **Learn first.** Pull the last 14 days of metrics from every connected network (see "Weekly report" for the fields; at minimum Instagram Reels IGRE03, IGRE11 reach, IGRE23 views, IGRE07 comments, IGRE12 saves, IGRE21 shares). Note which topic and story angle got the most reach and the most comments, and lean today's choice toward it within the weekly cadence. Read "Learnings".
   If no spec exists for today, write one (see "Writing a new spec"). Pick the next item from the cadence/rotation, skipping any product used in the last 10 days (check `log.csv`). An existing spec without `"format": "story"` is rewritten as a story Reel on the same product.
3. Build the Reel as a **narrated village story** (default from 31 Oct 2026, owner's standing instruction: "any video you make, do this kind of narration"). See "Village story Reels" below. Only if HeyGen fails or premium credits are under 20, build a 15 s HeyGen food-shot Reel ("HeyGen AI-video Reels"); under 15 credits, build the old way: `tools/make_reel.sh specs/<file>.json reels/<same-name>.mp4` (then `isAiGenerated: false`).
4. Look at 5 frames (one per card) to check the text fits, each card sits on its matching shot, and the AI footage has no garbled text, logos, faces or deformed hands.
5. Commit the spec and video, push to `main`.
6. Wait until `raw.githubusercontent.com` serves the file (check with `gh api repos/gjsgopi-dev/pureorganiczone-reels/contents/reels/<file>.mp4`).
7. Schedule in Metricool with `createScheduledPost`: Instagram type from the spec's `ig_type` field, or if missing, from "Growth strategy > Weekly cadence" below (REEL or TRIAL_REEL); set `isAiGenerated: true` (and YouTube `isAiGeneratedContent: true`, Pinterest `isAiGenerated: true`, `isAiGeneratedPerson: false`) for HeyGen Reels and `isAiGenerated: false` for text-and-graphics Reels built with make_reel.sh, `showReelOnFeed: true` (REEL only), `autoPublish: true`, `draft: false`, media = the raw URL, `videoCoverMilliseconds: 1500`, caption from the spec, time = spec `post_time` (default 17:45 IST) today. If that time has passed, use the next free hour from Metricool's best-times.
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

### Competitor lessons (review of 30 Oct 2026, Docs "Pure Organic Zone: Competitor Reels & Ads Review")
National brands sell trust with celebrities and proof (tests, farmer counts, certificates); quick commerce sells cheaper certified staples in 10 minutes. Don't fight on staple price, speed or range. Win on:
- **Fresh goat meat is our lead product** (owner, 30 Oct 2026: it sells well and has few local competitors). Goat meat Reels on **Monday** (curry cut or boneless) and **Friday** ("order today for your weekend": keema, curry cut, or paya / head curry cut, which are next-day delivery). Rotate cuts and dishes (mutton curry, keema, paya soup, biryani, Sunday lunch) so no cut repeats within 10 days.
- **Other fresh food on Wednesday** (country chicken, vegetables, fruits, eggs), and **Sunday** may be a Sunday-lunch meat Reel. Always show the delivery slot ("Order by 11 AM for today's 11–3 slot") and "Hyderabad only". Never name or compare with other meat shops or apps.
- Goat meat hooks use what Hyderabad people search: "MUTTON HOME DELIVERY HYDERABAD", "FRESH GOAT MEAT HYDERABAD", "MUTTON KEEMA HYDERABAD", "PAYA HYDERABAD". Telugu line in the caption ("తాజా మేక మాంసం మీ ఇంటికే"). Claims stay factual: fresh, cut to order only if the owner confirms it, delivery slots, price. No health claims about meat.
- When recommending a Reel to boost in the weekly report, prefer the best goat meat Reel.
- **Proof series, once a week (Saturday Trial Reel):** one product's certificate, lab report or farm source on screen. Use only real documents in `assets/proof/` (owner-supplied). If none exists for that product, say "Ask us for the certificate in DM" and show the product instead. Never invent or imply a certificate, test or farm.
- **Kits and ghee over single staples:** lead convert Reels with combos and ghee, where our offer prices are strongest. Single dal/rice/atta Reels only as part of a swap or kit.
- **A real person on camera when the owner supplies footage** (owner, staff, Madhapur store). Hook line examples: "Walk in and see it", "Picked this morning".
- **Habit language:** "this week's swap", "your Monday fresh order", daily-habit series names, so one order becomes a routine.

### Make Reels easier to find (search reaches people who don't know us)
- Scene 1 shows the search phrase on screen, e.g. "A2 GHEE" or "MILLET NOODLES FOR KIDS".
- The caption's first line includes the phrase people search: product + benefit or place ("A2 bilona ghee Hyderabad", "millet noodles for kids").
- Hashtags: 2 broad category tags (#OrganicFood #HealthyEating), 3 product tags (#A2Ghee #BilonaGhee #MilletNoodles), 1–2 Hyderabad tags on local posts, then #PureOrganicZone. 6–8 total.

### Shorter Reels (for specs written from 2 Nov 2026)
- 4 scenes, 11–14 seconds total. Scene 1 at most 2.0 s, a hook with a question or a surprising fact. People should finish and replay it.

### Captions that sell
- End every caption with one clear action, rotating between: "Follow for a healthy swap every day", "Send this to someone who still buys ___", "Save this for your next grocery order".
- Always include the offer price and `🛒 pureorganiczone.com (link in bio)`.
- Add UTM tags to the product link in every caption and Pinterest `pinLink`: `?utm_source=instagram&utm_medium=reel&utm_campaign=<spec slug>` (check the tagged URL still returns 200). This lets website analytics show which Reels sell.
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

## Village story Reels (default from 31 Oct 2026)
The owner's model Reels: "Taatha's Sunday Natu Kodi" (31 Oct 19:00, post 411619492) and "Taatha's Festival Mutton" (1 Nov 09:00, post 411619545). Photoreal AI people and village scenes, an Indian English narrator telling a short heritage story, English + Telugu captions, ending on the owner's brand clip with the app band.
**Story angles** (rotate; tie each to the day's product): how our grandparents raised/ate it (taatha, paati, ammamma, village courtyard, wood fire, clay pot, banana leaf); festival or Sunday family meals (Sankranti/Kanuma, Bonalu, Dasara, Sunday lunch); the farmer or shepherd behind it (dawn fields, grazing hills, backyard hens); a tradition explained (bilona churning, wood-pressed oil, millet rotte, hand-pounded spices); then → today, the same food delivered in Hyderabad or across India.
**Health wording:** our elders "ate simple, fresh, home-grown food and stayed active". Never say a food made them healthy, cures or prevents anything, and no health claims about meat (see rules below).
1. Spec: `"format": "story"`, plus `story_clips` (2 items: `heygen_prompt`, `en` caption ≤ 40 characters, `te` Telugu caption, `start`), `end_clip` (one brand clip URL from "Accounts": natu kodi clip for country chicken, a goat clip for mutton, the organic store clip for everything else), `voiceover`, `voice_id`, plus the usual `title`, `caption`, `ig_type`, `post_time`, `product_url`.
2. Two `text_to_video` calls (in parallel): `aspectRatio` "9:16", `duration` 8, `resolution` "1080p". Prompt: "Photorealistic cinematic vertical shot, …", rural Telangana setting, named Indian people (grandfather in white dhoti, grandmother in cotton saree, farmer, family), warm natural light, one camera move, "No text, no logos." Never show a doctor, medicine, a hospital, a competitor brand or a child eating raw meat. Poll `get_model_video` every 30 s.
3. One `create_speech_without_player` call, voice **Rahul – Bright & Warm** `080227efd3874821a1328e1b5ff1620f` (keep this voice so the account sounds consistent), speed 1. Script: 55–70 words, three parts separated by exactly two `<break time="0.6s"/>` tags: story line for clip 1 (≈ 6–8 s) `<break>` story line for clip 2 (≈ 6–8 s) `<break>` the pitch (≈ 10 s): "Today, Pure Organic Zone brings … to your home in Hyderabad in 60 to 90 minutes" (fresh food; "delivered all over India" for packaged products) + "Order on our website, or download the Pure Organic Zone app on the App Store or Google Play for better prices, and subscribe daily, weekly or monthly." Save the response's `word_timestamps` to `<scratchpad>/ts.json` with the Write tool.
4. Download the clips and the wav with curl, put the local paths in a copy of the spec's `story_clips` (`file` field), then: `python3 tools/story_reel.py <spec copy> <voice.wav> <ts.json> reels/<same-name>.mp4`. The tool slows a clip up to 1.7x if a line runs long (it stops with an error if longer: shorten that line and generate the voiceover once more), adds the caption boxes and brand tag, plays the brand clip last with the app band ("Get the Pure Organic Zone app · App Store · Google Play · Subscribe daily, weekly or monthly"), and normalises loudness.
5. Look at one frame per scene. Regenerate a clip at most once, and only for garbled text, extra limbs, deformed hands or faces, or anything that breaks the rules above.
6. Instagram `isAiGenerated: true`, YouTube `isAiGeneratedContent: true`, Pinterest `isAiGenerated: true`, `isAiGeneratedPerson: true` (story Reels show AI people).
7. Credits: about 7.5 premium credits per 8 s clip, so one story Reel ≈ 15 credits; 30 a month ≈ 450 of the 600 monthly credits. Call `get_current_user` after building and put the remaining credits in the owner message. If under 20 before building, use the fallback in step 3 of the daily run and tell the owner.
8. Comments: the caption's question is about the viewer's own memories or preference ("What did your ammamma cook on Sundays?", "Jonna rotte or rice?"). These are the posts most likely to get comments.

### Sales-led weekly cadence (from 2 Nov 2026; replaces the day plan in "Competitor lessons" where they differ)
Real site orders (catalog.md "Best sellers by real orders") show Hyderabad fresh food is 89% of orders, and every subscription product is fresh. So:
- **Mon:** goat meat story (curry cut, boneless, keema; rotate). **Fri:** goat or sheep meat weekend story (sheep meat is the #3 seller, 485 orders; paya and head curry are next-day).
- **Wed:** weekly vegetable box or fruit story with **subscription** as the call to action ("set it once, fresh every week"), using spinach, beans, gourds, tomatoes, coriander, banana, papaya, pomegranate.
- **Sat:** natu kodi or country eggs story (Proof Reel only when a real document exists in `assets/proof/`).
- **Sun:** Sunday-lunch meat story (morning post, 8:30–9:30 IST, when meat orders are placed).
- **Tue, Thu: Vendor Spotlight story** (below), picking from catalog.md "Vendor best sellers", never the same vendor within 14 days.
- Every fresh-food story names the subscription option; every Reel names the website and the app.

### Vendor Spotlight story Reels (owner, 31 Oct 2026)
Feature one marketplace vendor and its best-selling products by name, to sell those products and show the range of the marketplace.
- Story: the place and tradition behind the vendor's product (Meghalaya pepper hills for GreeNE Origins, Tamil heritage rice fields for Divyams, millet fields for Milletio's bars, a kolhu oil press for Yashoda's oils, a Telugu kitchen making podis for ANIKA). Narration names the vendor once ("from GreeNE Origins, on Pure Organic Zone"), the on-screen caption names the product, and the pitch is "delivered all over India, order on our website or app".
- Use only the vendor's brand name. No vendor logo, photos, videos or claims taken from their site or social media unless the owner says the vendor agreed; never invent a farm, founder or certificate for them. Prices and links come from `tools/site_sales.py` / the product page.
- Supplements and wellness mixes (e.g. Auranectra): no health claims, add "Not a substitute for medical advice."
- Learning from vendors' own Reels: once the owner adds vendor Instagram handles under Metricool > Competitors, the weekly report reads their Reels' views, comments and interactions (IGCR fields) and the hourly watch notes which vendor topics pull engagement. Until then, use our own order data.

### News and trend hooks (owner, 31 Oct 2026)
Growth Watch reads the news and social trends twice a day and suggests how the next Reel can ride them, to reach new people and grow followers.
- **Look for:** Hyderabad and Telangana news and events (festivals and dates such as Karthika masam, Sankranti/Kanuma, Bonalu, Dasara, Ramzan, Christmas; weather like rain or a cold wave; big local events, cricket matches, long weekends, new metro or flyover openings in Jubilee Hills, Hitech City, Gachibowli, Kondapur, Marredpally, Secunderabad); food and health trends in India (millets, A2, protein, seasonal produce); what is trending in Indian food Reels (formats, audio, phrases); and what is getting attention on our own and vendors' accounts.
- **Use it as:** a hook line, a story angle, a timely caption question, an area name in the caption and hashtags (e.g. "Rainy evening in Hitech City? Natu kodi pulusu weather"), or a better posting time. The product and the weekly cadence still come from sales data; a trend changes the angle, not the product, unless a festival clearly favours another product (e.g. Ramzan → mutton and paya, Karthika masam → vegetarian staples and fruits, Sankranti → mutton, natu kodi and podis).
- **Never:** use tragedies, accidents, crime, disease outbreaks, politics, religion-based targeting or a celebrity's name or image; make health claims from news; copy another account's video, audio or script; claim we are part of an event. Food-safety scare stories are never used to frighten buyers.
- Every hook in "Live insights" carries its source link and date so the daily task can check it is still current (drop hooks older than 3 days).

### Competitor watch (chosen by the agents, not only Metricool; owner, 31 Oct 2026)
Research only: competitors are never named, shown, copied or compared in our Reels or captions. The agents keep this list current, adding a brand when it shows up in search, ads or news for our products in Hyderabad, and dropping one that no longer competes.
- **Fresh meat, Hyderabad (our 89% of orders):** Licious, FreshToHome, TenderCuts, Nandus, Sneha (Sneha Select), plus meat on Swiggy Instamart, Zepto and Blinkit.
- **Organic brands (pan-India and Hyderabad):** Organic India, Organic Tattva, 24 Mantra Organic, Two Brothers Organic Farms, Zama Organics, Organic Mandya, Akshayakalpa, The Organic World (Hyderabad stores).
- **Quick commerce and marketplaces:** Swiggy Instamart, Blinkit, Zepto, BigBasket, Amazon Fresh.
- **How to read them:** Metricool competitor data where the account is added (IGCO/IGCR fields); otherwise WebSearch/WebFetch for their latest campaigns, offers, festival pushes, new products, Reel and ad themes (news, ad-tracker pages, YouTube Shorts pages, their own sites), and public view/like/comment counts where a page shows them. Note what format, hook and offer drew attention, then turn it into our own original idea. Never copy their scripts, video, audio, claims or prices.
- Growth Watch checks 3–4 of these each morning (rotating so each is checked weekly) and writes useful findings to `insights/competitor_watch.csv` (date, brand, what they did, engagement if public, source URL, idea for us).

### Small vendors: grow their sales (owner, 31 Oct 2026)
69 vendors sell on our marketplace; 42 have only 1–10 orders, 9 have none, and 125 of 325 packaged products have never been ordered (site data 31 Oct; refresh with `python3 tools/site_sales.py --vendors`). Fresh food brings most of our buyers, so use that traffic to sell vendors' products:
- **Add-on line in every fresh-food Reel caption:** one vendor product that goes with the dish, with its link: mutton → Shevades Chicken/Mutton Masala (₹51); natu kodi → Rahasya groundnut oil or Yashoda mustard oil; vegetable box → ANIKA karam podis (₹60–65), Divyams heritage rice; Sunday lunch → Farmiya Govind Bhog rice; kids → Milletio millet bars (₹62), LazyMan jaggery peanut butter (₹160). Format: `➕ Goes well with: <product> by <vendor>, ₹<price> <link>`.
- **Vendor Spotlight (Tue/Thu) alternates** between one vendor (single best seller) and a **"Telugu kitchen basket"** story that features 3 small vendors' products together (e.g. ANIKA podi + Yashoda oil + Divyams rice), so more vendors get seen each week. Prefer vendors with 1–10 orders and products with wishlists or good ratings but few orders.
- **Collab posts:** when the owner records a vendor's Instagram handle in `insights/vendor_handles.csv` (vendor, handle, agreed yes/no), add it as `instagramData.collaborators` on that vendor's Reel only if agreed is yes. A collab shows the Reel to both audiences.
- **Vendor kit (owner sends):** after a vendor's Reel posts, the owner message includes the Reel link and a one-line ask for the vendor to share it, so their customers find our app.
- Track each featured vendor's orders before and after its Reel in `insights/reel_sales.csv`; keep featuring vendors whose sales move.

### Buyer feedback and follow-up (owner, 31 Oct 2026)
Customers write to the MyChatBot sales assistant ("Pureorganiczone Assistant", id 27598) on Instagram DMs and comments-to-DM, Messenger and WhatsApp. Growth Watch reads these chats to learn what buyers say and to bring warm buyers back to order.
- **Read:** `list_chats` for chats active since the last check, then `get_chat_messages` for each new one. Sort each into: buyer or interested shopper, existing customer feedback (praise or problem), vendor/seller, spam.
- **Learn:** log one row per chat in `insights/customer_feedback.csv` (date, chat_id, channel, type, product, what they said in ≤ 12 words, outcome). No names, phone numbers, emails, addresses or order numbers in the file. Themes (most-asked products, objections such as delivery area or price, praise words customers use) go into "Live insights" and shape Reel hooks and caption questions; a buyer's own words never appear in a Reel unless the owner says that customer agreed.
- **Follow up (one message, only where allowed):** to a person who asked about or started an order in the last 24 hours (Meta's messaging window for Instagram and Messenger), whose chat has no order confirmation or later reply, and who never said stop. Send once with `send_one_off_message` on the same channel: the product they asked about with its link, one add-on, the app and subscription line. Never more than one follow-up per person per 7 days, never to vendors, complaints or spam, never to anyone outside chats they started, and never between 10 PM and 8 AM.
- **Existing buyers who praise a product:** suggest the matching subscription or one related product in that same follow-up; tell the owner if they agreed to share their words.
- **Complaints and needs-operator chats:** never sell; message the owner at once with the chat link so a person replies.
- The assistant's replies are limited by the MyChatBot plan (trial until 9 Nov 2026 with about 100 AI replies); if replies run low, tell the owner.

### Win competitors' unhappy customers (owner, 31 Oct 2026)
Competitors' customers complain in public. Read those complaints in aggregate, then make sure our Reels, captions and the sales assistant answer exactly those pain points, so their unhappy buyers find us and switch.
- **Where to read (public pages only):** Google Maps and Google reviews of their Hyderabad stores and dark stores, App Store and Google Play reviews of their apps (Licious, FreshToHome, TenderCuts, Nandus, Sneha, Zama, The Organic World and others in "Competitor watch"), MouthShut, Trustpilot, Reddit (r/hyderabad, r/IndianFood), YouTube comments on their videos, and comments on their public Instagram/Facebook posts when a page shows them.
- **What to record:** themes only, never people. `insights/competitor_pain_points.csv` (date, brand, product type, pain point in ≤ 12 words, how often it appears, source URL, our answer). No names, handles, photos, phone numbers or quotes longer than a few words.
- **Typical pain points to look for:** meat not fresh or frozen, smell, bones/fat in boneless, small portions, late or missed slots, price hikes, fake "organic", no certificate, rude support, refund hassles, app bugs.
- **Turn each into our answer, only where it is true for us:** e.g. "cut fresh after you order" (only if the owner confirms), 60–90 min Hyderabad meat delivery, walk-in Madhapur store ("see it before you buy"), the 1-hour perishables refund window, a real person on WhatsApp 9704518572, subscriptions. Use them as Reel hooks and caption questions ("Ever got 'fresh' mutton that wasn't?"), as assistant objection answers, and as ad angles for the owner.
- **Never:** name, show or compare a competitor; quote or screenshot their reviews; contact, DM, tag, follow, comment on or reply to their customers or reviewers; post under their posts; create fake reviews or accounts; claim anything about them. People find us through our own Reels, search, ads and word of mouth.
- **Paid reach to competitors' shoppers (owner decides budget):** the weekly report recommends one Meta ad set built from the best pain-point Reel: (1) **store-radius targeting**: 1–2 km pins around competitors' Hyderabad stores, dark stores and meat shops found in "Competitor watch" (keep their addresses in `insights/competitor_locations.csv`: brand, area, address, source URL); (2) **interest targeting** with any competitor or category names Meta lists (check with the Adspirer search tool when actions are available); (3) later a **lookalike** of our consenting buyers. Scheduled runs never create ads.
- **Never identify individuals:** don't look up a reviewer's or commenter's profile, don't match people across sites, don't build lists of competitors' customers, and don't upload anyone's details to an ad platform unless they are our own customers who agreed to marketing.

### Our own feedback (owner, 31 Oct 2026)
Read what people say about us too, so problems are fixed fast and praise is reused (with permission).
- **Where:** product reviews and ratings on pureorganiczone.com (`tools/site_sales.py` gives counts and average rating; product pages show the text), App Store and Google Play reviews of the Pure Organic Zone app, Google reviews of the Madhapur store, comments on our own posts (Metricool and the sales-assistant chats), and vendor brands' product reviews on our site.
- **Log** themes in `insights/customer_feedback.csv` (no personal details). **Alert the owner at once** about any 1–2 star review or public complaint, with the link, so a person replies. Never auto-reply to public reviews. Praise becomes a Reel or caption idea only with the customer's permission.
- Feed recurring praise words ("fresh", "on time", "real natu kodi") into Reel hooks, and recurring complaints into "Live insights" for the owner to fix.

### Most-probable customer profiles (types of buyers, never named people; owner, 31 Oct 2026)
Each profile is an audience description for Meta/Google targeting and for choosing which Reel to boost there. Meta matches real people to it privately; we never see or collect names. Refine with weekly results.
| Profile | Areas (pins) | Age / interests for ads | Reels that match | Offer line |
|---|---|---|---|---|
| Premium meat families | Jubilee Hills, Banjara Hills, Film Nagar | 30–60; home cooking, fine dining, non-veg food | Festival mutton, Sunday-lunch stories, boneless/keema | 60–90 min delivery, weekly meat subscription |
| IT families, weekday rush | Hitech City, Gachibowli, Kondapur, Madhapur, Nanakramguda, Kokapet | 26–42; healthy eating, parenting, fitness | Natu kodi rainy-evening, veg box subscription, kids' millet snacks | App subscription, "set it once" veg box |
| Old-city and Secunderabad households | Marredpally, Secunderabad, Tarnaka, Malkajgiri | 35–60; Telugu food, family cooking | Taatha village stories, natu kodi, paya and head curry | WhatsApp ordering, next-day paya |
| Health-conscious professionals | Manikonda, Miyapur, Kukatpally, Begumpet | 28–50; organic food, yoga, Ayurveda | Ghee and oil traditions, millet and heritage-rice stories, vendor spotlights | Delivered all over India, app prices |
| Competitors' nearby shoppers | 1–2 km around competitors' stores in insights/competitor_locations.csv | 25–55; online grocery, meat delivery | The current best pain-point Reel | Fresh in 60–90 min, walk-in Madhapur store |
| Our warm audience | Instagram/Facebook engagers, site visitors (pixel) | any | The week's top Reel | App + subscription |
The weekly report names the best profile × Reel pair to boost and a budget; the owner approves. Daily Reels use the profile's area names in captions and hashtags so they also reach these people organically.

### Sales learning loop
`python3 tools/site_sales.py` snapshots order counts per product (public product fields only; the page also embeds seller account data, which must never be read, printed or stored). The change between snapshots = new orders. Compare the products a Reel promoted with their new orders over the next 48 h, and log it in `insights/reel_sales.csv` (date, reel slug, product, orders in the 48 h before, orders in the 48 h after). When the owner hands over real sales figures, add them to `insights/` and prefer them over this estimate.

## HeyGen AI-video Reels (fallback)
Connected through the HeyGen connector (account pureorganiczone@gmail.com, Creator plan, 600 premium credits a month, resetting on the 30th). One Reel costs about 13 credits (15 s 1080p video + voiceover, measured 30 Oct), so one a day fits. First example: `specs/2026-10-30_diabetes_swaps.json`.
1. Spec fields on top of the usual ones: `"format": "heygen"`, `heygen_prompt`, `voiceover`, `voice_id`, `cards`, `footage_map`.
   - `heygen_prompt`: vertical 9:16, warm natural light, 4 numbered shots (0–3 s, 3–6 s, 6–10 s, 10–15 s) of the actual foods, hands allowed, "no people's faces, absolutely no text, letters, logos or captions". Never show a competitor brand, a doctor, medicine or a hospital.
   - `voiceover`: 35–42 words (about 15 s at speed 1.1), same message as the cards. Health topics end with "Always follow your doctor's advice and medication."
   - `voice_id`: default Deirdre, `84bc506c91674034aa1d32e22903f627` (gentle, instructive). Keep one voice so the account sounds consistent.
2. Call `text_to_video` once with the prompt, `aspectRatio` "9:16", `duration` 15, `resolution` "1080p". Poll `get_model_video` every 30 s until completed.
3. Meanwhile call `create_speech_without_player` once with the voiceover, voice_id and `speed` 1.1. Use its word timestamps to set each card's `start`/`end` and the `footage_map` (each `[src_start, src_end, out_len]` slice plays sped up or slowed to out_len, so the rice shot sits under the rice line).
4. Download both files with curl into the scratchpad, then: `python3 tools/heygen_reel.py specs/<file>.json <footage.mp4> <voice.wav> reels/<same-name>.mp4`. All on-screen text, prices and the disclaimer are drawn by this tool, never by HeyGen. The tool also puts the company logo (`assets/logo.png`, on a white badge, y 215–487) on every frame, so cards must start at `top` 560 or lower; `tools/make_reel.sh` Reels carry the same logo badge.
5. Never regenerate to try alternatives. Only if the footage shows garbled text, a face, a logo or a deformed hand, generate once more with that fixed in the prompt; if it fails again, build with make_reel.sh instead and tell the owner.
6. After building, call `get_current_user` and put the remaining credits in the owner message.

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
- **App line in every caption (from 31 Oct 2026)**, just after the 🛒 line: `📱 Better prices on the Pure Organic Zone app (App Store & Google Play). Subscribe daily, weekly or monthly.` For Hyderabad fresh food also keep `📲 WhatsApp 9704518572`. Never invent a discount number or app-only price.

## Health and claims rules (strict)
- Describe nutrients and traditional use; never claim a food cures, treats or prevents a disease.
- Anything about diabetes, blood sugar, weight, BP or medicine ends with: "Always follow your doctor's advice and medication." (or "Not a substitute for medical advice.")
- Organic produce: say "grown without synthetic pesticides", not "chemical-free".
- Never invent certifications, farm names, founder stories, customer reviews or numbers.
- Never use competitors' videos, images, music or brand names in the Reel.

## Weekly report (Mondays)
Learn from **every connected network**, not only Instagram (owner, 31 Oct 2026). Pull the last 7 days of Instagram Reels metrics (IGRE01 date, IGRE03 content, IGRE11 reach, IGRE23 views, IGRE07 comments, IGRE12 saves, IGRE21 shares, IGRE08 engagement, IGRE27 retention), then for Facebook (reels/posts), YouTube (videos), LinkedIn (posts) and Pinterest (pins) call `getAnalyticsAvailableMetrics` once per network to find the date, text, reach/impressions, views, comments, shares and clicks fields, and pull those too. Add competitor metrics (IGCO02, IGCO07, IGCO10, IGCO12). Build one table per Reel with its numbers on each network, and name which network brings the most reach, comments and link clicks. Rank our Reels, name the top topic and format, compare with competitors' engagement, and write 2–3 concrete changes into the "Learnings" section below so daily runs use them.
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
- 31 Oct review (Instagram Reels, 25–30 Oct): owner's Hyderabad meat Reels lead by far: goat meat reach 305 / views 543, country chicken 220 / 394, vs ghee 67, millet noodles 60, pumpkin seeds 113, the rest 11–37. Comments were 0–2 on every Reel; saves highest on pumpkin seeds (16). So: meat and fresh-food story Reels keep Mon/Wed/Fri/Sun; every caption asks a memory/preference question to start comments; packaged products get a heritage story angle instead of a plain explainer.
- 31 Oct: owner switched every Reel to the narrated village story format ("Village story Reels") with the website + app + subscription call to action. First two: natu kodi (31 Oct 19:00) and festival mutton (1 Nov 09:00), both scheduled from chat to Instagram, Facebook and YouTube. Compare their reach and comments against the meat baseline above in the 2 Nov report.

## Live insights (written by the hourly Growth Watch; keep ≤ 12 lines, newest first)
- 31 Oct 23:00 NEXT REEL (Mon 2 Nov, spec 2026-11-02_millet_noodles.json, now "Ammamma's Weeknight Mutton Fry"): keep as written: goat boneless ₹589, 17:45, hook "Ever had a meat order cancelled or pushed to tomorrow? Ours reaches you in 60–90 min", add-on Shevades Chicken/Mutton Masala ₹51 (25 orders), areas Hitech City/Gachibowli/Kondapur, weather drier from 2 Nov. Caption question: "Mutton fry with rice or chapati?". From Tue 3 Nov, packaged slots lean to the Diwali gifting window (8 Nov) per the 17:00 note.
- 31 Oct 23:00 Natu kodi story (19:00): Metricool has no IG or FB rows for it yet at ~4 h, and older Reels' numbers are unchanged since 08:10, so Reel data is syncing about once a day; judge it at the 08:00 run (vs reach 120 and the owner's meat Reels 220–305). Site: 0 new orders since 17:09 (7,221 lines), country chicken unchanged. 1 Nov 09:00 mutton story still pending on IG, FB, YouTube.
- 31 Oct 20:00 Natu kodi story (post 411619492) published at 19:00 on IG, FB and YouTube (https://www.instagram.com/reel/DfKRUVPCrxf/); Metricool shows no metrics yet at ~1 h, so the 3 h check moves to the 23:00 run (judge vs reach 120). 1 Nov 09:00 mutton story still pending on the same 3 networks. Older Reels, site orders (0 new since 17:09) and reviews unchanged; no new shopper chats; assistant has 97 replies left (trial ends 9 Nov).
- 31 Oct 17:00 Correction: Deepavali is Sun 8 Nov (https://www.officeholidays.com/holidays/india/telangana/diwali), so 8 Nov is not a plain "last mutton Sunday before Karthika": make 2–7 Nov the Diwali gifting window (dry-fruit/seed combos, ghee for deepam and sweets, jaggery, til gud laddus) and lead 8 Nov with ghee + sweets + gift box. Only order movement today: Best Offer Deals Healthy Super Seeds & Nuts Combo ₹1,922, 1→3 order lines since 11:08 (no Reel behind it), a fit for a Diwali gift Reel. Reels, followers and other products unchanged; 2 new chats, neither a shopper ask. Tonight 19:00 natu kodi story: judge at 3 h (22:00) vs reach 120.
- 31 Oct 11:00 No change since 08:00: Reel metrics, followers and site orders identical (0 new orders); no new shopper chats. The A2 ghee comment-to-DM lead passed its 24 h window unanswered, so: on post captions with codes (PURE20), have the assistant quote the post's own price and ask for the order in the first reply. No public complaints; Android app has 0 ratings (994 installs): the app CTA in tonight's natu kodi story is the first real test.
- 31 Oct 08:00 NEXT REEL: Mon 2 Nov spec rewritten from millet noodles to "Ammamma's Weeknight Mutton Fry" (goat boneless ₹589, 17:45, add-on Shevades masala ₹51, hook "Ever had a meat order cancelled or pushed to tomorrow? Ours reaches you in 60–90 min", areas Hitech City/Gachibowli/Kondapur). Millet noodles go to a later slot.
- 31 Oct 08:00 Reels (IG reach at 20–68 h): veg box 37 (2 saves), diabetes kit 21, honey trial 11; all far below the 120 baseline. Facebook views are higher than IG (130 / 95 / 46); LinkedIn 10–12 impressions; Pinterest 0; YouTube returned no data. Followers 44,344 → 44,305 (28→29 Oct).
- 31 Oct 08:00 Tonight's natu kodi (19:00) and 1 Nov 09:00 mutton stories are scheduled to IG, FB and YouTube only (no LinkedIn or Pinterest, unlike the all-networks rule). Judge them at 3 h / 12 h against reach 120.
- 31 Oct 08:00 Top competitor pain point (meat apps): orders cancelled or moved to a later day, then refund hassles (Trustpilot FreshToHome 2.0/5, https://uk.trustpilot.com/review/freshtohome.com; Licious Google Play themes, https://kimola.com/reports/unveil-customer-insights-with-licious-feedback-analysis-report-google-play-en-in-156549). Our honest answer: 60–90 min Hyderabad delivery + a real person on WhatsApp. Second: fatty/smelly mutton: answer with "see it at our Madhapur store"; "cut fresh after you order" needs the owner's OK first.
- 31 Oct 08:00 Strongest hook: Karthika masam starts Tue 10 Nov (to 8 Dec); many Telugu families skip non-veg (https://hindutone.com/festivals/karthika-masam-2026-hyderabad-temples-deepam-timings/). Sun 1 Nov = "mutton before Karthika" (8 Nov is Deepavali, see 17:00); from 10 Nov swap meat slots to veg box subscription, ghee (deepam), podis and Telugu kitchen baskets.
- 31 Oct 08:00 Weather: evening thundershowers possible 31 Oct–1 Nov, drier from 2 Nov (https://www.theweek.in/news/india/2026/10/28/will-it-rain-in-hyderabad-tomorrow-imd-weather-update-for-telangana-mentions-thundershowers.html).
- 31 Oct 08:00 Buyers: 1 real shopper chat in 48 h (A2 ghee comment-to-DM, no reply after the price). Most chats are vendor/ops WhatsApp groups. Feed posts with discount codes (PURE20) pull DMs; the assistant answered with the ₹999 combo, not the post's ₹988 price.
