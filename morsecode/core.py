"""
Core encode/decode functions for the morsecode package.

Public functions:
- encode(text, language="EN", *, strict=True, unknown="?", uppercase=None)
- decode(morse, language="EN", *, strict=True, unknown="?", uppercase=None)

Language keys follow ISO 2-letter codes (e.g., 'EN').
We avoid duplicating digits/space in every language by using a COMMON section.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from .exceptions import (
    LanguageNotFoundError,
    UnknownCharacterError,
    UnknownMorseCodeError,
)

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "morsecode.json")
with open(_DATA_PATH, "r", encoding="utf-8") as _f:
    _RAW: Dict[str, Dict[str, str]] = json.load(_f)

# Validate required sections
if "EN" not in _RAW:
    raise RuntimeError("morsecode.json must contain an 'EN' base mapping.")
if "COMMON" not in _RAW:
    raise RuntimeError("morsecode.json must contain a 'COMMON' mapping for digits/space.")

DEFAULT_LANG = "EN"


def _normalize_lang(lang: str) -> str:
    """Normalize a language ID to uppercase two-letter form (e.g., 'en' -> 'EN')."""
    return lang.upper()


def _get_language_overrides(language: str) -> Dict[str, str]:
    """
    Return the override dict for the selected language code.

    Raises:
        LanguageNotFoundError: if language code not available and not 'EN'.
    """
    key = _normalize_lang(language)
    if key == "EN":
        return {}
    if key not in _RAW:
        raise LanguageNotFoundError(key, available=[k for k in _RAW.keys() if k not in ("COMMON",)])
    return _RAW[key]


def _merge_language_dict(language: str) -> Dict[str, str]:
    """
    Merge EN base letters + language overrides + COMMON digits/space.

    The result contains:
      - A–Z from EN
      - Any diacritics/overrides from the selected language
      - Digits/space from COMMON
    """
    base = dict(_RAW["EN"])            # letters A–Z
    overrides = _get_language_overrides(language)  # diacritics etc.
    common = _RAW["COMMON"]            # digits/space

    merged: Dict[str, str] = {}
    merged.update(base)       # baseline letters
    merged.update(overrides)  # diacritics override/add
    merged.update(common)     # digits + space

    return merged


def _build_reverse_pref_ascii(merged: Dict[str, str]) -> Dict[str, str]:
    """
    Build a reverse map (morse -> char) preferring ASCII A–Z for any collisions.

    Strategy:
      1) First insert ASCII A–Z if present.
      2) Then insert digits/space if present.
      3) Finally insert any remaining keys (e.g., diacritics) only if not set yet.
    """
    rev: Dict[str, str] = {}

    # 1) Prefer plain ASCII letters
    for codepoint in range(ord("A"), ord("Z") + 1):
        ch = chr(codepoint)
        morse = merged.get(ch)
        if morse:
            rev.setdefault(morse, ch)

    # 2) Digits & space from COMMON
    for key in _RAW["COMMON"].keys():
        morse = merged.get(key)
        if morse:
            rev.setdefault(morse, key)

    # 3) Remaining keys (diacritics, special letters)
    for ch, morse in merged.items():
        rev.setdefault(morse, ch)

    return rev


def encode(
        text: str,
        language: str = DEFAULT_LANG,
        *,
        strict: bool = True,
        unknown: str = "?",
        uppercase: Optional[bool] = None,
) -> str:
    """
    Encode plain text into Morse code.

    Args:
        text: Input text to encode.
        language: Two-letter language code (default: 'EN').
        strict: If True, raise UnknownCharacterError for unmapped characters.
                If False, emit `unknown` for unmapped characters.
        unknown: Placeholder used when `strict=False` and a character is unmapped.
        uppercase: If True, force-uppercase text before encoding. If None, defaults to
                   True when `language` != DEFAULT_LANG, else False.

    Returns:
        Space-separated Morse string, with '/' between words.

    Raises:
        LanguageNotFoundError, UnknownCharacterError.
    """
    lang_norm = _normalize_lang(language)
    if uppercase is None:
        uppercase = (lang_norm != DEFAULT_LANG)

    src = text.upper() if uppercase else text
    mapping = _merge_language_dict(lang_norm)

    out: List[str] = []
    for i, ch in enumerate(src):
        if ch == " ":
            out.append("/")
            continue
        code = mapping.get(ch.upper())
        if code is None:
            if strict:
                raise UnknownCharacterError(ch, i, lang_norm)
            out.append(unknown)
        else:
            out.append(code)

    # Collapse multiple consecutive '/'
    result: List[str] = []
    prev_slash = False
    for tok in out:
        if tok == "/":
            if not prev_slash:
                result.append(tok)
            prev_slash = True
        else:
            result.append(tok)
            prev_slash = False

    return " ".join(result)


def decode(
        morse: str,
        language: str = DEFAULT_LANG,
        *,
        strict: bool = True,
        unknown: str = "?",
        uppercase: Optional[bool] = None,
) -> str:
    """
    Decode Morse code into plain text.

    Args:
        morse: Morse string; letters separated by spaces, words by '/'.
        language: Two-letter language code (default: 'EN').
        strict: If True, raise UnknownMorseCodeError for unmapped tokens.
                If False, insert `unknown` for unmapped tokens.
        unknown: Placeholder used when `strict=False` and a token is unmapped.
        uppercase: If True, force-uppercase the decoded text. If None, defaults to
                   True when `language` != DEFAULT_LANG, else False.

    Returns:
        Decoded plain text (words separated by single spaces).

    Raises:
        LanguageNotFoundError, UnknownMorseCodeError.
    """
    lang_norm = _normalize_lang(language)
    if uppercase is None:
        uppercase = (lang_norm != DEFAULT_LANG)

    merged = _merge_language_dict(lang_norm)
    reverse = _build_reverse_pref_ascii(merged)

    tokens = morse.split()
    out: List[str] = []

    for idx, tok in enumerate(tokens):
        if tok == "/":
            out.append(" ")
            continue
        ch = reverse.get(tok)
        if ch is None:
            if strict:
                raise UnknownMorseCodeError(tok, idx, lang_norm)
            out.append(unknown)
        else:
            out.append(ch)

    text = "".join(out)
    text = " ".join(text.split())
    if uppercase:
        text = text.upper()
    return text
