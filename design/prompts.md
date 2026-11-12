# Обкладинка, форзаци й зад книги — промпти для Nano Banana Pro

Рішення автора: усередині книги ілюстрацій немає. Картинки є лише на обкладинці, двох форзацах (внутрішніх сторонах обкладинки) і на задній обкладинці. Збірка (`python3 build/make_book.py`) сама підхоплює файли з `sources/art/book/`:

| Файл | Що це | Стан |
|---|---|---|
| `cover.jpg` | передня обкладинка | ✅ готово |
| `back.jpg` | задня обкладинка (поверх неї — анотація з `book/act1/annotation.md`) | ✅ готово |
| `map.png` | передній форзац: карта Чистилища (Акт 1) | необов'язково |
| `endpaper_back.png` | задній форзац: Сфера й The Point | необов'язково |

Якщо `back.png` ще немає, у книзі стоїть намальований кодом зад: нічне поле й анотація. Без `map.png` і `endpaper_back.png` форзаців просто немає.

## Як генерувати

- **Налаштування:** співвідношення **2:3**, роздільність **2K** (для карти краще **4K**).
- **Еталон стилю.** До кожного промпта прикріплюй готову обкладинку (`sources/art/book/cover.jpg`) і починай з рядка:

  > The attached image is the front cover of the same book: match its ink-and-charcoal technique, paper texture, lighting, checkerboard and color palette exactly, but do not copy its composition.

- **Без тексту.** Підписи на карті й форзаці я додам сам, українською й тим самим шрифтом, що в книзі. Тому в промптах прямо написано «no text». Якщо модель усе ж намалює літери, допиши: «Keep everything exactly the same, but remove all text, letters and labels.»
- **Краї.** Я обрізаю картинку під A5, тобто трохи зверху й знизу. Важливе тримай подалі від країв, приблизно на 5%.
- **Водяний знак.** Якщо в кутку з'явиться знак-зірочка, скажи мені, я приберу.

---

## `back.png` — задня обкладинка

Продовження передньої обкладинки: той самий світ, але порожніший і тихіший. Верхні 60% — темне небо під текст анотації.

```
The back cover of a dark literary novel, a direct continuation of the attached front cover: the same endless black-and-white checkerboard plain and the same low, heavy, motionless night clouds, but emptier and quieter. The upper 60% of the image must be calm, dark, almost empty sky with only faint soft clouds, because a block of printed text will be placed there.

In the lower part: the checkerboard stretches to a low horizon. A faint trail of footprints crosses the squares and leads away toward the horizon; in each footprint a tiny white flower has grown. Far in the distance, very small and barely visible at the edge of the darkness, a tiny figure with plum-violet hair stands and watches; the flowers nearest to her are crushed. No other figures, no tree.

Style: dark literary book illustration in ink and charcoal wash with fine cross-hatching and grainy paper texture, cinematic low-key lighting, restrained and melancholic. Palette: deep black, charcoal greys and bone white; the only colors are the small muted violet of the distant figure and a barely visible touch of deep crimson (#8E1B1F). The edges of the image fade softly into pure black.
There must be no text, no letters or numbers, no barcode, no logo, no watermark, no frame or border.
```

---

## `map.png` — передній форзац: карта Чистилища

Шлях Акту 1 знизу вгору: Клітинні поля → дорога (50 км) → поселення → тріснута біла дорога → палац під стовпом світла → установка розподілу в горі. Краї карти — невідомі землі.

```
A hand-drawn fantasy map for the front endpaper of a dark literary novel, in the style of the attached cover: ink and charcoal on aged, dark, grainy paper, drawn as an old explorer's map in an oblique bird's-eye view. Vertical composition. Keep important details away from the outer 5% of the image.

From bottom to top:
— At the bottom: the Cell Fields, a vast black-and-white checkerboard plain drawn in perspective, with low motionless clouds over it.
— A long winding road leads upward from the checkerboard; along the road the black and white squares gradually fade and "forget" themselves into pale grass and meadow. A thin dotted crimson line (#8E1B1F) marks the route along the whole road up to the palace.
— In the middle: a grey village made of mismatched houses from a thousand different worlds and eras (a medieval cottage, a concrete block, a pagoda, a wooden barn, a glass tower), all faded to the same grey, with a dry well in the center.
— Above it: a cracked white road leading up a hill to a white palace built by thought alone, with cracks running through its walls; a vertical pillar of light falls onto the palace from a round gap in the clouds above it, and a small blinding point of light shines in that gap. Beside the palace, a small enclosed garden with young trees.
— At the top, behind the palace: a great dark mountain with a colossal structure of seven concentric descending circular terraces carved into it, like a funnel, with a faint stream of tiny souls flowing into it.
— Around the edges the map dissolves into darkness and unexplored lands: at the upper left a snowy desert, at the right a dense jungle, at the lower left an ordinary forest, all drawn faintly and fading into black.

Leave a few small calm empty areas near each place and one larger empty area in the lower right corner, because labels and a title will be added there later.

Palette: bone white, charcoal greys and black; color only in the dotted crimson route (#8E1B1F) and a small touch of sprout green (#6F9A4A) in the palace garden. Decorations: a simple compass rose drawn as a small checkerboard square with a crimson diamond in the center.
There must be no text, no letters, no place names, no numbers, no labels, no legend text, no logo, no watermark.
```

**Якщо хочеш спробувати з написами одразу** (Nano Banana Pro непогано пише, але кирилиця може зіпсуватися), заміни останній рядок на:
```
Add hand-lettered place names in Ukrainian, in a classical serif hand, exactly as written: «Клітинні поля» at the checkerboard, «П'ятдесят кілометрів» along the road, «Поселення» at the village, «Палац» at the palace, «Сад світів» at the garden, «Установка розподілу» at the terraced mountain, «Снігова пустеля», «Джунглі», «Ліси» at the edges, and the title «Чистилище» in the lower right corner. No other text, no logo, no watermark.
```

---

## `endpaper_back.png` — задній форзац: Сфера й The Point (необов'язково)

Устрій світу з лору: Рай, Чистилище й Пекло разом утворюють Сферу. Вона обертається навколо The Point і завжди повернута до нього боком Раю.

```
A cosmological diagram for the back endpaper of a dark literary novel, in the style of the attached cover, drawn like an antique astronomical engraving in ink and charcoal on dark, grainy paper. Vertical composition. Keep important details away from the outer 5% of the image.

In the upper part of the image burns a small, blinding point of white light — a god without a body — with thin straight rays spreading from it. Below it, a great sphere slowly turns on a thin elliptical orbit drawn around the point. The sphere is divided into three layers: the side facing the point is brightly lit and pale (Paradise); the middle band is moderate grey with a tiny checkerboard pattern on its surface (Purgatory); the far side, turned away from the light, is the darkest black, with only faint red glimmers deep inside (Hell). Thin dotted lines show the rays reaching Paradise fully, Purgatory partly, and barely touching Hell. Around the composition, a delicate ring of tiny stars and faint orbital lines.

Leave small calm empty areas next to the point and next to each layer of the sphere, because labels will be added there later.

Palette: bone white, charcoal greys and black; color only in the faint crimson glimmers inside Hell (#8E1B1F).
There must be no text, no letters, no numbers, no labels, no symbols of real religions, no logo, no watermark.
```

---

Коли закинеш картинки, скажи мені. Я поставлю їх, на карту й форзац додам українські підписи (позиції — у `design/labels.json`), перезберу PDF і DOCX і перевірю, як усе лягло.
