# Ілюстрації до книги — промпти для генератора

Оформлення книги вже готове й без картинок: обкладинка, сторінки частин і орнаменти намальовані кодом (`build/art.py`). Ілюстрації його доповнять: збірка (`python3 build/make_book.py`) сама підхопить файли з `sources/art/book/` з назвами, як у таблиці нижче. Будь-якого файла може не бути — тоді лишиться поточне оформлення.

**Куди класти:** `sources/art/book/` (через GitHub: *Add file → Upload files*, у гілку `claude/hopeful-hopper-fazgqb`) або прикріпи в чат. Формати: png, jpg або webp.

## Мова оформлення (щоб ти розумів, що я задумав)

- **Мотив — Клітинні поля:** чорно-біла шахова дошка до обрію. Це перше, що бачать Ніко й Різе після смерті.
- **Кольори:** ніч (майже чорний), кістяно-білий, **темно-червоний** (кров, блискавка, акцент тексту) і **крапля зеленого** (паросток: колір сили творення й волосся Ріріки). Усе інше — сірі тони.
- **Обкладинка (зараз):** назва над нічним полем, у центрі на обрії червона блискавка влучає в маленький зелений паросток.
- **Сторінки частин:** чорні, з полем, що тоне в темряві. Ілюстрації частин стануть на їхнє місце.

## Загальні правила для кожної картинки

**Формат:** вертикальний 2:3, щонайменше 2000 × 3000 px (я обріжу під A5). Заставки розділів — квадрат 1:1, від 1024 px.

**Стиль** — додавай у кінець кожного промпта:

```
Style: dark literary book illustration, ink and charcoal wash with fine cross-hatching and grainy paper texture, cinematic low-key lighting, restrained and melancholic, mature tone. Near-monochrome palette: deep black, charcoal greys, bone white; the only colors are deep crimson red (#8E1B1F) and small touches of fresh sprout green (#6F9A4A). Edges of the image fade softly into pure black (#0B0B0D). No text, no letters, no logo, no watermark, no signature, no frame or border.
```

**Негативний промпт** (якщо генератор його має):

```
text, letters, captions, watermark, logo, signature, frame, border, bright saturated colors, cute chibi style, glossy 3D render, extra fingers, deformed hands, duplicated faces
```

**Якщо хочеш ближче до своїх артів**, заміни першу частину стилю на `Style: dark anime/manga illustration with clean ink lines and muted cel shading, …`, а палітру й решту лиши як є.

**Персонажі** — вставляй ці описи без змін, щоб персонажі були однакові на всіх картинках:

- **NIKO:** `a young man about 19, slim, messy black hair, pale skin, dark simple jacket over a shirt` (з частини 4 додавай `crimson-red eyes`).
- **RIZE (до смерті):** `a slim 17-year-old girl with long blonde hair and delicate Japanese features, a green cloth armband sewn onto her sleeve`.
- **RIRIKA (у Чистилищі):** `a slim 17-year-old girl with a short green bob, one lock of hair covering her right eye, blue eyes` (з частини 5 додавай `white high-collared uniform with gold details`).
- **MIMU:** `a small young servant girl with plum-violet hair, spade-shaped pupils, a dot on her forehead, an unnervingly wide smile, dark red servant dress with gold trim`.
- **OLD GOD:** `an ancient emaciated god fused into his throne by roots, blind white eyes, a heavy golden crown`.

Порада: фігури краще давати дрібно, зі спини або в профіль. Так генератор менше псує обличчя, і персонажі виходять схожими між собою.

---

## Головні ілюстрації

У верхній третині/половині (де вказано) — тихе темне місце: там буде назва. Не став туди нічого важливого.

| Файл | Де стане в книзі |
|---|---|
| `cover.png` | обкладинка (замість намальованого поля; назва зверху) |
| `prolog.png` | ліва сторінка навпроти початку Прологу |
| `part1.png` … `part6.png` | сторінки частин (назва частини зверху) |
| `end.png` | маленька кінцівка в кінці книги (квадрат) |

### `cover.png` — обкладинка
```
Vertical book cover illustration. A vast black-and-white checkerboard plain stretching to a distant horizon under low, heavy, motionless night clouds. Far away in the center, on the horizon, a lone sakura tree split in half from crown to roots by lightning: one half charred black and faintly smoking, the other still holding a few pale petals; from the split grows a tiny bright green sprout. A single thin crimson lightning bolt hangs frozen in the air above the tree. Two small figures stand far away on the checkerboard holding hands, seen from behind: NIKO and RIRIKA. The upper 45% of the image is calm empty dark sky with soft clouds, reserved for the title.
```

### `prolog.png` — «Ми стали пам'яттю»
```
Night, heavy endless rain at the edge of a forest. A blackened sakura trunk split in two by lightning, a thin stubborn line of smoke rising from the split despite the rain; grey petals trampled into the mud. Yellow police tape stretched between wet bushes, the flashing light of a patrol car turning the falling rain cold blue for an instant. In the foreground, a closed black umbrella lies on a small, nameless mound of fresh earth. No people, no bodies. Quiet, grief, emptiness. (Exception to the palette: cold police-light blue is allowed.)
```

### `part1.png` — Частина перша. «Той день»
```
The last sakura tree at the edge of an old sacred forest on the outskirts of a grey occupied city; a summer thunderstorm is gathering, the sky low and violet-black. Two teenagers sit close together under the tree, seen from behind: NIKO and RIZE (before death), her wrist bandaged. A phone in her hand glows faintly green. In the far background the city skyline: identical five-story blocks, loudspeakers on poles, giant portraits of a leader on facades (faces indistinct). A black umbrella lies forgotten on the park path. Upper 40% — storm clouds, calm and dark, reserved for the title.
```

### `part2.png` — Частина друга. «Клітинні поля»
```
An endless black-and-white checkerboard plain under low, frozen clouds; no wind, no shadows, everything unnaturally still, thin fog. A girl, RIZE, stands holding a heavy, toy-like, plywood-looking pale-blue pistol in both trembling hands. A few steps away a young man, NIKO, lies fallen on the squares. Far behind, at the edge of the fog, a tiny figure with plum-violet hair watches. Fragments of other worlds — a door, a broken chair, a piece of a staircase — hang motionless in the sky. Upper 40% — calm fog and clouds, reserved for the title. (Exception: the pistol is pale blue.)
```

### `part3.png` — Частина третя. «Дорога»
```
The checkerboard slowly "forgets" itself into grass: in the foreground the black and white squares fade into a pale meadow. Two figures walk away from us hand in hand along a long road toward a distant vertical pillar of light on the horizon: NIKO and RIRIKA (green bob). Small white flowers bloom in NIKO's footprints behind him. Far behind them a small violet-haired figure follows, and the white flowers are crushed under her shoes. On the horizon, a grey village made of houses from a thousand different worlds, all faded to grey. Upper 45% — empty pale-grey sky, reserved for the title.
```

### `part4.png` — Частина четверта. «Палац»
```
A vast throne hall of a white palace built by thought alone, cracks running across the white stone walls and floor; a vertical pillar of light falls through a gap in the ceiling and clouds. On the throne sits the OLD GOD, fused into it by roots that spread across the floor. Before him stand NIKO and RIRIKA, small figures seen from behind. To the side kneels MIMU, smiling too widely. There are no mirrors anywhere. Muted gold only on the crown. Upper 40% — dark vaulted ceiling, calm, reserved for the title.
```

### `part5.png` — Частина п'ята. «Роки»
```
A garden of worlds in a white palace courtyard at dusk, bare branches with tiny new buds. NIKO (crimson-red eyes) kneels holding a huge translucent flower bud the size of a human head; inside the bud: stars, oceans, mountains, tiny cities, the first fires, the first people praying. Beside him stands RIRIKA in a white high-collared uniform with gold details, her hand on his shoulder, one lock of hair over her right eye. Faint green light from the bud. Upper 40% — calm dusk sky, reserved for the title.
```

### `part6.png` — Частина шоста. «Весілля»
```
A wedding under a dome made of thousands of mirror shards scattering soft light; the floor is a carpet of white flowers; on the throne only one last old root remains. The bride RIRIKA in a simple white dress, the groom NIKO with crimson-red eyes; they hold wooden rings with tiny living green sprouts. Quiet guests: maids in white, grey villagers, a man in shackles. At the edge MIMU claps, smiling too wide. Intimate, solemn, a little ominous. Upper 40% — the mirror dome, darker, reserved for the title.
```

### `end.png` — кінцівка (квадрат 1:1, на білому)
```
Small square vignette: a tiny green sprout growing from a crack in a single black-and-white checkerboard tile, one small drop of crimson beside it. Black ink on pure white background, minimal, lots of empty white space, centered. No text.
```

---

## Заставки розділів (необов'язково, 18 штук)

Маленькі квадратні малюнки над назвою кожного розділу. Для всіх — один шаблон, змінюється лише предмет:

```
Small square chapter vignette: [ПРЕДМЕТ]. Black ink on pure white background, minimal etching style, a single small crimson accent, centered, lots of empty white space around. No text, no frame.
```

| Файл | Розділ | [ПРЕДМЕТ] |
|---|---|---|
| `ch00.png` | Пролог | a closed black umbrella lying on a small mound of earth in the rain |
| `ch01.png` | 1. Промінь | a thin ray of morning sunlight crossing a bed, an envelope with money on the sheet |
| `ch02.png` | 2. Дубові двері | heavy old oak double doors taken from a ruined church, slightly ajar |
| `ch03.png` | 3. Старе дерево | an old tree with strangely bent branches, a black umbrella dropped on the path beneath it |
| `ch04.png` | 4. Сакура | a sakura branch in a storm, a lightning bolt behind it, a phone with a glowing green button |
| `ch05.png` | 5. Убивця | a pistol lying on a single black-and-white checkerboard tile |
| `ch06.png` | 6. Синій пістолет | a toy-like pistol crumbling into blue dust (the only pale-blue element) |
| `ch07.png` | 7. Ріріка | an eye with a spade-shaped pupil, half hidden by a strand of green hair |
| `ch08.png` | 8. П'ятдесят кілометрів | footprints in grass, small white flowers growing in them, one flower crushed |
| `ch09.png` | 9. Поселення | incense sticks smoking on a grey windowsill, a rope coiled beside them |
| `ch10.png` | 10. Під стовпом світла | a cracked white road leading to a vertical pillar of light |
| `ch11.png` | 11. Він сам тебе просив | a bullet made of a single seed, lying in an open palm |
| `ch12.png` | 12. Уроки | seven concentric circles carved in stone, a small open chest of seeds |
| `ch13.png` | 13. Корона | a golden crown with roots growing from it, dust rising upward from it |
| `ch14.png` | 14. Біла мантія | scissors cutting a green cloth armband, a folded white high-collared mantle |
| `ch15.png` | 15. Перший світ | a flower bud with stars and tiny mountains visible inside it |
| `ch16.png` | 16. Сакура вдруге | a young sakura sapling with its first blossoms, a single petal falling |
| `ch17.png` | 17. Весілля | two wooden rings with tiny living green sprouts, a mirror shard beside them |

---

Коли закинеш файли, скажи мені. Я перезберу PDF і DOCX і перевірю, як усе лягло: кадрування, читабельність назв і чи не вибивається колір.
