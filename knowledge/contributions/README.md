# Contributing an Arabic Accent | المساهمة بلهجة عربية

<div dir="rtl">
أضف لهجتك هنا عن طريق إنشاء مجلد بالمحتوى الخاص بك.
</div>

Add your accent here by creating a folder with your content.

---

## Steps | الخطوات

### 1. Create a folder | أنشئ مجلداً

Use lowercase, no spaces | استخدم أحرف صغيرة، بدون مسافات:

```
knowledge/contributions/tunisian/
knowledge/contributions/yemeni/
knowledge/contributions/moroccan/
knowledge/contributions/iraqi/
```

### 2. Add `accent.json` | أضف ملف البيانات

```json
{
  "name": "Tunisian Arabic",
  "description": "Vocabulary and phrases for Tunisian dialect"
}
```

Or in Arabic | أو بالعربية:

```json
{
  "name": "اللهجة التونسية",
  "description": "مفردات وعبارات اللهجة التونسية"
}
```

### 3. Add your content | أضف محتواك

**Option A**: PDF files (`.pdf`) | ملفات PDF

**Option B**: Markdown file `content.md` | ملف Markdown

---

## Example structure | هيكل المثال

With PDFs | مع ملفات PDF:
```
knowledge/contributions/tunisian/
├── accent.json
├── vocabulary.pdf
└── phrases.pdf
```

With Markdown | مع Markdown:
```
knowledge/contributions/tunisian/
├── accent.json
└── content.md
```

---

## Content template | قالب المحتوى

Use this template for `content.md`:

```markdown
# اللهجة التونسية | Tunisian Arabic

## المفردات | Vocabulary

### باهي (behi)
**المعنى | Meaning:** Good, okay
**مثال | Example:** الحال باهي (Everything is good)

### شنوة (shnoua)
**المعنى | Meaning:** What
**مثال | Example:** شنوة تحب؟ (What do you want?)

## العبارات الشائعة | Common Phrases

| العبارة | Phrase | المعنى | Meaning |
|---------|--------|--------|---------|
| عسلامة | asslema | مرحبا | Hello |
| يعيشك | yaishek | شكرا | Thank you |
```

---

## Content guidelines | إرشادات المحتوى

- ✅ Include vocabulary with meanings | أضف مفردات مع معانيها
- ✅ Add example phrases | أضف عبارات أمثلة
- ✅ Use UTF-8 encoding | استخدم ترميز UTF-8
- ✅ Include transliteration (Latin letters) | أضف النطق بالحروف اللاتينية
- ✅ Provide both Arabic and English | وفر العربية والإنجليزية

---

## Then | ثم

Open a pull request! | افتح طلب سحب!

**Note**: PRs can ONLY add files to this folder. Changes to other files will be blocked.

**ملاحظة**: طلبات السحب يمكنها فقط إضافة ملفات لهذا المجلد. التغييرات على ملفات أخرى سيتم حظرها.
