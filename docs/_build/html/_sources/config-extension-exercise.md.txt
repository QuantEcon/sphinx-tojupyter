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

(config-extension-exercise)=
# Configuration for Exercise Directives

```{contents} Options
---
depth: 1
local: 
---
```

## exercise_include_exercise

Enable inclusion / exclusion of exercises directives contained in the rst







|Values|
|:--------------------------------------------------------------------------------------------------:|
|True (|**|default|**|)|
|False|

`conf.py` usage:

```{code-cell} python
exercise_include_exercise = False
```

## exercise_inline_exercises

Add inline exercises as a formatting choice







|Values|
|:--------------------------------------------------------------------------------------------------:|
|False (|**|default|**|)|
|True|

If the config variable exercise_inline_exercises is set to false (the default),
then where ever the exercise initially appeared in the body of the document, you will
instead see a link that says `See exercise #` which refers to an ExerciseList.

