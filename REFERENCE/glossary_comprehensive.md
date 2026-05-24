# Sound University — Comprehensive Glossary
*Audio engineering vocabulary mapped to Suno prompt behavior and classical Arabic poetry production.*

These terms describe what you **hear** — not what you measure. When you can name the exact problem in your generation, you know which word in your prompt to delete or replace. The Arabic translations are working labels, not formal acoustic definitions.

---

## 1. Spatial & Reverb Terms (The "Room" / الفضاء الصوتي)

*These terms describe the size, reflectivity, and echo character of the imaginary space the recording sits inside.*

---

- **Smeared / Washed Out (مشتت / غارق)**
  - **What you hear:** The vocal sounds distant, as if singing inside a cave. Sharp Arabic consonants (ق، ط، ك) lose their attack and blur into the next word. The poetic meter (الوزن) floats off-grid.
  - **Suno Cause:** Tags like `atmospheric`, `epic`, `cinematic`, `large hall`, or `ethereal`. Suno adds heavy reverb, pushing the vocal away from the center and smearing it across the stereo field.

- **Dry (جاف)**
  - **What you hear:** Zero echo. The singer sounds like they are standing three inches from your face in a padded room. You can hear breath and lip movement before the word even starts.
  - **Suno Cause:** Tags like `close-mic`, `dry studio vocal`, `dead room`, or `intimate`. Usually what you want for poetry to keep the lyrics pristine.

- **Reverb Tail (ذَيْل الصَّدى)**
  - **What you hear:** The fading echo that lingers after a sound stops — the "bloom" after the singer closes a syllable. In large spaces, this tail is long and overlaps the next word. In dead rooms, it vanishes instantly.
  - **Suno Cause:** Emerges from any genre recorded in large reflective spaces (orchestral, choral, ambient). The longer the tail, the more it swallows consonants at the end of poetic lines.

- **Room Tone / Ambience (نَبْرَة الغُرْفَة)**
  - **What you hear:** The subtle "breath" of the recording space itself — the difference between a recording that sounds like it happened somewhere versus one that sounds clinical. A stone cathedral has room tone. A padded studio has almost none.
  - **Suno Cause:** Genre memories carry room tone by default. `Gregorian chant` implies stone. `Raw singer-songwriter` implies a small wood room. `Telephone vocal` implies no room at all.

- **Stereo Width (الاتساع الصوتي)**
  - **What you hear:** How far left and right the instruments spread in your headphones. A narrow mix feels mono and centered. A wide mix feels like the instruments are surrounding you. Excessive width can push the vocal to the side and make it feel detached from the music.
  - **Suno Cause:** Large ensemble genres (orchestral, ambient, cinematic) default to wide stereo. Intimate genres (acoustic folk, sawt) default to narrow and centered.

---

## 2. Frequency & Weight Terms (The "Body" / جَسَد الصَّوْت)

*These terms describe the distribution of energy across low, mid, and high frequencies — the physical "weight" of the sound.*

---

- **Thin / Hollow (نَحِيف / خَافِت)**
  - **What you hear:** A male baritone sounds like a teenager, or like he is singing through an old telephone. The voice has no chest or gravity. The Arabic phrase لَا صَدْرَ فِيهِ captures it exactly.
  - **Suno Cause:** Missing energy in the 100–250 Hz range (chest resonance frequencies). Often triggered by lo-fi tags, vintage phonograph aesthetics, or genres historically recorded before bass-capturing microphones existed.

- **Muddy (غَائِم / مُوحَل)**
  - **What you hear:** A congested, woolly rumble. A thick blanket thrown over the speakers. The bass guitar, kick drum, and lower vocal register all blend into one indistinct mass. The poetic words dissolve in the noise.
  - **Suno Cause:** Too many instruments crowding the 100–400 Hz range simultaneously. Triggered by `heavy dark rock`, `dense psychedelic`, or `wall of sound` without a `sparse` counterweight.

- **Bright / Harsh (صَاخِب / حَادّ)**
  - **What you hear:** High frequencies that hurt at volume. Cymbals cut through. The letters س، ش، ت become piercing rather than crisp. At its worst it feels like a physical needle in the ear.
  - **Suno Cause:** Suno over-boosting the 4–8 kHz range to make the track sound "modern" and exciting. Triggered by `hyper-pop`, `commercial pop`, `over-compressed`, or `boosted highs`.

- **Sibilance (حِدَّة السِّين)**
  - **What you hear:** A specific subset of harshness — the hissing, whistling over-emphasis of consonants س، ش، ز، ص. It is the difference between a crisp Seen and one that sounds like it is slicing through the mix.
  - **Suno Cause:** The same genres that trigger harshness, but most acute when the vocal is over-compressed. In Arabic poetry, Verse 3 of Lesson 02 demonstrates this directly: `سِينُ الكَلَامِ وَشِينُهُ سَيْفاً`.

- **Warm (دَافِئ)**
  - **What you hear:** The pleasant opposite of thin and harsh simultaneously. The voice has chest resonance without being muddy. Instruments feel rounded at the edges rather than sharp. There is a sense of physical closeness and richness without weight.
  - **Suno Cause:** Genres historically recorded with tube microphones, close-mic placement, and minimal high-end boost. Triggered by `vintage`, `warm analog`, `acoustic tarab`, `intimate`, or `studio jazz`.

- **Bass-Heavy (ثَقِيل القَاع)**
  - **What you hear:** The low end dominates everything. The kick drum and bass guitar push air through your headphones, but the vocal floats on top of a rumble rather than sitting on a clear stage. A different problem from muddy — here the bass is powerful and defined, just too loud.
  - **Suno Cause:** Genres where low-end spectacle is the point: `trap`, `drill`, `deep house`, `dark techno`. Rarely a risk in Arabic poetry contexts unless sampling reference audio from these genres.

---

## 3. Separation & Dynamics Terms (The "Mix" / وُضُوح المَزِيج)

*These terms describe how well individual sounds — particularly the vocal — stand apart from each other in the mix.*

---

- **Buried / Masked (مَغْمُور / مَحْجُوب)**
  - **What you hear:** You know the singer is singing, but you are straining to understand the words. A guitar or synth is playing in the same frequency range as the voice, effectively erasing it from the foreground.
  - **Suno Cause:** Frequency masking — Suno placed a dense wall of instruments (guitars at 500 Hz–1 kHz) directly in front of the vocal. Fixed by `vocal-forward`, `sparse arrangement`, or structural `[Instrumental Break]` tags.

- **Punchy / Transient (حَاضِر / قَاطِع)**
  - **What you hear:** The exact opposite of buried. Drum hits crack sharply. The singer's consonants arrive at the ear with physical impact. Every syllable lands like a drumstick on a skin. The Arabic term نَبْض (pulse) captures this quality.
  - **Suno Cause:** Good dynamic range and minimal frequency overlap. Achieved by `clean production`, `staccato`, `minimalist arrangement`, `sparse`, `dry vocal-forward`.

- **Ducking (التَّرَاجُع الآلِي)**
  - **What you hear:** Instruments automatically grow quieter when the singer starts and return when the singer pauses. The vocal is always audible because the mix is breathing around it. You never have to choose between the voice and the band.
  - **Suno Cause:** Emerges naturally from `call and response`, `sparse`, `vocal-forward`, and `minimalist acoustic` genre memories. These genres require the instrument to step back for the human voice — it is built into their DNA.

- **Dynamic Range (المَدى الدِّينامِيكِي)**
  - **What you hear:** The distance between the softest and loudest moments in the track. High dynamic range means the quiet parts are genuinely quiet and the loud parts hit hard. Low dynamic range means everything is at the same volume — the track feels like a wall that never breathes.
  - **Suno Cause:** Overcompressed genres (modern pop, EDM, hyper-pop) crush dynamic range. Acoustic and classical genres preserve it. Khabab poetry with a punchy staccato prompt will have high dynamic range; the same poem in a wall-of-sound prompt will have none.

- **Compression (الضَّغْط الصَّوْتِي)**
  - **What you hear:** The automatic reduction of volume peaks. A compressed vocal stays at a consistent level — it never goes too quiet or too loud. Useful for intelligibility, but excess compression makes the vocal feel plastic, lifeless, and disconnected from the acoustic space.
  - **Suno Cause:** Modern pop genres use heavy compression by default. Triggered by `polished`, `radio-ready`, `commercial`, `over-produced`. Avoided by `raw`, `unplugged`, `live performance`, `acoustic`.

---

## 4. Vocal Timbre & Register Terms (The "Voice" / صَوْت المُغَنِّي)

*These terms describe the character of the human voice itself — its texture, weight, and physical quality — independent of the room or the instruments.*

---

- **Breathy (مُتَنَفِّس)**
  - **What you hear:** Air mixed visibly with the tone. The singer sounds like they are sighing into the microphone. Intimate and fragile. In Arabic poetry contexts, this is usually a failure mode — it reads as weak and undermines the authority of Fusha. In very dry, close-mic genres, it can sound accidentally intimate.
  - **Suno Cause:** Triggered by `ASMR`, `whispered`, `soft folk`, `bedroom pop`. A risk when using intimate genre anchors without a `clear enunciation` counterweight.

- **Chesty / Resonant (صَدْرِي / رَنَّان)**
  - **What you hear:** The positive opposite of مشكلة الصدر. The voice has gravity and physical presence. You feel it in your chest as much as you hear it in your ears. Baritone territory. In Arabic: صَوْتٌ لَهُ صَدْرٌ.
  - **Suno Cause:** Emerges from genres where a commanding, chest-driven male voice is structurally required: `theatrical`, `operatic`, `heroic`, `symphonic metal`, `stadium rock`, `choral`.

- **Nasal (أَنْفِي)**
  - **What you hear:** The tone resonates in the nasal cavity more than the chest. The singer sounds slightly congested. In Arabic, this is a particular risk when the genre gravity pulls toward Indian film music or certain pop styles — the voice loses its ground and starts floating.
  - **Suno Cause:** Can appear with `Bollywood`, `South Asian pop`, certain `flamenco` derivations. Not typically intentional in Arabic poetry production.

- **Silky / Smooth (نَاعِم / مَنْسَاب)**
  - **What you hear:** The voice moves between syllables with no rough edges. Transitions between notes are invisible. Pleasant in lyrical, romantic contexts. In classical Arabic prosody, excessive smoothness can erase the staccato boundary between feet (تفعيلات), making the meter sound blurred.
  - **Suno Cause:** Triggered by `romantic`, `R&B`, `smooth jazz`, `neo-soul`. A risk if used without a syllabic anchor like `strict enunciation` or `staccato`.

- **Airy / Heady (هَوَائِي / رَأْسِي)**
  - **What you hear:** The upper register of the voice, close to falsetto. Light, floating, ethereal. The opposite of chesty. In Arabic classical tradition this can approximate the upper reaches of Tarab ornaments, but without anchoring it sounds like the singer has no authority over the text.
  - **Suno Cause:** Triggered by `falsetto`, `ethereal`, `ambient pop`, `choir boy`. Rarely appropriate for Fusha unless deliberately combined with a strong rhythmic anchor.

- **Melismatic (مُلَحَّن / طَرَبِي)**
  - **What you hear:** Multiple notes sung on a single syllable — the Arabic Tarab tradition in its most extreme form. The vowel stretches and ornaments across several pitches before landing. When controlled, it is one of the most beautiful things Suno can produce with classical Arabic text. When uncontrolled, it distorts the meter beyond recognition.
  - **Suno Cause:** A free byproduct of `theatrical`, `operatic`, `tarab`, `maqam`, `Sufi chant`, `classical crossover`. Not easily summoned directly — it arrives when the genre DNA structurally requires it. Controlled by adding `strict syllabic enunciation` when you want less.

- **Declamatory / Strict (إِنْشَادِي / صَارِم)**
  - **What you hear:** Each syllable delivered as a distinct, equal-weight strike. No ornament, no vowel stretching. The meter lands exactly as written. Think of a military cadence or a Quranic recitation in a plain style. In Suno, this is the mode that best preserves the عروض (prosody).
  - **Suno Cause:** Triggered by `declamatory`, `strict syllabic enunciation`, `military march`, `spoken word`, `choral`, `Quranic recitation style`.

---

## 5. Rhythm & Time Terms (The "Grid" / الإِيقَاع وَالزَّمَن)

*These terms describe how the music relates to the pulse of time — whether it pushes forward, hangs back, or breaks the grid entirely.*

---

- **Driving (دَافِع)**
  - **What you hear:** The music leans into the beat with relentless forward momentum. Every element pushes you toward the next measure. In Arabic poetry this can work beautifully with fast meters (Khabab, Rajaz) but can overwhelm slow, meditative meters (Taweel, Basit).
  - **Suno Cause:** Triggered by `driving`, `energetic`, `uptempo`, `relentless`. Arrives naturally with `rock`, `blues rock`, `march`.

- **Laid-Back / Relaxed (مُتَرَاخٍ)**
  - **What you hear:** The singer and instruments sit slightly *behind* the beat rather than on top of it. There is a sense of ease and unhurriedness. Common in soul and blues traditions. In Arabic contexts this can accidentally sound like dialectal drift — the meter appears to lose its grip.
  - **Suno Cause:** Triggered by `relaxed`, `slow blues`, `soul`, `groove-based`. A risk when using these genres without a `strict syllabic` anchor.

- **Tight (مُحْكَم)**
  - **What you hear:** Every element lands exactly on the beat with machine precision. No swing, no delay. The meter of the poetry and the pulse of the music coincide perfectly. This is what a good Khabab generation should feel like.
  - **Suno Cause:** Triggered by `tight`, `precise`, `quantized`, `staccato`, `percussive`, `minimalist acoustic`.

- **Groove / Pocket (النَّبْضَة / الجَيْب الإِيقَاعِي)**
  - **What you hear:** The feeling that the music is alive and breathing — the players are slightly humanizing the beat in a way that makes your head nod involuntarily. Not the same as laid-back; groove is controlled while laid-back is loose.
  - **Suno Cause:** Emerges from genres built on live performance memory: `blues`, `funk`, `Afrobeat`, `traditional percussion`. Difficult to force directly — it is a byproduct of certain genre DNA.

- **Syncopation (التَّنَاوُب الإِيقَاعِي)**
  - **What you hear:** Emphasis placed on the *off* beats — the spaces between the main pulse — rather than the main pulse itself. Western pop and jazz rely heavily on this. It is structurally incompatible with Arabic classical prosody, which places weight on the تفعيلة feet. When Suno applies Western syncopation to a classical Arabic poem, the meter sounds broken.
  - **Suno Cause:** The default tendency of most Western genres. Reduced by `strict syllabic enunciation`, `declamatory`, `staccato`, and Arabic genre anchors.

- **Staccato (مُقَطَّع)**
  - **What you hear:** Notes cut short, with silence between them. Each sound is a separate, detached strike. In Arabic poetry, staccato is the sound of the prosodic foot landing clearly. The Khabab meter (طَقْ طَقْ طَقْ طَقْ) is the most naturally staccato meter in Arabic.
  - **Suno Cause:** Triggered directly by `staccato`, `punchy`, `percussive`. Naturally present in `unplugged folk`, `traditional percussion`, `desert blues`.

- **Legato (مُتَّصِل / مُنْسَاب)**
  - **What you hear:** Sounds flow smoothly from one to the next with no break or silence between them. The opposite of staccato. In Arabic poetry, legato is appropriate for slow, meditative meters but is a failure mode for fast, percussive ones — it dissolves the foot boundaries.
  - **Suno Cause:** Triggered by `smooth`, `flowing`, `ethereal`, `ambient`, `ballad`, `tarab` (when uncontrolled).

- **Rubato (حُرِّية الإِيقَاع)**
  - **What you hear:** Freedom from the strict pulse. The singer stretches and contracts the timing expressively — speeding up through a phrase, then pulling back dramatically at the climax. Beautiful in improvised Mawwal or classical Tarab. Dangerous in a Suno generation because it can cause the AI to lose track of where the meter is.
  - **Suno Cause:** Triggered by `expressive`, `free-time`, `mawwal`, `classical tarab`, `Sufi improvisation`. Only appropriate when you are not relying on the prosodic grid to carry the track.

- **Tempo Mismatch (تَضَارُب الإِيقَاع)**
  - **What you hear:** The speed of the music is structurally incompatible with the speed of the Arabic meter. A 140 BPM Hard Rock track will try to make the Kamil meter march at rock speed — forcing the singer to either rush the syllables into slurs or stall unnaturally between lines.
  - **Suno Cause:** Uploading a high-BPM Western audio reference, or using genre DNA (rock, punk, EDM) whose default tempo exceeds what the Arabic meter can sustain. Fixed by adding `mid-tempo`, `measured`, `deliberate` to the style field.

---

## 6. Tonal & Modal Color Terms (The "Color" / اللَّوْن الصَّوْتِي)

*These terms describe the emotional and tonal character of the music — the feeling a scale, mode, or harmony creates before a single word is sung.*

---

- **Dark (دَاكِن)**
  - **What you hear:** A heavy, minor, downward-leaning tonal character. The music feels like it is pulling you underground. In Arabic music, darkness comes from specific Maqamat — particularly Saba and Kurd — and from descending melodic phrases.
  - **Suno Cause:** Triggered by `dark`, `minor key`, `ominous`, `doom`, `melancholic`. In Arabic context, arrives naturally with `Maqam Saba` or `Sufi lament`.

- **Haunting / Eerie (مُسَكَّن / وَحْشِي)**
  - **What you hear:** Unresolved, suspended tones that create a sense of incompleteness. The music feels like a question that refuses to answer itself. Related to dark, but where dark is heavy, haunting is weightless and unsettling.
  - **Suno Cause:** Triggered by `haunting`, `ethereal`, `ambient`, `sparse`, `unresolved`. Often a byproduct of large reverb spaces that swallow the ending consonants.

- **Exotic / Orientalist (شَرْقِي / مُثِير)**
  - **What you hear:** The use of augmented second intervals (the characteristic interval of Maqam Hijaz and related modes) that signal "Middle Eastern" to Western ears. This is a double-edged term — it can anchor Suno beautifully to Arabic tonal memory, or it can produce a cartoonish "Aladdin" result.
  - **Suno Cause:** Triggered by `Middle Eastern`, `Arabian`, `Oud scale`, `Hijaz mode`, `desert`. Use cautiously — always pair with a specific tradition anchor.

- **Modal (مَقَامِي)**
  - **What you hear:** Music built on a mode or Maqam rather than the simple major/minor Western system. The scale has a specific "flavor" that cannot be reduced to happy or sad. Each Maqam has an emotional personality in Arabic tradition: Bayati (yearning), Hijaz (desert longing), Rast (balanced, noble), Saba (grief), Kurd (intimate, close).
  - **Suno Cause:** Triggered by `maqam [name]`, `Arabic mode`, `Persian modal`, `Andalusian`. Suno's memory of specific Maqamat is uneven — Hijaz is strongest, Saba is weakest.

- **Resolved / Consonant (مُتَنَاغِم)**
  - **What you hear:** The music lands on its home note with a sense of arrival and completion. In poetry production, a resolved ending makes the final couplet feel like a conclusion rather than a fragment.
  - **Suno Cause:** Structural tags like `[Outro]` push Suno toward resolution. Genre memories of sonata form and song structure also encourage it. Tarab genres tend to resist resolution — they prefer the suspended longing.

- **Dissonant (نَشَاز)**
  - **What you hear:** Clashing notes that create tension or unease. Not necessarily wrong — classical and jazz traditions use dissonance deliberately. In Suno Arabic poetry contexts, unintended dissonance usually means the AI has lost track of the Maqam and is using two incompatible tonal systems simultaneously.
  - **Suno Cause:** Triggered by `avant-garde`, `atonal`, `experimental`. Occurs accidentally when Western and Arabic tonal systems collide in the same generation.

- **Bright Tonal / Luminous (مُضِيء — لوني، لا ترددي)**
  - **What you hear:** A major-key, upward-lifting tonal character. The music feels like morning or triumph. Different from *Bright* in the frequency sense — this is about mood and scale, not harshness. Maqam Rast sits here.
  - **Suno Cause:** Triggered by `major key`, `triumphant`, `heroic`, `uplifting`. In Arabic context, arrives with `Maqam Rast`, `nasheed`, `celebratory`.

---

## 7. Arrangement & Structure Terms (The "Architecture" / البِنْيَة المُوسِيقِيَّة)

*These terms describe how instruments are layered, how density changes over time, and how the vocal and instruments relate to each other structurally.*

---

- **Sparse (مُتَفَرِّق / خَفِيف)**
  - **What you hear:** Few instruments, with audible space between each sound. The silence between notes is part of the arrangement. The vocal has room to breathe and every word lands clearly. This is the single most reliable tag for protecting Fusha intelligibility.
  - **Suno Cause:** Triggered directly by `sparse`, `minimal`, `stripped`, `solo instrument`. Naturally present in `unplugged folk`, `solo oud`, `traditional sawt`.

- **Lush / Dense (مُكْتَنِز / كَثِيف)**
  - **What you hear:** Many instruments playing simultaneously, filling every frequency band. The music feels rich and orchestral but the vocal must fight for space. Beautiful in instrumental passages — dangerous during verses.
  - **Suno Cause:** Triggered by `orchestral`, `lush`, `full arrangement`, `symphonic`, `wall of sound`.

- **Call and Response / Lazma (اللَّزْمَة / الصَّدى والجَوَاب)**
  - **What you hear:** The singer delivers a line. An instrument answers in the silence that follows. The vocal and the instrument have a conversation. In Arabic music tradition this is the Lazma — the instrumental hook between vocal phrases. It is one of the most natural ways to use Western instruments alongside classical Arabic lyrics without collision.
  - **Suno Cause:** Triggered by `call and response`, `call and response lazma`, `blues structure`, `desert blues`. The term `Tarab` can also trigger this but pulls the genre harder toward Arabic tradition.

- **Build-Up (تَصَاعُد)**
  - **What you hear:** The music grows progressively more dense, louder, and more intense as it moves toward a climax. Instruments are added layer by layer. In poetry production, a build-up before the Chorus gives the resolution more emotional weight.
  - **Suno Cause:** Structural tags (`[Verse]` → `[Chorus]`) naturally encourage this. Reinforced by `crescendo`, `building intensity`, `epic scale`.

- **Breakdown (تَفْكِيك / تَهْدِئَة)**
  - **What you hear:** The music strips back suddenly — often to a single instrument or voice alone. The contrast with what came before is the point. After a dense verse, a breakdown makes the next entry feel like a restart.
  - **Suno Cause:** Triggered by structural `[Bridge]` tags, `stripped`, `bare`, `solo vocal`. In rock and electronic genres, breakdowns are part of the DNA.

- **Wall of Sound (جِدَار الصَّوْت)**
  - **What you hear:** Every frequency band is filled simultaneously with layered instruments — guitars, strings, percussion, vocals, pads — all playing at once. The effect is overwhelming and immersive. The vocal is either buried inside the wall or floats just above it. Never used for intelligibility — only for sonic spectacle.
  - **Suno Cause:** Triggered by `wall of sound`, `shoegaze`, `dense`, `layered production`, `symphonic`. The deliberate choice for مشكلة الصوف demonstrations.

- **Monophonic / Solo (أُحَادِي / مُنْفَرِد)**
  - **What you hear:** A single melodic line with no harmony or accompaniment. The voice alone, or a single instrument. The oldest form of music. In Arabic poetry contexts, a monophonic generation strips away all acoustic complexity and exposes the prosody with surgical clarity.
  - **Suno Cause:** Triggered by `solo vocal`, `a cappella`, `unaccompanied`, `solo oud`. Difficult to sustain for a full Suno track — usually emerges in intro or outro sections.

---

## Diagnostic Framework: How to Name Your Problem

When you listen to a generation you do not like, work through these seven questions in order. The first answer that fits is your problem.

| # | Question | If yes, your problem is in... |
|---|---|---|
| 1 | Does the vocal sound distant, echoey, or lost in space? | **The Room** (Spatial) |
| 2 | Does the vocal sound thin/hollow OR muddy/heavy OR painfully sharp? | **The Body** (Frequency) |
| 3 | Can you hear the singer but cannot understand the words? | **The Mix** (Separation) |
| 4 | Is the vocal texture wrong — too breathy, nasal, airy, or not chesty enough? | **The Voice** (Timbre) |
| 5 | Is the rhythm fighting the meter — rushing, dragging, or off the grid? | **The Grid** (Rhythm) |
| 6 | Does the musical mood feel wrong — too dark, too bright, tonally alien? | **The Color** (Tonal) |
| 7 | Are the instruments not giving way to the vocal, or is the structure wrong? | **The Architecture** (Arrangement) |

Once you name the dimension, you know which section of this glossary to consult — and which prompt words to change.
