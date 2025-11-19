# MyST Markdown Feature Coverage

This document provides a comprehensive analysis of MyST markdown feature support in sphinx-tojupyter v1.0.

## Currently Supported MyST Features

### ✅ Well Supported

1. **Code Cells** (`{code-cell}`)
   - Handled via standard code block translation
   - Full support for different languages

2. **Math** 
   - Inline: `$...$`
   - Display: `$$...$$`
   - Labeled equations via `displaymath` and `math_block` nodes

3. **MyST-NB Glue** 
   - `{glue:text}` role ✅
   - `{glue:figure}` directive ✅
   - Cross-document references (with warnings) ✅

4. **Sphinx-Proof Directives** (15 types)
   - theorem, axiom, lemma, definition, remark
   - conjecture, corollary, algorithm, criterion
   - example, property, observation, proposition
   - assumption, notation, proof
   - All with numbering and cross-references ✅

5. **Basic Markdown**
   - Headers (H1-H6)
   - Emphasis (*italic*, **bold**)
   - Inline code (`code`)
   - Links
   - Images
   - Lists (bullet, numbered, definition)
   - Tables
   - Block quotes
   - Footnotes

6. **Directives**
   - `{note}` ✅
   - `{topic}` ✅
   - `{figure}` ✅
   - `{toctree}` (handled by Sphinx)

## ⚠️ Potentially Missing/Untested MyST Features

### 1. Admonitions (Important!)
MyST supports many admonition types that might not be handled:

- `{warning}` - May not be styled properly
- `{tip}` - Unknown support
- `{important}` - Unknown support
- `{caution}` - Unknown support
- `{attention}` - Unknown support
- `{danger}` - Unknown support
- `{error}` - Unknown support
- `{hint}` - Unknown support
- `{seealso}` - Unknown support

**Status:** We have `visit_note()` but may not handle other admonition types.

### 2. Special Blocks

- `{admonition}` (custom title) - Unknown
- `{sidebar}` - Unknown
- `{margin}` - Jupyter Book specific, likely N/A
- `{epigraph}` - Unknown
- `{highlights}` - Unknown
- `{pull-quote}` - Unknown

### 3. Code/Literal Blocks

- `{code-block}` with options - Partially tested
  - `:linenos:` - line numbers
  - `:emphasize-lines:` - highlight lines
  - `:caption:` - code captions
  
**Status:** Basic code blocks work, but special options may not render

### 4. Containers and Divs

- `{div}` - Generic container - Unknown
- `{container}` - Generic container - Unknown

### 5. Substitutions and Replacements

- `{sub-ref}` - Substitution references - Unknown  
- `{|variable|}` - Text substitutions - Unknown

### 6. Roles (Inline Markup)

- `{kbd}` - Keyboard input - Unknown
- `{menuselection}` - Menu selections - Unknown
- `{guilabel}` - GUI labels - Unknown
- `{file}` - File paths - Unknown
- `{abbr}` - Abbreviations - Unknown
- `{doc}` - Document links - Unknown (might work via reference)
- `{ref}` - Cross-references - Unknown (might work via reference)

### 7. Target and Reference Features

- `(target-name)=` - Target definitions - Unknown
- `[text](target-name)` - Internal links - Unknown
- `{numref}` - Numbered references - Unknown

### 8. Special MyST Syntax

- `:::` - Fence-style directives - Unknown (might work)
- `:::{directive}` - Nested directives - Unknown
- `+++` - Directive options separator - Unknown

### 9. Tables

- Grid tables - Unknown
- List tables - Unknown  
- CSV tables - Unknown

**Status:** Basic markdown tables work, but complex RST tables unknown

### 10. Cross-referencing

- Automatic header anchors - Unknown
- `{ref}` role - Unknown
- `{doc}` role - Unknown
- `{download}` - Already supported ✅

## 📋 Recommended Actions

### High Priority (Common Usage)

1. **Test and document admonitions** - Very commonly used
   - Add test cases for warning, tip, important, caution
   - Ensure they render with appropriate formatting

2. **Test code-block options** - Important for teaching
   - Line numbers
   - Syntax highlighting hints
   - Captions

3. **Test nested directives** - Common in MyST
   - Directives within directives
   - Admonitions within lists

### Medium Priority

4. **Test MyST-specific syntax**
   - `:::` fence-style directives
   - `(target-name)=` targets
   - `[text](target-name)` links

5. **Test substitutions** - Sometimes used
   - Variable substitutions
   - Cross-references

### Low Priority (Can defer)

6. **Special roles** (kbd, guilabel, etc.) - Less common
7. **Advanced tables** - Markdown tables usually sufficient
8. **Containers/divs** - Less common in academic content

## 🧪 Testing Strategy

1. Create `tests/myst_features/` with test cases for:
   - All admonition types
   - Code block options
   - Nested directives
   - MyST-specific syntax

2. Run conversion and check output quality

3. Document unsupported features in README/docs

## 💡 Quick Win Test

Create a single test file `tests/myst_coverage.md` with:

```markdown
# MyST Feature Test

## Admonitions

\```{warning}
This is a warning
\```

\```{tip}
This is a tip
\```

## Code with Options

\```{code-block} python
:linenos:
:emphasize-lines: 2

def hello():
    print("world")  # This line emphasized
\```

## Nested Directive

\```{note}
This note contains:

- A list
- With items
- And a code block:

  \```python
  x = 42
  \```
\```
```

## Test Results

**✅ COMPLETED** - See `MYST-TEST-RESULTS.md` for comprehensive results.

### Quick Summary

**Works Well:**
- ✅ Note admonitions (with formatting)
- ✅ Basic code blocks
- ✅ Math equations
- ✅ Standard markdown (lists, tables, links)

**Degraded (content preserved, formatting lost):**
- ⚠️ Other admonitions (warning, tip, etc.) - render as plain text
- ⚠️ Code block options - ignored (linenos, caption, emphasize-lines)
- ⚠️ Nested directives - split into multiple cells

**Missing:**
- ❌ Fence-style directives (:::)
- ❌ Special inline roles (kbd, file, abbr)

### Decision: Ready for v2.0

**Rationale:**
1. Core functionality works correctly
2. No content is ever lost, only formatting
3. Degradation is graceful and understandable
4. Users have simple workarounds
5. Can enhance in v2.1 without breaking changes

### Next Steps

1. **v2.0**: Release with documented limitations
2. **v2.1**: Add enhanced MyST support
   - Implement remaining admonition types
   - Add code block option support
   - Improve nested directive handling
