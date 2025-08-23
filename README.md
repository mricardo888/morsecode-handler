Got it 👍 — you want the README to be **friendly and user-facing**, not just for developers.
Here’s a polished **audience-facing `README.md`** for GitHub / PyPI:

---

# 📡 morsecode

Easily **encode and decode Morse code** in Python 🐍.
This library is simple, lightweight, and includes both a **Python API** and a **Command-Line Interface (CLI)**.

✅ Learn Morse code
✅ Encode secret messages
✅ Use it in scripts, projects, or just for fun

---

## 🚀 Installation

Install from [PyPI](https://pypi.org/project/morsecode/):

```bash
pip install morsecode
```

---

## 🛠️ Usage in Python

```python
import morsecode

# Encode text
encoded = morsecode.encode("HELLO WORLD")
print(encoded)
# .... . .-.. .-.. --- / .-- --- .-. .-.. -..

# Decode Morse back to text
decoded = morsecode.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
print(decoded)
# HELLO WORLD
```

### Lenient Mode (skip unknown characters)

```python
import morsecode
morsecode.encode("HELLO 🙂", strict=False, unknown="?")
# .... . .-.. .-.. --- / ?
```

---

## 💻 Command Line Tool

Once installed, you also get the `morsecode` CLI:

```bash
# Encode
morsecode encode "HELLO WORLD"
# .... . .-.. .-.. --- / .-- --- .-. .-.. -..

# Decode
morsecode decode ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
# HELLO WORLD

# Lenient mode (replace unknown characters with '?')
morsecode encode "HELLO 🙂" --lenient
# .... . .-.. .-.. --- / ?
```

---

## 🌍 Language Support

Perfect 👍 — here’s a **Markdown table** you can drop into the **Language Support** section of your `README.md`.
It uses the **ISO 639-1 two-letter codes** (Set 1) we defined in `morsecode.json`.

---

## 🌍 Language Support

Great — you’re aiming for a **truly global Morse support table** 🌍.

🔑 Important note:

* Morse code itself is **Latin-alphabet–based**, but **ITU extensions** and conventions exist for diacritics (Ä, Ñ, Ü, etc.).
* For **non-Latin scripts** (Arabic, Chinese, Japanese, Korean, etc.), there are historical/adapted Morse systems (e.g., **Wabun code** for Japanese Kana, **Chinese telegraph code**, **Arabic Morse transliteration**).
* To keep things consistent in this library, we map non-Latin languages by **romanization/transliteration** (e.g., Arabic → Latin equivalents, Chinese → Pinyin letters). That way the same dot/dash system works without redesigning the encoder.

---

## 🌍 Language Support

The library supports **50+ languages** across **Europe, Asia, Africa, and the Americas**.
All languages include **A–Z** and **digits (0–9)** via a shared `COMMON` section.
Diacritics (Á, É, Ç, Ö, etc.) are mapped to their base letters unless an official ITU Morse extension exists.
Non-Latin scripts use **romanized equivalents**.

| Code | Language              | Notes (Diacritics / Special Handling)             |
| ---- | --------------------- | ------------------------------------------------- |
| EN   | English               | Base A–Z                                          |
| ES   | Spanish               | Á, É, Í, Ó, Ú, Ü, Ñ                               |
| FR   | French                | À, Â, Æ, Ç, É, È, Ê, Ë, Î, Ï, Ô, Ö, Ù, Û, Ü, Ÿ, Œ |
| DE   | German                | Ä, Ö, Ü, ß                                        |
| PT   | Portuguese            | Á, Â, Ã, À, Ç, É, Ê, Í, Ó, Ô, Õ, Ú, Ü             |
| IT   | Italian               | À, È, É, Ì, Ò, Ó, Ù                               |
| NL   | Dutch                 | Uses base set                                     |
| SV   | Swedish               | Å, Ä, Ö                                           |
| NO   | Norwegian             | Æ, Ø, Å                                           |
| DA   | Danish                | Æ, Ø, Å                                           |
| FI   | Finnish               | Ä, Ö                                              |
| IS   | Icelandic             | Á, Ð, É, Í, Ó, Ú, Ý, Þ, Æ, Ö                      |
| PL   | Polish                | Ą, Ć, Ę, Ł, Ń, Ó, Ś, Ź, Ż                         |
| CS   | Czech                 | Á, Č, Ď, É, Ě, Í, Ň, Ó, Ř, Š, Ť, Ú, Ů, Ý, Ž       |
| SK   | Slovak                | Á, Ä, Č, Ď, É, Í, Ĺ, Ľ, Ň, Ó, Ô, Ŕ, Š, Ť, Ú, Ý, Ž |
| SL   | Slovenian             | Č, Š, Ž                                           |
| HR   | Croatian              | Č, Ć, Đ, Š, Ž                                     |
| SR   | Serbian               | Č, Ć, Đ, Š, Ž                                     |
| RO   | Romanian              | Ă, Â, Î, Ș, Ț                                     |
| HU   | Hungarian             | Á, É, Í, Ó, Ö, Ő, Ú, Ü, Ű                         |
| TR   | Turkish               | Ç, Ğ, İ, Ö, Ş, Ü                                  |
| CA   | Catalan               | À, Ç, É, È, Í, Ï, Ò, Ó, Ú, Ü                      |
| GL   | Galician              | Á, É, Í, Ó, Ú, Ñ                                  |
| EO   | Esperanto             | Ĉ, Ĝ, Ĥ, Ĵ, Ŝ, Ŭ                                  |
| ET   | Estonian              | Õ, Ä, Ö, Ü, Š, Ž                                  |
| LV   | Latvian               | Ā, Č, Ē, Ģ, Ī, Ķ, Ļ, Ņ, Š, Ū, Ž                   |
| LT   | Lithuanian            | Ą, Č, Ę, Ė, Į, Š, Ų, Ū, Ž                         |
| AF   | Afrikaans             | Ë, Ï, Ö, Ü, Ê, Ô, Û                               |
| SW   | Swahili               | Uses base set (Latin letters)                     |
| AR   | Arabic                | Transliterated to Latin (A=ا, B=ب, etc.)          |
| HE   | Hebrew                | Transliterated (Alef=A, Bet=B, etc.)              |
| ZH   | Chinese (Simplified)  | Pinyin Romanization                               |
| ZH-T | Chinese (Traditional) | Pinyin Romanization                               |
| JA   | Japanese              | Wabun Code for Kana (あ=・－, い=・・, etc.)            |
| KO   | Korean                | SKATS (romanized Hangul → Morse equivalents)      |
| HI   | Hindi                 | ISO transliteration → Latin                       |
| BN   | Bengali               | ISO transliteration → Latin                       |
| UR   | Urdu                  | Same as Arabic transliteration                    |
| FA   | Persian (Farsi)       | Same as Arabic transliteration                    |
| TH   | Thai                  | RTGS Romanization → Latin                         |
| VI   | Vietnamese            | Ă, Â, Ê, Ô, Ơ, Ư, Đ mapped to base letters        |
| ID   | Indonesian            | Base set                                          |
| MS   | Malay                 | Base set                                          |
| TL   | Tagalog               | Ñ mapped to N                                     |
| QU   | Quechua               | Base set                                          |
| GN   | Guarani               | Base set                                          |
| NA   | Nahuatl               | Base set                                          |

---

### 🔑 Key Notes

* **Digits 0–9 and space ( / )** are universal for all languages.
* **European languages**: Full diacritic coverage.
* **Asian languages**: Provided through **romanization or historical Morse systems** (e.g., Wabun, SKATS, Pinyin).
* **Arabic & Hebrew**: Transliterated into Latin letters.
* **African & American indigenous languages**: Supported via their Latin orthography.

---

Would you like me to also mark in the table **which languages have diacritic overrides** (like Spanish, French, German)
vs those that just use plain A–Z?

---

## ⚡ Features

* 🔑 Encode and decode Morse code
* 🎯 Strict mode (raise errors) or Lenient mode (skip unknowns)
* 💻 CLI for quick terminal use
* 🌍 Language support via JSON dictionary
* 📝 MIT licensed — free to use anywhere

---

## 📜 License

Released under the MIT License.
Created by **Ricardo** ([mricardo888](https://github.com/mricardo888)).

---

✨ With `morsecode`, you can turn plain text into dots and dashes (and back) in seconds!
