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
````

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

## 🌍 Supported Languages

This library supports **41 languages** across Latin, Cyrillic, Arabic, Hebrew, Greek, and Korean scripts.  
We follow the **ISO 639-1 standard** for the two-letter language codes (e.g., `EN` for English, `FR` for French, `RU` for Russian).

| Code | Language     | Code | Language    | Code | Language    | Code | Language   |
|------|--------------|------|-------------|------|-------------|------|------------|
| AF   | Afrikaans    | AR   | Arabic      | EU   | Basque      | CA   | Catalan    |
| HR   | Croatian     | CS   | Czech       | DA   | Danish      | NL   | Dutch      |
| EN   | English      | EO   | Esperanto   | ET   | Estonian    | FI   | Finnish    |
| FR   | French       | GL   | Galician    | DE   | German      | EL   | Greek      |
| HE   | Hebrew       | HU   | Hungarian   | IS   | Icelandic   | ID   | Indonesian |
| GA   | Irish        | IT   | Italian     | KO   | Korean      | LV   | Latvian    |
| LT   | Lithuanian   | MS   | Malay       | NO   | Norwegian   | PL   | Polish     |
| PT   | Portuguese   | RO   | Romanian    | RU   | Russian     | SR   | Serbian    |
| SK   | Slovak       | SL   | Slovenian   | ES   | Spanish     | SV   | Swedish    |
| TL   | Tagalog      | TR   | Turkish     | UK   | Ukrainian   | VI   | Vietnamese |

---

## ⚡ Features

* 🔑 Encode and decode Morse code
* 🎯 Strict mode (raise errors) or Lenient mode (skip unknowns)
* 💻 CLI for quick terminal use
* 🌍 Multi-language support via JSON dictionary
* 📝 MIT licensed — free to use anywhere

---

## 📜 License

Released under the MIT [License](LICENSE).
Created by **Ricardo** ([mricardo888](https://github.com/mricardo888)).

---

✨ With `morsecode`, you can turn plain text into dots and dashes (and back) in seconds!

---
