---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# MyST Feature Coverage Test

This document tests various MyST markdown features to identify gaps in conversion.

## 1. Admonitions

### Note (Known to work)

```{note}
This is a note admonition. We know this works.
```

### Warning

```{warning}
This is a warning admonition. Does it convert properly?
```

### Tip

```{tip}
This is a tip admonition. Does it convert properly?
```

### Important

```{important}
This is an important admonition. Does it convert properly?
```

### Caution

```{caution}
This is a caution admonition. Does it convert properly?
```

### Danger

```{danger}
This is a danger admonition. Does it convert properly?
```

### Error

```{error}
This is an error admonition. Does it convert properly?
```

### Hint

```{hint}
This is a hint admonition. Does it convert properly?
```

### See Also

```{seealso}
This is a see-also admonition. Does it convert properly?
```

### Custom Admonition

```{admonition} Custom Title
This is a custom admonition with a title. Does it convert properly?
```

## 2. Code Blocks with Options

### With Line Numbers

```{code-block} python
:linenos:

def hello():
    print("world")
    return 42
```

### With Caption

```{code-block} python
:caption: Example Function

def example():
    return "test"
```

### With Emphasized Lines

```{code-block} python
:emphasize-lines: 2,4

def emphasized():
    # This line should be highlighted
    x = 10
    # This line too
    return x
```

## 3. Nested Directives

### Note with List and Code

```{note}
This note contains nested elements:

- First item
- Second item with code:

  ```python
  x = 42
  print(x)
  ```

- Third item
```

### Warning with Math

```{warning}
This warning contains math:

$$
E = mc^2
$$

Be careful with energy calculations!
```

## 4. Special Blocks

### Sidebar

```{sidebar} Sidebar Title
This is sidebar content that should appear alongside the main text.
```

### Topic

```{topic} Topic Title
This is a topic block with some content.
```

## 5. MyST-Specific Syntax

### Fence-Style Directive

:::note
This uses fence-style directive syntax with three colons.
:::

### Target Definition

(my-target)=
## Section with Target

This section has a target that can be referenced.

### Internal Link

Reference to [target section](my-target).

## 6. Inline Roles

### Keyboard Input

Press {kbd}`Ctrl+C` to copy.

### File Path

Edit the {file}`config.py` file.

### Abbreviation

The {abbr}`HTML (HyperText Markup Language)` specification.

## 7. Advanced Lists

### Definition List with Nested Content

Term 1
: Definition with **bold text** and `code`

Term 2
: Definition with a list:
  - Item 1
  - Item 2

## Test Results

This section will be filled after conversion to see which features worked.
