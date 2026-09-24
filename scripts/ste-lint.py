#!/usr/bin/env python3
"""Deterministic linter for the structural STE rules in SKILL.md.

Checks only rules verifiable without ASD's dictionary. Deliberately never
flags hedges or modality (may/might/could): the skill treats confidence as
content, and a linter that pressures hedges out would rewrite claims.

Usage:
    ste-lint.py FILE [FILE ...]
    echo "text" | ste-lint.py [--json]
    ste-lint.py --baseline 5 FILE      # pass unless hard violations exceed 5
    ste-lint.py --disable passive-voice,present-perfect FILE
    ste-lint.py --enable history FILE  # opt-in rules (see OPTIONAL_RULES)
    ste-lint.py --max-words 30 FILE    # sentence cap (default 25)
    ste-lint.py --summary FILE ...     # per-file counts, worst file first
    ste-lint.py --lang rust --parts docs,comments,messages src/lib.rs
    ste-lint.py --selftest

Input languages (`--lang`, else chosen from the file extension):

- markdown (default, also plain text and stdin): prose is read per
  paragraph, so a sentence that wraps over several lines is one sentence.
  Code fences, display math, HTML comments, link definitions and YAML front
  matter are skipped. Inline code and inline math count as one word each.
  Link targets do not count.
- rust (`*.rs`): only the prose parts are read, never the code. `--parts`
  selects them (default `docs,comments`):
    docs      `///`, `//!`, `/** */`, `/*! */` (read as Markdown, as rustdoc does)
    comments  `//`, `/* */` (lines that look like commented-out code are skipped)
    messages  string literals inside panic!/assert!/expect/println!/... calls
    strings   every string literal with three or more words
  Messages are error text, so they get the strict cap (`--max-words-strict`,
  default 20).

Exit 1 when hard ("advisory-free") violations exceed the baseline (default 0).
Advisory findings (passive voice, compound tenses, em dashes, dual-use
phrasal verbs) never fail the run. Exit 2 on a usage error.
"""
import bisect
import json
import re
import sys

# ponytail: regex heuristics, not a parser. No noun-cluster rule — needs POS
# tagging to avoid constant false positives; add spaCy-backed rule if ever needed.
# No ellipsis rule by owner's choice: technical writing sometimes earns one.
RULES = [
    ("semicolon", "advisory-free",
     re.compile(r";"),
     "STE bans the semicolon (Rule 8.1). Split into separate sentences."),
    ("phrasal-verb", "advisory-free",
     re.compile(r"\b(spin(?:ning|s)? up|spun up|reach(?:ing|es|ed)? out|div(?:e|es|ing|ed) into|dove into|kick(?:ing|s|ed)? off|circl(?:e|es|ing|ed) back|touch(?:ing|es|ed)? base"
                r"|figur(?:e|es|ed|ing) out|find(?:s|ing)? out|found out|point(?:s|ed|ing)? out|end(?:s|ed|ing)? up"
                r"|c(?:o|a)m(?:e|es|ing) up with|g(?:e|o)t(?:s|ting)? rid of|look(?:s|ed|ing)? into|sort(?:s|ed|ing)? out)\b", re.I),
     "Soft phrasal verb. Use the single plain verb (start, contact, read, begin)."),
    ("phrasal-verb-technical", "advisory",
     re.compile(r"\b(set(?:s|ting)? up|fall(?:s|ing)? back|fell back|back(?:s|ed|ing)? up|turn(?:s|ed|ing)? (?:on|off)"
                r"|shut(?:s|ting)? down|pick(?:s|ed|ing)? up|hand(?:s|ed|ing)? (?:off|over|on|back)|rul(?:e|es|ed|ing) out"
                r"|fill(?:s|ed|ing)? in|carr(?:y|ies|ied|ying) on|g(?:ive|ives|ave|iving) back)\b", re.I),
     "Possible phrasal verb (Rule 9.3). If it is not a fixed technical term, use one plain verb."),
    ("marketing-adjective", "advisory-free",
     re.compile(r"\b(seamless(?:ly)?|robust(?:ly)?|cutting-edge|effortless(?:ly)?|blazing[- ]fast|world-class|state-of-the-art|game-chang(?:ing|er))\b", re.I),
     "Marketing adjective. Delete, or replace with the measurement that earns the claim."),
    ("nominalization", "advisory-free",
     re.compile(r"\b(perform|performs|performed|conduct|conducts|conducted|carry out|carries out|carried out)\s+(?:a|an|the)\s+\w+(?:tion|sion|ment|ance|ence|ysis)\b", re.I),
     "Action frozen into a noun. Use the verb (analyze, not perform an analysis of)."),
    ("passive-voice", "advisory",
     re.compile(r"\b(is|are|was|were|been|being)\s+(\w+ed|given|taken|made|done|found|seen|known|shown|written|built|sent|set|run|read|kept|held|left|put)\b(?!\s+(?:to|for|by)\s+\w+ing)", re.I),
     "Possible passive voice. Name the actor and use an active verb, unless the actor is unknown or irrelevant."),
    ("present-perfect", "advisory",
     # modal + perfect infinitive ("may have failed") is a protected hedge, not present perfect
     re.compile(r"(?<!\bmay )(?<!\bmight )(?<!\bcould )(?<!\bshould )(?<!\bwould )(?<!\bmust )\b(has|have|had)\s+(?:been\s+)?\w+(?:ed|en)\b", re.I),
     "Compound tense. Use simple past/present unless current relevance is the point (then keep and flag)."),
    ("em-dash", "advisory",
     re.compile(r"(?<=\S)\s*—\s*(?=\S)"),
     "Em dash joins two ideas (run-on). Consider two sentences, a colon, or parentheses."),
]

# Opt-in rules (`--enable NAME`). Not STE rules: house rules that often come
# with STE rewrites of documentation.
OPTIONAL_RULES = [
    ("history", "advisory-free",
     re.compile(r"\b(no longer|used to (?:be|have)|previously|formerly|any ?more|currently|as of now|nowadays|originally"
                r"|(?:was|were|has been|have been) (?:renamed|replaced|removed|changed|added)|an? (?:earlier|older|previous) version)\b", re.I),
     "Change history in a description of the current state. Describe what is, not what changed."),
]

# One word, one meaning: groups of verbs commonly rotated for the same action.
# Only pairs where the members are genuinely interchangeable — error/fault/failure
# are distinct concepts and stay out.
SYNONYM_GROUPS = [
    ("check", "verify", "confirm", "validate"),
    ("delete", "remove", "erase"),
    ("start", "launch", "begin", "initiate"),
    ("stop", "halt", "terminate"),
    ("show", "display"),
    ("use", "utilize", "employ"),
    ("fix", "repair", "correct"),
    ("send", "transmit"),
    ("get", "retrieve", "fetch", "obtain"),
    ("change", "modify", "alter"),
]

MAX_WORDS = 25  # descriptions cap; instructions cap is 20 but undetectable without context
MAX_WORDS_STRICT = 20  # error messages (rust `messages`) are strict-mode text

CODE_FENCE = re.compile(r"^(```|~~~)")
INLINE_CODE = re.compile(r"(`+)(?!`).*?(?<!`)\1(?!`)")  # N backticks close N (CommonMark)
LIST_ITEM_START = re.compile(
    r"^(?P<indent> {0,3})(?P<marker>[-*+]|[0-9]+[.)])(?P<gap> +)(?P<body>.*)$"
)
CONJUNCTION_END = re.compile(r"\b(?:and|or)\s*$", re.I)
TABLE_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")

# Masking: every span keeps its length, so columns stay exact.
INLINE_MATH = re.compile(r"(?<![\\$\w])\$(?=[^\s$])[^$\n]*?(?<=[^\s\\])\$(?![\d$])")
LINK_TARGET = re.compile(r"\]\([^)\s]*\)")
LINK_REF = re.compile(r"\]\[[^\]]*\]")
HTML_COMMENT_INLINE = re.compile(r"<!--.*?-->")
FORMAT_ARG = re.compile(r"\{[^{}\s]*\}")  # {}, {x}, {path:?}, {:>10.6}
LINK_DEF = re.compile(r"^ {0,3}\[[^\]]+\]:\s*\S")
HEADING = re.compile(r"^ {0,3}#{1,6}(?:\s+|$)")
BLOCKQUOTE = re.compile(r"^ {0,3}(?:>\s?)+")
WORD = re.compile(r"\w")
# A sentence ends at . ! or ? (plus closing quotes/brackets/emphasis), then
# whitespace, then something that can open a sentence.
SENTENCE_END = re.compile(r"[.!?][\"')\]*_]*\s+(?=[\"'(\[*_]*[A-ZΑ-Ω])")
ABBREVIATIONS = {"e.g", "i.e", "vs", "cf", "etc", "approx", "fig", "no", "eq", "resp", "al"}

RUST_PARTS = {"docs", "comments", "messages", "strings"}
MESSAGE_CALLEES = {
    "panic!", "assert!", "assert_eq!", "assert_ne!", "debug_assert!", "debug_assert_eq!",
    "debug_assert_ne!", "unreachable!", "unimplemented!", "todo!", "expect", "expect_err",
    "println!", "eprintln!", "print!", "eprint!", "format!", "write!", "writeln!",
    "bail!", "anyhow!", "ensure!", "error!", "warn!", "info!",
}
RAW_STRING_START = re.compile(r'(?:b|c)?r(?P<hashes>#*)"')
# A `//` line that ends like code and contains code punctuation.
COMMENTED_OUT_CODE = re.compile(r"^(?=.*(?:[=(]|::|->)).*[;{}]\s*$")


def _word_re(base):
    return re.compile(r"\b" + base + r"(?:s|es|ed|d|ing)?\b", re.I)


# Synonym rotation is about *verbs*. A determiner before the word marks a noun
# ("the start", "per launch"), and "fixed"/"correct" are usually adjectives
# ("fixed shapes") unless an object follows ("fixed the bug").
NOUN_CUE = re.compile(r"(?:\b(?:the|a|an|this|that|these|those|each|every|its|their|per|at|of|one|no|any"
                      r"|same|both|few|fewer|many|more|most|some|all|other|such|first|last|two|three)\s+|-)$",
                      re.I)
COMPOUND_AFTER = re.compile(r"^-\w")  # "launch-bound": part of a compound modifier
ADJECTIVE_FORMS = {"fixed", "correct"}
VERB_OBJECT = re.compile(r"^\s+(?:the|a|an|it|this|that|these|those|them)\b", re.I)


def _verb_match(pattern, text):
    """First match of a synonym-group member that reads as a verb."""
    for m in pattern.finditer(text):
        if NOUN_CUE.search(text[:m.start()]) or COMPOUND_AFTER.match(text[m.end():]):
            continue
        if m.group(0).lower() in ADJECTIVE_FORMS and not VERB_OBJECT.match(text[m.end():]):
            continue
        return m
    return None


def _leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def _is_list_continuation(line, content_indent):
    if not line.strip():
        return True
    if LIST_ITEM_START.match(line):
        return False
    return _leading_spaces(line) >= content_indent


def _split_table_row(line):
    """Return trimmed table cells and their zero-based source columns.

    A pipe must separate at least two cells. Escaped pipes stay in their cell.
    This deliberately implements only the ordinary Markdown table shape; it is
    enough to distinguish a table from prose that happens to contain a pipe.
    """
    left = len(line) - len(line.lstrip())
    right = len(line.rstrip())
    content = line[left:right]
    if "|" not in content:
        return None
    if content.startswith("|"):
        content = content[1:]
        left += 1
    if content.endswith("|"):
        content = content[:-1]
    raw_cells = re.split(r"(?<!\\)\|", content)
    if len(raw_cells) < 2:
        return None

    cells = []
    column = left
    for raw_cell in raw_cells:
        leading = len(raw_cell) - len(raw_cell.lstrip())
        cells.append((raw_cell.strip(), column + leading))
        column += len(raw_cell) + 1
    return cells


def _markdown_table_cells(lines):
    """Map ordinary Markdown table rows to their prose cells.

    The separator row anchors detection, so pipe-containing prose is not
    treated as a table. Both leading-pipe and no-leading-pipe table styles are
    accepted when their header and body use the same number of cells.
    """
    table_cells = {}
    index = 1
    while index < len(lines):
        separator = _split_table_row(lines[index])
        header = _split_table_row(lines[index - 1])
        if (not separator or not header or len(separator) != len(header)
                or not all(TABLE_SEPARATOR_CELL.fullmatch(cell)
                           for cell, _ in separator)):
            index += 1
            continue

        table_cells[index - 1] = header
        table_cells[index] = []
        index += 1
        while index < len(lines):
            row = _split_table_row(lines[index])
            if not row or len(row) != len(separator):
                break
            table_cells[index] = row
            index += 1
    return table_cells


def _dangling_conjunction_findings(text, filename):
    lines = text.splitlines()
    findings = []
    in_fence = False
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if CODE_FENCE.match(stripped):
            in_fence = not in_fence
            index += 1
            continue
        if in_fence:
            index += 1
            continue
        start = LIST_ITEM_START.match(line)
        if not start:
            index += 1
            continue

        content_indent = (len(start.group("indent"))
                          + len(start.group("marker"))
                          + len(start.group("gap")))
        item_lines = [(index, start.group("body"))]
        next_index = index + 1
        item_fence = False
        while next_index < len(lines):
            candidate = lines[next_index]
            candidate_stripped = candidate.strip()
            if CODE_FENCE.match(candidate_stripped):
                # Fence delimiters are state markers, not meaningful item lines.
                item_fence = not item_fence
                next_index += 1
                continue
            if item_fence:
                next_index += 1
                continue
            if not _is_list_continuation(candidate, content_indent):
                break
            item_lines.append((next_index, candidate))
            next_index += 1

        meaningful = []
        for line_index, item_line in item_lines:
            # Preserve code spans as neutral operands while ignoring their contents.
            cleaned = INLINE_CODE.sub(" CODE ", item_line).strip()
            if cleaned:
                meaningful.append((line_index, cleaned))
        if meaningful:
            end_line_index, end_line = meaningful[-1]
            conjunction = CONJUNCTION_END.search(end_line)
        else:
            end_line_index, end_line, conjunction = None, None, None
        if conjunction:
            if end_line_index == index:
                finding_line = index + 1
                finding_col = start.start("marker") + 1
            else:
                raw_end_line = next(
                    raw for line_index, raw in item_lines
                    if line_index == end_line_index
                )
                masked_end_line = INLINE_CODE.sub(
                    lambda match: " " * len(match.group(0)), raw_end_line
                )
                raw_conjunction = CONJUNCTION_END.search(masked_end_line)
                finding_line = end_line_index + 1
                finding_col = raw_conjunction.start() + 1 if raw_conjunction else 1
            findings.append({
                "file": filename,
                "line": finding_line,
                "col": finding_col,
                "rule": "dangling-conjunction",
                "level": "advisory-free",
                "match": end_line,
                "message": "List item ends with a coordinating conjunction. Complete the item or join it with the next item.",
            })
        index = next_index
    return findings


# ---------------------------------------------------------------------------
# Prose extraction. A block is a list of (lineno, col0, content) source lines
# of one kind; `_paragraphs` cuts a block into paragraphs of such pieces.
# ---------------------------------------------------------------------------

def _mask(text, kind):
    """Neutralize non-prose spans, keeping the length (and so the columns)."""
    def placeholder(match):
        return "X" + " " * (len(match.group(0)) - 1)

    def blank(match):
        return " " * len(match.group(0))

    text = INLINE_CODE.sub(placeholder, text)
    text = INLINE_MATH.sub(placeholder, text)
    if kind in ("messages", "strings"):
        text = FORMAT_ARG.sub(placeholder, text)
    text = LINK_TARGET.sub(blank, text)
    text = LINK_REF.sub(blank, text)
    text = HTML_COMMENT_INLINE.sub(blank, text)
    return text.replace("[", " ").replace("]", " ")


def _paragraphs(lines):
    """Cut Markdown block lines into paragraphs of (lineno, col0, text) pieces.

    A blank line, a heading, a list-item start, a table cell or a skipped
    construct ends a paragraph. Wrapped lines join into one paragraph.
    """
    contents = [content for _, _, content in lines]
    table = _markdown_table_cells(contents)
    paragraphs, current = [], []
    fence = math = html = False

    def flush():
        if current:
            paragraphs.append(list(current))
            current.clear()

    for index, (lineno, col0, raw) in enumerate(lines):
        stripped = raw.strip()
        if fence:
            fence = not CODE_FENCE.match(stripped)
            continue
        if math:
            math = "$$" not in stripped
            continue
        if html:
            html = "-->" not in stripped
            continue
        if CODE_FENCE.match(stripped):
            flush()
            fence = True
            continue
        if stripped.startswith("$$"):
            flush()
            math = "$$" not in stripped[2:]
            continue
        if stripped.startswith("<!--"):
            flush()
            html = "-->" not in stripped
            continue
        if not stripped:
            flush()
            continue
        if index in table:
            flush()
            for cell, column in table[index]:
                if cell:
                    paragraphs.append([(lineno, col0 + column, cell)])
            continue
        if LINK_DEF.match(raw):
            flush()
            continue
        heading = HEADING.match(raw)
        if heading:
            flush()
            paragraphs.append([(lineno, col0 + heading.end(), raw[heading.end():].rstrip())])
            continue
        quote = BLOCKQUOTE.match(raw)
        if quote:
            col0 += quote.end()
            raw = raw[quote.end():]
        item = LIST_ITEM_START.match(raw)
        if item:
            flush()
            current.append((lineno, col0 + item.start("body"), item.group("body").rstrip()))
            continue
        lead = len(raw) - len(raw.lstrip())
        current.append((lineno, col0 + lead, raw.strip()))
    flush()
    return paragraphs


def _markdown_blocks(text):
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":  # YAML front matter
        for index in range(1, len(lines)):
            if lines[index].strip() in ("---", "..."):
                start = index + 1
                break
    return [{"kind": "markdown",
             "lines": [(n + 1, 0, lines[n]) for n in range(start, len(lines))]}]


def _unescape_rust_string(raw, raw_start, is_raw, pos):
    """Split a string literal body into (lineno, col0, text) lines.

    `\\n` and real newlines break lines, a backslash-newline continuation joins
    them (with the leading whitespace of the next line dropped, as rustc
    does). Other escapes shrink to one character, so columns after an escape
    are approximate.
    """
    out, text, begin = [], [], None
    k = 0

    def end_line():
        if begin is not None or text:
            lineno, col = pos(raw_start + (begin if begin is not None else k))
            out.append((lineno, col, "".join(text)))

    while k < len(raw):
        char = raw[k]
        if begin is None:
            begin = k
        if not is_raw and char == "\\" and k + 1 < len(raw):
            nxt = raw[k + 1]
            if nxt == "\n":
                k += 2
                while k < len(raw) and raw[k] in " \t":
                    k += 1
                continue
            if nxt == "n":
                end_line()
                text, begin = [], None
                k += 2
                continue
            if nxt == "u":
                close = raw.find("}", k)
                text.append("?")
                k = close + 1 if close > 0 else k + 2
                continue
            text.append(" " if nxt == "t" else nxt)
            k += 2
            continue
        if char == "\n":
            end_line()
            text, begin = [], None
            k += 1
            continue
        text.append(char)
        k += 1
    end_line()
    return out


def _rust_blocks(src, parts):
    """Lex Rust source into prose blocks: comments, docs and string literals."""
    line_starts = [0] + [k + 1 for k, char in enumerate(src) if char == "\n"]

    def pos(index):
        line = bisect.bisect_right(line_starts, index) - 1
        return line + 1, index - line_starts[line]

    blocks, records = [], []
    stack, prev = [], [None, None]  # callee per open bracket, last two tokens
    i, n = 0, len(src)

    def is_ident_char(char):
        return char.isalnum() or char == "_"

    def add_string(content_start, raw, is_raw):
        callee = stack[-1] if stack else None
        kind = "messages" if callee in MESSAGE_CALLEES else "strings"
        words = len([t for t in raw.split() if WORD.search(t)])
        if (kind == "messages" and "messages" in parts) or ("strings" in parts and words >= 3):
            blocks.append({"kind": kind, "lines": _unescape_rust_string(raw, content_start, is_raw, pos)})

    while i < n:
        char = src[i]
        if src.startswith("//", i):
            end = src.find("\n", i)
            end = n if end < 0 else end
            text = src[i:end]
            lineno, col = pos(i)
            standalone = not src[line_starts[lineno - 1]:i].strip()
            if text.startswith("///") and not text.startswith("////"):
                kind, prefix = "outer", 3
            elif text.startswith("//!"):
                kind, prefix = "inner", 3
            else:
                kind, prefix = "line", 2
            content = text[prefix:]
            if content.startswith(" "):
                content, prefix = content[1:], prefix + 1
            records.append((kind, lineno, col + prefix, content.rstrip(), standalone, col))
            i = end
            continue
        if src.startswith("/*", i):
            depth, j = 1, i + 2
            while j < n and depth:
                if src.startswith("/*", j):
                    depth, j = depth + 1, j + 2
                elif src.startswith("*/", j):
                    depth, j = depth - 1, j + 2
                else:
                    j += 1
            doc = (src.startswith("/*!", i)
                   or (src.startswith("/**", i) and not src.startswith("/***", i)
                       and not src.startswith("/**/", i)))
            body_start = i + (3 if doc else 2)
            lines, k = [], body_start
            for piece in src[body_start:max(body_start, j - 2)].split("\n"):
                lineno, col = pos(k)
                stripped = piece.lstrip()
                lead = len(piece) - len(stripped)
                if stripped.startswith("*"):
                    stripped = stripped[1:]
                    lead += 1
                    if stripped.startswith(" "):
                        stripped, lead = stripped[1:], lead + 1
                lines.append((lineno, col + lead, stripped.rstrip()))
                k += len(piece) + 1
            kind = "docs" if doc else "comments"
            if kind in parts:
                blocks.append({"kind": kind, "lines": lines})
            i = j
            continue
        if char in "bcr" and (i == 0 or not is_ident_char(src[i - 1])):
            raw = RAW_STRING_START.match(src, i)
            if raw:
                close = '"' + raw.group("hashes")
                end = src.find(close, raw.end())
                end = n if end < 0 else end
                add_string(raw.end(), src[raw.end():end], True)
                i = end + len(close)
                continue
            if char in "bc" and src.startswith('"', i + 1):
                i += 1
                char = '"'
        if char == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            add_string(i + 1, src[i + 1:j], False)
            i = j + 1
            prev = [prev[1], ("string",)]
            continue
        if char == "'":
            if src.startswith("\\", i + 1):
                close = src.find("'", i + 3)
                i = n if close < 0 else close + 1
            elif i + 2 < n and src[i + 2] == "'":
                i += 3
            else:
                i += 1  # a lifetime or a label
            continue
        if char.isalpha() or char == "_":
            j = i
            while j < n and is_ident_char(src[j]):
                j += 1
            prev = [prev[1], ("ident", src[i:j])]
            i = j
            continue
        if char in "([{":
            callee = None
            if prev[1] and prev[1][0] == "ident":
                callee = prev[1][1]
            elif prev[1] == ("bang",) and prev[0] and prev[0][0] == "ident":
                callee = prev[0][1] + "!"
            stack.append(callee)
            prev = [prev[1], ("open",)]
        elif char in ")]}":
            if stack:
                stack.pop()
            prev = [prev[1], ("close",)]
        elif char == "!":
            prev = [prev[1], ("bang",)]
        elif not char.isspace():
            prev = [prev[1], ("punct", char)]
        i += 1

    # Consecutive standalone comment lines of one kind form one block.
    groups = []
    for kind, lineno, col, content, standalone, indent in records:
        last = groups[-1] if groups else None
        if (last and standalone and last["standalone"] and last["kind"] == kind
                and lineno == last["lines"][-1][0] + 1
                and (kind != "line" or indent == last["indent"])):
            last["lines"].append((lineno, col, content))
        else:
            groups.append({"kind": kind, "standalone": standalone, "indent": indent,
                           "lines": [(lineno, col, content)]})
    for group in groups:
        kind = "comments" if group["kind"] == "line" else "docs"
        if kind not in parts:
            continue
        lines = group["lines"]
        if kind == "comments":
            lines = [(lineno, col, "" if COMMENTED_OUT_CODE.match(content) else content)
                     for lineno, col, content in lines]
        blocks.append({"kind": kind, "lines": lines})
    blocks.sort(key=lambda block: block["lines"][0][:2] if block["lines"] else (0, 0))
    return blocks


def _sentence_spans(text):
    """Yield (start, end) of each sentence in a paragraph, abbreviation-aware."""
    start = 0
    for match in SENTENCE_END.finditer(text):
        word = text[:match.start() + 1].split()[-1].lower().strip("(\"'*_").rstrip(".")
        if word in ABBREVIATIONS:
            continue
        yield start, match.start() + 1
        start = match.end()
    yield start, len(text)


def lint(text, filename="<stdin>", lang=None, parts=None, max_words=MAX_WORDS,
         max_words_strict=MAX_WORDS_STRICT, enabled=()):
    """Lint one document. Returns (findings, words_total)."""
    if lang is None:
        lang = "rust" if filename.endswith(".rs") else "markdown"
    if lang == "rust":
        blocks = _rust_blocks(text, set(parts or ("docs", "comments")))
    else:
        blocks = _markdown_blocks(text)
    rules = RULES + [rule for rule in OPTIONAL_RULES if rule[0] in enabled]

    findings = []
    words_total = 0
    # first occurrence of each synonym-group member: (group_idx, base) -> (line, col, match)
    seen_synonyms = {}

    def finding(line, col, rule, level, match, message, **extra):
        findings.append({"file": filename, "line": line, "col": col, "rule": rule,
                         "level": level, "match": match, "message": message, **extra})

    for block in blocks:
        kind = block["kind"]
        cap = max_words_strict if kind == "messages" else max_words
        for pieces in _paragraphs(block["lines"]):
            raw = " ".join(content for _, _, content in pieces)
            masked = " ".join(_mask(content, kind) for _, _, content in pieces)
            starts, offset = [], 0
            for _, _, content in pieces:
                starts.append(offset)
                offset += len(content) + 1

            def at(index):
                piece = bisect.bisect_right(starts, index) - 1
                lineno, col0, _ = pieces[piece]
                return lineno, col0 + index - starts[piece] + 1

            for rule_id, level, pattern, message in rules:
                for m in pattern.finditer(masked):
                    finding(*at(m.start()), rule_id, level, raw[m.start():m.end()].strip(), message)
            for gi, group in enumerate(SYNONYM_GROUPS):
                for base in group:
                    m = _verb_match(_word_re(base), masked)
                    if m:
                        spot = (*at(m.start()), m.group(0))
                        if (gi, base) not in seen_synonyms or spot < seen_synonyms[(gi, base)]:
                            seen_synonyms[(gi, base)] = spot
            for begin, end in _sentence_spans(masked):
                sentence = masked[begin:end]
                n = len([token for token in sentence.split() if WORD.search(token)])
                words_total += n
                if n > cap:
                    original = raw[begin:end]
                    lead = len(original) - len(original.lstrip())
                    excerpt = " ".join(original.split())
                    finding(*at(begin + lead), "long-sentence", "advisory-free", f"{n} words",
                            f"Sentence has {n} words (cap {cap}). Split it.",
                            excerpt=excerpt[:80] + ("…" if len(excerpt) > 80 else ""))
        # Rustdoc and string blocks are small Markdown documents of their own.
        virtual = "\n".join(content for _, _, content in block["lines"])
        for f in _dangling_conjunction_findings(virtual, filename):
            lineno, col0, _ = block["lines"][f["line"] - 1]
            f["line"], f["col"] = lineno, col0 + f["col"]
            findings.append(f)
    # synonym rotation: flag each member after the first, at its first occurrence
    for gi, group in enumerate(SYNONYM_GROUPS):
        present = [(seen_synonyms[(gi, b)], b) for b in group if (gi, b) in seen_synonyms]
        if len(present) > 1:
            present.sort()  # document order
            first_base = present[0][1]
            for (lineno, col, match), base in present[1:]:
                finding(lineno, col, "synonym-rotation", "advisory-free", match,
                        f"'{base}' and '{first_base}' name the same action. Pick one and use it every time.")
    findings.sort(key=lambda f: (f["line"], f["col"]))
    return findings, words_total


def report(findings, words_total, as_json, hard_count, baseline):
    rate = round(len(findings) * 100 / words_total, 1) if words_total else 0.0
    if as_json:
        print(json.dumps({"violations": findings, "count": len(findings),
                          "hard_count": hard_count, "baseline": baseline,
                          "words": words_total, "per_100_words": rate}, indent=2))
        return
    for f in findings:
        detail = f"{f['match']}: {f['excerpt']}" if "excerpt" in f else f["match"]
        print(f"{f['file']}:{f['line']}:{f['col']} {f['rule']}: {f['message']} [{detail}]")
    print(f"\n{len(findings)} violations ({hard_count} hard, baseline {baseline}), "
          f"{words_total} words, {rate} per 100 words")
    print("Hedges/modality (may, might, could) are never flagged: confidence is content.")


def report_summary(per_file):
    """One line per file, the most hard violations first."""
    rows = sorted(per_file, key=lambda row: (-row[1], -row[2], row[0]))
    print(f"{'hard':>5} {'adv':>5} {'words':>7}  file")
    for path, hard, advisory, words in rows:
        print(f"{hard:>5} {advisory:>5} {words:>7}  {path}")


def selftest():
    bad = ("The panel is removed; spin up the job. "
           "Perform an analysis of the seamless log. "
           "We have received the report.")
    findings, _ = lint(bad)
    rules = {f["rule"] for f in findings}
    for expected in ("semicolon", "phrasal-verb", "nominalization",
                     "marketing-adjective", "passive-voice", "present-perfect"):
        assert expected in rules, expected
    # hedges must never be flagged, including modal + perfect infinitive
    findings, _ = lint("The request may have failed. It could be a timeout. "
                       "The disk might have filled.")
    assert findings == [], findings
    # code blocks skipped
    findings, _ = lint("```\nx = a; y = b\n```")
    assert findings == []
    # all supported list markers, case variants, and trailing whitespace
    findings, _ = lint(
        "- Confirm the target and\n"
        "* Record the result OR  \n"
        "+ Close the panel\n"
        "1. Start the task and\n"
        "2) Stop the task OR"
    )
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 4, dangling
    assert [f["line"] for f in dangling] == [1, 2, 4, 5], dangling
    assert [f["col"] for f in dangling] == [1, 1, 1, 1], dangling
    assert all(f["level"] == "advisory-free" for f in dangling), dangling

    # valid continuation lines and standalone four-space code are ignored
    findings, _ = lint("  - Confirm the target and\n    record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Confirm the target\n  and")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 2, dangling
    assert dangling[0]["col"] == 3, dangling
    findings, _ = lint("    - code and")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("> - Confirm the target and\n> - Record the result or")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Do this and\n~~~\ncode and\n~~~")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 1, dangling
    findings, _ = lint("```text\n- code and\n```")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)

    # one- and three-space markers and ordered continuation width
    findings, _ = lint(" - Start the task and\n   record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("-  Start the task and\n   record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("-\tStart the task and")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("   - Start the task and", filename="fixture.md")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["col"] == 4, dangling
    assert dangling[0]["file"] == "fixture.md"
    assert dangling[0]["match"].endswith("and")
    assert "Complete the item" in dangling[0]["message"]
    findings, _ = lint("100. Start the task and\n  unrelated text")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1, dangling
    findings, _ = lint("- Start the task and.\n- Stop the task or,")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Start the task and\n\n  record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Parent item and\n  - Nested item or")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert [f["line"] for f in dangling] == [1, 2], dangling

    # ordinary prose, inline code, and fenced code are ignored
    findings, _ = lint("The process may include steps and")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Use `and` as a label")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Combine `left` and `right`")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings), findings
    findings, _ = lint("~~~\n- code and\n~~~")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint(("word " * 30).strip() + ".")
    assert any(f["rule"] == "long-sentence" for f in findings)
    # Markdown table syntax is layout, not prose. Each cell stays lintable.
    short_cell = " ".join(f"term{number}" for number in range(1, 25)) + "."
    for table in (
            "| Label | Detail |\n"
            "| --- | --- |\n"
            f"| Clear | {short_cell} |",
            "Label | Detail\n"
            "--- | ---\n"
            f"Clear | {short_cell}"):
        findings, words_total = lint(table)
        assert not any(f["rule"] == "long-sentence" for f in findings), findings
        assert words_total == 27, words_total
    long_cell = " ".join(f"term{number}" for number in range(1, 27)) + "."
    findings, _ = lint(
        "| Label | Detail |\n"
        "| --- | --- |\n"
        f"| Clear | {long_cell} |"
    )
    long_sentences = [f for f in findings if f["rule"] == "long-sentence"]
    assert len(long_sentences) == 1, long_sentences
    assert long_sentences[0]["match"] == "26 words", long_sentences
    # synonym rotation: second member flagged, first named as the keeper
    findings, _ = lint("Check the config file. Then verify the output. Verify twice.")
    rot = [f for f in findings if f["rule"] == "synonym-rotation"]
    assert len(rot) == 1 and "'verify' and 'check'" in rot[0]["message"], rot
    # single consistent term: no flag
    findings, _ = lint("Check the config. Check the output.")
    assert not any(f["rule"] == "synonym-rotation" for f in findings)
    # nouns and adjectives are not verb rotation
    findings, _ = lint("Start the job. Count each launch and the same launches. "
                       "Both display forms. The kernel-launch count. Use fixed shapes. It is correct.")
    assert not any(f["rule"] == "synonym-rotation" for f in findings), findings
    findings, _ = lint("Fix the bug. Then corrected the value. Correct the typo.")
    assert any(f["rule"] == "synonym-rotation" and f["match"] == "corrected" for f in findings), findings
    # per-file labels
    findings, _ = lint("a; b", filename="x.md")
    assert findings[0]["file"] == "x.md"

    # A sentence wrapped over several lines is one sentence, reported where it starts.
    wrapped = ("Intro.\nOne two three four five six seven\n"
               + "\n".join(["one two three four five six seven"] * 3) + ".\n\nShort one.")
    long_sentences = [f for f in lint(wrapped)[0] if f["rule"] == "long-sentence"]
    assert len(long_sentences) == 1, long_sentences
    assert (long_sentences[0]["line"], long_sentences[0]["col"]) == (2, 1), long_sentences
    assert long_sentences[0]["match"] == "28 words", long_sentences
    assert long_sentences[0]["excerpt"].startswith("One two"), long_sentences
    # abbreviations do not end a sentence, capitals after them do not split
    assert lint("See e.g. Burn for this. Then stop.")[1] == 7
    # inline code and math count as one word, link targets do not count
    assert lint("Use `a b c` and $x + y$ here.")[1] == 5
    assert lint("See [`Layer`](crate::modules::Layer) now.")[1] == 3
    # LaTeX `\;` in math and display math are not semicolons
    findings, _ = lint("Inline $a\\;b$ math.\n\n$$\nx\\;y\n$$\n\nThen text.")
    assert not any(f["rule"] == "semicolon" for f in findings), findings
    # YAML front matter, HTML comments and link definitions are skipped
    findings, words = lint("---\nname: x; y\n---\n<!-- a; b -->\n[x]: https://a.b/c;d\nText.")
    assert findings == [] and words == 1, (findings, words)
    # a double-backtick span can hold a backtick or a semicolon
    findings, words = lint("The set ``a;`b`` is small.")
    assert findings == [] and words == 5, (findings, words)
    # columns stay exact across masked spans
    findings, _ = lint("The `code` part; then more.")
    semicolon = [f for f in findings if f["rule"] == "semicolon"]
    assert semicolon[0]["col"] == 16, semicolon
    # em dash is advisory, a lone table dash is not a finding
    findings, _ = lint("One idea — and another.\n\n| a | b |\n| --- | --- |\n| — | x |")
    dashes = [f for f in findings if f["rule"] == "em-dash"]
    assert len(dashes) == 1 and dashes[0]["level"] == "advisory", dashes
    # opt-in history rule
    text = "This no longer panics. It currently runs once."
    assert not any(f["rule"] == "history" for f in lint(text)[0])
    assert len([f for f in lint(text, enabled={"history"})[0] if f["rule"] == "history"]) == 2

    # Rust: code is never prose; docs and comments are read as Markdown.
    rust = (
        "//! Module doc; with a semicolon.\n"
        "use a::b; // trailing note; here\n"
        "/// Outer doc that wraps\n"
        "/// over two lines.\n"
        "fn f<'a>(x: &'a str) -> char { let c = ';'; let s = \"not; prose\"; c }\n"
        "// let commented = out(code);\n"
        "/* block; comment */\n"
        "fn g() { panic!(\"bad state; stop {x:?}\"); }\n"
        "const R: &str = r#\"raw \"quoted\"; text here\"#;\n"
    )
    findings, _ = lint(rust, filename="lib.rs")
    semicolons = sorted((f["line"], f["col"]) for f in findings if f["rule"] == "semicolon")
    assert semicolons == [(1, 15), (2, 27), (7, 9)], semicolons
    findings, _ = lint(rust, filename="lib.rs", parts={"messages"})
    assert [(f["line"], f["col"]) for f in findings] == [(8, 27)], findings
    findings, _ = lint(rust, filename="lib.rs", parts={"strings"})
    assert sorted(f["line"] for f in findings) == [8, 9], findings
    # a doc comment is one paragraph over its lines; messages use the strict cap
    doc = "/// " + " ".join(["word"] * 13) + "\n/// " + " ".join(["word"] * 13) + ".\nfn f() {}\n"
    findings, _ = lint(doc, filename="a.rs")
    assert [(f["line"], f["col"], f["match"]) for f in findings] == [(1, 5, "26 words")], findings
    msg = "fn f() { assert!(x, \"" + " ".join(["word"] * 21) + "\"); }\n"
    assert [f["match"] for f in lint(msg, filename="a.rs", parts={"messages"})[0]] == ["21 words"]
    # a backslash continuation joins the string lines
    cont = "fn f() { panic!(\"first half; \\\n    second half\"); }\n"
    findings, _ = lint(cont, filename="a.rs", parts={"messages"})
    assert [f["rule"] for f in findings] == ["semicolon"], findings
    print("selftest OK")


def _usage_error(message):
    print(f"ste-lint: {message}", file=sys.stderr)
    return 2


def main(argv):
    if "--selftest" in argv:
        selftest()
        return 0
    as_json = "--json" in argv
    summary = "--summary" in argv
    baseline = 0
    disabled, enabled = set(), set()
    lang, parts = None, None
    max_words, max_words_strict = MAX_WORDS, MAX_WORDS_STRICT
    paths = []
    known = ({rule[0] for rule in RULES} | {rule[0] for rule in OPTIONAL_RULES}
             | {"long-sentence", "synonym-rotation", "dangling-conjunction"})
    i = 0
    try:
        while i < len(argv):
            a = argv[i]
            if a == "--baseline":
                i += 1
                baseline = int(argv[i])
            elif a == "--disable":
                i += 1
                disabled = set(argv[i].split(","))
            elif a == "--enable":
                i += 1
                enabled = set(argv[i].split(","))
            elif a == "--lang":
                i += 1
                lang = argv[i]
            elif a == "--parts":
                i += 1
                parts = set(argv[i].split(","))
            elif a == "--max-words":
                i += 1
                max_words = int(argv[i])
            elif a == "--max-words-strict":
                i += 1
                max_words_strict = int(argv[i])
            elif not a.startswith("--"):
                paths.append(a)
            i += 1
    except (IndexError, ValueError):
        return _usage_error(f"option {argv[i - 1] if i else ''} needs a value")
    unknown = (disabled | enabled) - known
    if unknown:
        return _usage_error(f"unknown rule(s): {', '.join(sorted(unknown))}. "
                            f"Known: {', '.join(sorted(known))}")
    if lang not in (None, "markdown", "rust"):
        return _usage_error(f"unknown --lang {lang}. Known: markdown, rust")
    if parts is not None and parts - RUST_PARTS:
        return _usage_error(f"unknown --parts {', '.join(sorted(parts - RUST_PARTS))}. "
                            f"Known: {', '.join(sorted(RUST_PARTS))}")

    options = dict(lang=lang, parts=parts, max_words=max_words,
                   max_words_strict=max_words_strict, enabled=enabled)
    documents = ([(p, open(p, encoding="utf-8").read()) for p in paths]
                 or [("<stdin>", sys.stdin.read())])
    findings, words_total, per_file = [], 0, []
    for path, text in documents:
        found, words = lint(text, filename=path, **options)
        found = [f for f in found if f["rule"] not in disabled]
        hard = sum(1 for f in found if f["level"] == "advisory-free")
        per_file.append((path, hard, len(found) - hard, words))
        findings.extend(found)
        words_total += words

    hard_count = sum(1 for f in findings if f["level"] == "advisory-free")
    if summary:
        report_summary(per_file)
    else:
        report(findings, words_total, as_json, hard_count, baseline)
    return 1 if hard_count > baseline else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:  # e.g. `ste-lint.py … | head`
        sys.exit(1)
