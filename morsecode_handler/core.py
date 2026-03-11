"""
Core encode/decode functions for the morsecode_handler package.

Public functions:
- encode(text, language="EN", *, strict=True, unknown="?", uppercase=None)
- decode(morse, language="EN", *, strict=True, unknown="?", uppercase=None)

Language keys follow ISO 2-letter codes (e.g., 'EN').
We avoid duplicating digits/space in every language by using a COMMON section.
"""

from __future__ import annotations

import functools
import importlib.resources
import json
from typing import Dict, List, Optional

from .exceptions import (
    LanguageNotFoundError,
    UnknownCharacterError,
    UnknownMorseCodeError,
)

DEFAULT_LANG = "EN"
_COMMON_KEY = "COMMON"

_RAW: Optional[Dict[str, Dict[str, str]]] = None


def _load_data() -> Dict[str, Dict[str, str]]:
    """Lazy-load the morse mapping JSON data."""
    global _RAW
    if _RAW is not None:
        return _RAW

    try:
        # For Python 3.9+, use importlib.resources.files
        if hasattr(importlib.resources, "files"):
            data_str = (
                importlib.resources.files("morsecode_handler")
                .joinpath("data/morsecode_handler.json")
                .read_text(encoding="utf-8")
            )
        else:
            # Fallback for Python < 3.9 (e.g., 3.7, 3.8)
            data_str = importlib.resources.read_text(
                "morsecode_handler.data", "morsecode_handler.json", encoding="utf-8"  # noqa: E501
            )

        _RAW = (
            json.load(lambda _=None: None) if False else json.loads(data_str)
        )  # type checker trick / loads

    except Exception as e:
        raise RuntimeError(f"Failed to load morsecode_handler.json: {e}")

    # Validate required sections
    if DEFAULT_LANG not in _RAW:
        raise RuntimeError(f"morsecode_handler.json must contain an '{DEFAULT_LANG}' base mapping.")  # noqa: E501
    if _COMMON_KEY not in _RAW:
        raise RuntimeError(
            f"morsecode_handler.json must contain a '{_COMMON_KEY}' "
            "mapping for digits/space."
        )

    return _RAW


def _normalize_lang(lang: str) -> str:
    """Normalize a language ID to uppercase two-letter form (e.g., 'en' -> 'EN')."""  # noqa: E501
    return lang.upper()


def _get_language_overrides(language: str) -> Dict[str, str]:
    """
    Return the override dict for the selected language code.

    Raises:
        LanguageNotFoundError: if language code not available and not 'EN'.
    """
    raw_data = _load_data()
    key = _normalize_lang(language)
    if key == DEFAULT_LANG:
        return {}
    if key not in raw_data:
        raise LanguageNotFoundError(
            key,
            available=[k for k in raw_data.keys() if k not in (_COMMON_KEY,)]
        )
    return raw_data[key]


@functools.lru_cache(maxsize=None)
def _merge_language_dict(language: str) -> Dict[str, str]:
    """
    Merge EN base letters + language overrides + COMMON digits/space.

    The result contains:
      - A–Z from EN
      - Any diacritics/overrides from the selected language
      - Digits/space from COMMON
    """
    raw_data = _load_data()
    base = dict(raw_data[DEFAULT_LANG])  # letters A–Z
    overrides = _get_language_overrides(language)  # diacritics etc.
    common = raw_data[_COMMON_KEY]  # digits/space

    merged: Dict[str, str] = {}

    # Ensure all baseline and override keys are uppercase
    # to match encode text lookup.
    for k, v in base.items():
        merged[k.upper()] = v
    for k, v in overrides.items():
        merged[k.upper()] = v
    for k, v in common.items():
        merged[k.upper()] = v

    return merged


@functools.lru_cache(maxsize=None)
def _build_reverse_pref_cached(language: str) -> Dict[str, str]:
    """
    Cached wrapper to build reverse map for a given language.
    """
    merged = _merge_language_dict(language)
    overrides = _get_language_overrides(language)
    return _build_reverse_pref_internal(merged, overrides)


def _build_reverse_pref_internal(
    merged: Dict[str, str], overrides: Dict[str, str]
) -> Dict[str, str]:
    """
    Build a reverse map (morse -> char) with a language-aware preference order.

    - If the selected language appears to use a non-ASCII script (e.g., Arabic,
      Russian),  # noqa: E501
      prefer its override characters first so collisions resolve to that script.
      # noqa: E501
    - Otherwise (Latin-script languages), prefer ASCII A–Z first (status quo).
    """
    raw_data = _load_data()
    rev: Dict[str, str] = {}

    # Heuristic: if any override key is non-Latin
    # (e.g., Cyrillic > 1000, Arabic > 1500), treat as non-Latin script.
    # Latin diacritics are generally < 500.
    non_ascii_script = any(ord(k) > 500 for k in overrides.keys())

    def insert_chars(chars: list[str]) -> None:
        for ch in chars:
            morse = merged.get(ch.upper())
            if morse:
                rev.setdefault(morse, ch.upper())

    ascii_AZ = [chr(cp) for cp in range(ord("A"), ord("Z") + 1)]

    # Cast dict_keys to list so the loop interprets characters correctly
    lang_overrides = list(overrides.keys())
    common_keys = list(raw_data[_COMMON_KEY].keys())

    if non_ascii_script:
        # 1) Prefer language-specific overrides (e.g., Arabic/Russian letters)
        insert_chars(lang_overrides)
        # 2) Then ASCII A–Z (useful if input mixes scripts)
        insert_chars(ascii_AZ)
    else:
        # Latin languages: keep original behavior (prefer ASCII A–Z)
        insert_chars(ascii_AZ)
        insert_chars(lang_overrides)

    # 3) Digits & space from COMMON
    insert_chars(common_keys)

    # 4) Any remaining keys (backfill)
    for ch, morse in merged.items():
        if morse not in rev:
            rev[morse] = ch.upper()

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
        unknown: Placeholder used when `strict=False` and a character is
                 unmapped.  # noqa: E501
        uppercase: If True, force-uppercase text before encoding. If None,
                   defaults to  # noqa: E501
                   True when `language` != DEFAULT_LANG, else False.

    Returns:
        Space-separated Morse string, with '/' between words.

    Raises:
        LanguageNotFoundError, UnknownCharacterError.
    """
    lang_norm = _normalize_lang(language)
    if uppercase is None:
        uppercase = lang_norm != DEFAULT_LANG

    src = text.upper() if uppercase else text
    mapping = _merge_language_dict(lang_norm)

    out: List[str] = []
    for i, ch in enumerate(src):
        if ch == " ":
            out.append(mapping.get(" ", "/"))
            continue

        # When not uppercase forced, we need to look up the uppercase version
        lookup_ch = ch.upper()
        code = mapping.get(lookup_ch)
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
        uppercase: If True, force-uppercase the decoded text. If None,
                   defaults to  # noqa: E501
                   True when `language` != DEFAULT_LANG, else False.

    Returns:
        Decoded plain text (words separated by single spaces).

    Raises:
        LanguageNotFoundError, UnknownMorseCodeError.
    """
    # Decode Morse code into plain text.
    lang_norm = _normalize_lang(language)
    if uppercase is None:
        uppercase = lang_norm != DEFAULT_LANG

    reverse = _build_reverse_pref_cached(lang_norm)

    tokens = morse.split()
    out: List[str] = []

    mapping = _merge_language_dict(lang_norm)
    space_token = mapping.get(" ", "/")

    for idx, tok in enumerate(tokens):
        if tok == "/" or tok == space_token:
            out.append(" ")
            continue
        ch = reverse.get(tok)
        if ch is None:
            if strict:
                raise UnknownMorseCodeError(tok, idx, lang_norm)
            out.append(unknown)
        else:
            out.append(ch)

    # For decode, word separations are preserved as " " and everything else is
    # joined
    text = "".join(out)

    # We strip extra spaces and capitalize
    text = " ".join(text.split())
    if uppercase:
        text = text.upper()
    return text
