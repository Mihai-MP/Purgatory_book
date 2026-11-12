# Ілюстрації до книги — промпти для Nano Banana Pro

Оформлення книги вже готове й без картинок: обкладинку, сторінки частин і орнаменти малює код (`build/art.py`). Ілюстрації його доповнять: збірка (`python3 build/make_book.py`) сама підхопить файли з `sources/art/book/` з назвами з таблиць нижче. Будь-якого файла може не бути — тоді на його місці лишиться поточне оформлення.

**Куди класти:** `sources/art/book/` (GitHub → *Add file → Upload files*, гілка `claude/hopeful-hopper-fazgqb`) або прикріпи в чат. Формат png або jpg.

## Як працювати з Nano Banana Pro

**Налаштування**
- **Співвідношення сторін:** **2:3** (вертикальне) для головних картинок, **1:1** для заставок розділів і кінцівки, **16:9** для аркуша персонажів.
- **Роздільність:** **2K** (можна 4K). Заставкам вистачить 1K.

**Промпти**
- Кожен промпт нижче — суцільний опис. Копіюй блок повністю, нічого не дописуючи: стиль, палітра і що не малювати вже всередині.
- Окремого поля для негативного промпта в Nano Banana Pro немає, тому заборони («no text…») вписані прямо в текст. Вирізати їх не треба: ця модель охоче малює написи.

**Однакові персонажі на всіх картинках (дуже раджу)**
1. **Крок 1.** Згенеруй аркуш персонажів, промпт `REF-1` нижче. Вибери вдалий варіант і збережи як `ref_characters.png`.
2. **Крок 2.** Згенеруй обкладинку (`cover.png`). Якщо стиль сподобався, вона стане еталоном стилю.
3. **Крок 3.** До кожної наступної картинки прикріплюй обидва файли й починай промпт з рядка:

   > Image 1 is the character reference sheet: keep each character's face, hair, eye color and clothing exactly as shown. Image 2 is the style reference: match its ink-and-charcoal technique, texture and color palette, but do not copy its composition.

   Аркуш файлом у книгу не піде, він потрібен лише для схожості персонажів.

**Виправлення в тому ж чаті** — пиши звичайними словами, наприклад:
- «Keep everything exactly the same, but remove all text and letters.»
- «Keep the composition, but make the top 40% of the image darker and emptier.»
- «Keep the scene, but make the figures smaller and seen from behind.»
- «Make the palette more monochrome: only black, greys, bone white, a little deep crimson and a little sprout green.»

**Водяний знак.** Якщо Gemini поставить у кутку видимий знак-зірочку, скажи мені, коли надсилатимеш файли. Я його приберу: краї картинки все одно йдуть у чорне.

## Що я задумав (коротко)

- **Мотив — Клітинні поля:** чорно-біла шахова дошка до обрію.
- **Кольори:** майже чорна ніч, сірі тони, кістяно-білий, **темно-червоний** (#8E1B1F: кров, блискавка) і **крапля зеленого** (#6F9A4A: паросток, сила творення, волосся Ріріки).
- **Місце для назви:** у головних картинках верхня частина спокійна й темна, бо поверх неї ляже назва.

---

## REF-1 — аркуш персонажів (16:9, 2K)

```
Create a character reference sheet for a dark literary novel, on a plain bone-white paper background, drawn in ink and charcoal wash with fine cross-hatching. Show five characters standing side by side, full body, front view, evenly spaced, neutral poses, same scale, no overlapping.

From left to right:
1) Niko — a slim young man about nineteen, messy black hair, pale skin, crimson-red eyes, a dark simple jacket over a light shirt, dark trousers; quiet, gentle, tired expression.
2) Rize — a slim seventeen-year-old girl with long blonde hair and delicate Japanese features, blue eyes, a plain grey dress and a worn jacket, a green cloth armband sewn tightly onto her left sleeve; guarded, proud expression.
3) Ririka — the same girl after death: identical face and build, but her hair is now a short green bob with one long lock covering her right eye; blue eyes; a white high-collared uniform-like coat with subtle gold details; restrained, sad expression.
4) Mimu — a small young servant girl with plum-violet hair, spade-shaped pupils, a small dot on her forehead and an unnervingly wide smile, wearing a dark red servant dress with gold trim.
5) The old god — an ancient, emaciated man with long white hair and blind white eyes, wearing a heavy golden crown and a long pale mantle, roots growing from his feet.

Palette: near-monochrome black, charcoal and bone white; color only in Niko's red eyes, Rize's green armband, Ririka's green hair, Mimu's violet hair and red dress, and the muted gold of the crown.
There must be no text, no names, no labels, no letters or numbers anywhere in the image, no watermark, no frame.
```

---

## Головні ілюстрації (2:3, 2K)

| Файл | Де стане в книзі |
|---|---|
| `cover.png` | обкладинка (назва зверху) |
| `prolog.png` | ліва сторінка навпроти початку Прологу |
| `part1.png` … `part6.png` | сторінки частин (назва частини зверху) |
| `end.png` | кінцівка книги (1:1) |

### `cover.png` — обкладинка
```
A full-page vertical cover illustration for a dark literary novel called Purgatory; the top part of the image will hold the printed title, so keep the upper 45% calm, dark and empty, with only soft low night clouds.

Scene: a vast black-and-white checkerboard plain stretches from the bottom of the frame to a distant horizon under low, heavy, motionless clouds; there is no wind and no shadow, everything is unnaturally still. Far away at the center of the horizon stands a lone sakura tree split in half from crown to roots by lightning: one half charred black and faintly smoking, the other still holding a few pale petals, and from the split grows a tiny bright green sprout. A single thin crimson lightning bolt hangs frozen in the air above the tree. Two small figures stand far away on the checkerboard holding hands, seen from behind: a slim young man with messy black hair and a slim girl with a short green bob.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, cinematic low-key lighting, restrained and melancholic, mature tone. Palette: deep black, charcoal greys and bone white; the only colors are deep crimson red (#8E1B1F) and a small touch of fresh sprout green (#6F9A4A). The edges of the image fade softly into pure black.
There must be no text, no title, no letters or numbers anywhere in the image, no logo, no watermark, no frame or border.
```

### `prolog.png` — «Ми стали пам'яттю»
```
A full-page vertical illustration for the prologue of a dark literary novel.

Scene: night, heavy endless rain at the edge of a forest. A blackened sakura trunk split in two by lightning stands in the middle ground; a thin, stubborn line of smoke still rises from the split despite the rain. Grey petals are trampled into the mud. Yellow police tape is stretched between wet bushes, and the flashing light of a distant patrol car turns the falling rain cold blue for an instant. In the foreground a closed black umbrella lies on a small, nameless mound of fresh earth. There are no people and no bodies in the image — only grief and emptiness.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, cinematic low-key lighting, restrained and melancholic. Palette: deep black, charcoal greys and bone white, with a touch of deep crimson (#8E1B1F) and a tiny touch of sprout green (#6F9A4A); the only exception is the cold police-light blue in the rain. The edges fade softly into pure black.
There must be no text, no letters or numbers, no signs, no logo, no watermark, no frame or border.
```

### `part1.png` — Частина перша. «Той день»
```
A full-page vertical illustration opening Part One of a dark literary novel; the part title will be printed at the top, so keep the upper 40% calm and dark — only heavy, gathering storm clouds.

Scene: the last sakura tree at the edge of an old sacred forest on the outskirts of a grey occupied city; a summer thunderstorm is gathering and the sky is low and violet-black. Two teenagers sit close together under the tree, seen from behind: a slim young man with messy black hair, and a slim girl with long blonde hair, her wrist bandaged, a green cloth armband on her sleeve. A phone in her hand glows faintly green. In the far background, the city skyline: identical five-story apartment blocks, loudspeakers on poles, giant portraits of a leader on the facades with indistinct faces. A black umbrella lies forgotten on the park path.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, cinematic low-key lighting, restrained and melancholic. Palette: deep black, charcoal greys and bone white; color only in a little deep crimson (#8E1B1F) and the small green of the armband and the phone glow (#6F9A4A). The edges fade softly into pure black.
There must be no text, no letters or numbers, no slogans on the portraits or buildings, no logo, no watermark, no frame or border.
```

### `part2.png` — Частина друга. «Клітинні поля»
```
A full-page vertical illustration opening Part Two of a dark literary novel; the part title will be printed at the top, so keep the upper 40% calm — only thin fog and low frozen clouds.

Scene: an endless black-and-white checkerboard plain under low, motionless clouds, thin fog drifting over it; no wind, no shadows, everything unnaturally still. A slim girl with long blonde hair stands holding a heavy, toy-like, plywood-looking pale-blue pistol in both trembling hands. A few steps away a slim young man with messy black hair lies fallen on the squares. Far behind them, at the edge of the fog, a tiny figure with plum-violet hair watches. Fragments of other worlds — a door, a broken chair, a piece of a staircase — hang motionless in the sky.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, cinematic low-key lighting, restrained, tense and melancholic. Palette: deep black, charcoal greys and bone white with a touch of deep crimson (#8E1B1F); the pistol is the only pale-blue object; the violet of the distant figure is small and muted. The edges fade softly into pure black.
There must be no text, no letters or numbers, no logo, no watermark, no frame or border.
```

### `part3.png` — Частина третя. «Дорога»
```
A full-page vertical illustration opening Part Three of a dark literary novel; the part title will be printed at the top, so keep the upper 45% calm — an empty pale-grey sky.

Scene: in the foreground the black-and-white checkerboard slowly "forgets" itself and fades into pale grass. Two figures walk away from us hand in hand along a long road toward a distant vertical pillar of light on the horizon: a slim young man with messy black hair and a slim girl with a short green bob. Small white flowers bloom in the young man's footprints behind him. Far behind them a small figure with plum-violet hair follows, and the white flowers are crushed under her shoes. On the horizon lies a grey village made of houses from a thousand different worlds and eras, all faded to the same grey.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, soft diffuse light, restrained and melancholic. Palette: charcoal greys, bone white and black; color only in the girl's green hair (#6F9A4A) and a small touch of deep crimson (#8E1B1F). The edges fade softly into pure black.
There must be no text, no letters or numbers, no road signs, no logo, no watermark, no frame or border.
```

### `part4.png` — Частина четверта. «Палац»
```
A full-page vertical illustration opening Part Four of a dark literary novel; the part title will be printed at the top, so keep the upper 40% calm — a dark vaulted ceiling.

Scene: a vast throne hall of a white palace built by thought alone; cracks run across the white stone walls and floor, and a vertical pillar of light falls through a gap in the ceiling. On the throne sits an ancient, emaciated god with long white hair and blind white eyes, fused into the throne by roots that spread across the floor, a heavy golden crown on his head. Before him stand two small figures seen from behind: a slim young man with messy black hair and a slim girl with a short green bob. To the side kneels a small servant girl with plum-violet hair, spade-shaped pupils and an unnervingly wide smile, in a dark red dress with gold trim. There are no mirrors anywhere in the hall.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, dramatic shaft of light, solemn and ominous. Palette: white stone, charcoal greys and black; color only in muted gold on the crown, the girl's green hair (#6F9A4A) and the servant's deep crimson dress (#8E1B1F). The edges fade softly into pure black.
There must be no text, no letters or numbers, no inscriptions, no logo, no watermark, no frame or border.
```

### `part5.png` — Частина п'ята. «Роки»
```
A full-page vertical illustration opening Part Five of a dark literary novel; the part title will be printed at the top, so keep the upper 40% calm — a quiet dusk sky.

Scene: a garden of worlds in a white palace courtyard at dusk; bare branches carry tiny new buds. A slim young man with messy black hair and crimson-red eyes kneels, holding a huge translucent flower bud the size of a human head; inside the bud are stars, oceans, mountains, tiny cities, the first fires and the first people praying. Beside him stands a slim girl with a short green bob, one lock covering her right eye, in a white high-collared coat with subtle gold details, her hand on his shoulder. A faint green light glows from the bud onto their faces.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, intimate low light, tender and melancholic. Palette: charcoal greys, bone white and black; color only in the soft green glow and green hair (#6F9A4A), the red eyes and a touch of deep crimson (#8E1B1F), and muted gold details. The edges fade softly into pure black.
There must be no text, no letters or numbers, no logo, no watermark, no frame or border.
```

### `part6.png` — Частина шоста. «Весілля»
```
A full-page vertical illustration opening Part Six of a dark literary novel; the part title will be printed at the top, so keep the upper 40% darker and calm — the shadowed upper part of a dome.

Scene: a wedding under a dome made of thousands of mirror shards that scatter soft points of light; the floor is a carpet of white flowers; on the empty throne only one last old root remains. The bride, a slim girl with a short green bob and one lock over her right eye, wears a simple white dress made from an old mantle; the groom, a slim young man with messy black hair and crimson-red eyes, stands facing her; they hold wooden rings with tiny living green sprouts. Quiet guests stand around them: maids in white, grey villagers, a man in shackles. At the edge a small servant girl with plum-violet hair claps, smiling too widely.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, soft scattered light, intimate, solemn and a little ominous. Palette: bone white, charcoal greys and black; color only in the green hair and sprouts (#6F9A4A), the red eyes and a touch of deep crimson (#8E1B1F), and the small muted violet of the servant. The edges fade softly into pure black.
There must be no text, no letters or numbers, no logo, no watermark, no frame or border.
```

### `end.png` — кінцівка (1:1, 1K)
```
A small square end vignette for a book, on a pure white background: a tiny green sprout (#6F9A4A) growing from a crack in a single black-and-white checkerboard tile, with one small drop of deep crimson (#8E1B1F) beside it. Black ink, minimal etching style, centered, with a lot of empty white space around it.
There must be no text, no letters or numbers, no logo, no watermark, no frame or border.
```

---

## Заставки розділів (необов'язково, 1:1, 1K)

Маленькі малюнки над назвою кожного розділу. Шаблон один, у дужках змінюється лише предмет. Для однакового вигляду прикріплюй першу вдалу заставку як еталон стилю для решти («Image 1 is the style reference: match its line, texture and amount of white space»).

```
A small square chapter vignette for a book, on a pure white background: [ПРЕДМЕТ]. Black ink in a minimal etching style with fine hatching, a single small accent of deep crimson (#8E1B1F), the object centered with a lot of empty white space around it.
There must be no text, no letters or numbers, no logo, no watermark, no frame or border.
```

| Файл | Розділ | [ПРЕДМЕТ] |
|---|---|---|
| `ch00.png` | Пролог | a closed black umbrella lying on a small mound of earth in the rain |
| `ch01.png` | 1. Промінь | a thin ray of morning sunlight crossing a bed, an envelope with money lying on the sheet |
| `ch02.png` | 2. Дубові двері | heavy old oak double doors taken from a ruined church, slightly ajar |
| `ch03.png` | 3. Старе дерево | an old tree with strangely bent branches and a black umbrella dropped on the path beneath it |
| `ch04.png` | 4. Сакура | a sakura branch in a storm with a lightning bolt behind it, and a phone with a glowing green button |
| `ch05.png` | 5. Убивця | a pistol lying on a single black-and-white checkerboard tile |
| `ch06.png` | 6. Синій пістолет | a toy-like pistol crumbling into pale-blue dust (pale blue is allowed here instead of crimson) |
| `ch07.png` | 7. Ріріка | an eye with a spade-shaped pupil, half hidden behind a strand of green hair |
| `ch08.png` | 8. П'ятдесят кілометрів | footprints in grass with small white flowers growing in them, one flower crushed |
| `ch09.png` | 9. Поселення | incense sticks smoking on a grey windowsill, a coiled rope beside them |
| `ch10.png` | 10. Під стовпом світла | a cracked white road leading toward a vertical pillar of light |
| `ch11.png` | 11. Він сам тебе просив | a bullet made of a single seed, lying in an open palm |
| `ch12.png` | 12. Уроки | seven concentric circles carved in stone and a small open chest of seeds |
| `ch13.png` | 13. Корона | a golden crown with roots growing from it and dust rising upward from it |
| `ch14.png` | 14. Біла мантія | scissors cutting a green cloth armband, a folded white high-collared mantle beside it |
| `ch15.png` | 15. Перший світ | a flower bud with stars and tiny mountains visible inside it |
| `ch16.png` | 16. Сакура вдруге | a young sakura sapling with its first blossoms and a single falling petal |
| `ch17.png` | 17. Весілля | two wooden rings with tiny living green sprouts and a mirror shard beside them |

---

Коли закинеш файли, скажи мені. Я перезберу PDF і DOCX і перевірю кадрування, читабельність назв і колір.
