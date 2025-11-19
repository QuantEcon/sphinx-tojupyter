# Versioning Decision: v1.0.0 Instead of v2.0.0

**Date:** November 19, 2024  
**Decision:** Release the refactored sphinx-tojupyter as **v1.0.0** instead of v2.0.0

---

## Rationale

### Why v1.0.0 Makes More Sense

1. **No meaningful v1.0 ever existed**
   - v0.6.0 was the last pre-release version
   - A v1.0.0 tag was briefly created but was identical to v0.6.0
   - This v1.0.0 had no reason to exist and would be immediately deprecated

2. **v1.0.0 should represent "what this package IS"**
   - This refactor delivers on the package's true purpose: "Create Jupyter notebooks"
   - It's a clean, focused, mature implementation
   - v1.0.0 signals "this is the stable, production-ready version"

3. **Better semantic versioning story**
   - v0.x → v1.0 = "experimental → stable"
   - v1.0 → v2.0 (with nothing in between) = confusing
   - Saves v2.x for if we need another major architecture change

4. **Room for incremental improvements**
   - v1.0.0: Core notebook generation (current state)
   - v1.1.0: Enhanced MyST admonition support
   - v1.2.0: Code block options support
   - v1.3.0: Additional MyST features
   - More natural than jumping to v2.0 immediately

5. **Clearer messaging**
   - "v1.0 - First Stable Release" is compelling
   - "v2.0 breaking changes from v1.0 that's identical to v0.6" is confusing

---

## Actions Taken

### 1. Deleted v1.0.0 Tag and Release
```bash
gh release delete v1.0.0 --yes
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### 2. Updated Version References
Changed all references from v2.0.0 to v1.0.0 in:
- `setup.py` - VERSION = 'v1.0.0'
- `CHANGELOG.md` - Release notes
- `MIGRATION.md` - Guide title
- `README.md` - Documentation
- All documentation files in `docs/`
- Test documentation
- Planning documents

### 3. Updated Messaging
- **Old:** "v2.0 breaking changes from v1.0"
- **New:** "v1.0 - First stable release focused on notebook generation"

---

## Migration Path

### For Users on v0.6.0

**Upgrading to v1.0.0:**
- See [MIGRATION.md](MIGRATION.md) for detailed upgrade guide
- Breaking changes documented (removed PDF/HTML/execution features)
- Pin to v0.6.0 if you need the old features

**Stay on v0.6.0:**
```python
# requirements.txt or setup.py
sphinx-tojupyter==0.6.0
```

---

## Future Roadmap

### v1.x Series (Incremental Improvements)
- **v1.0.0** - Core notebook generation (current)
- **v1.1.0** - Enhanced MyST admonitions (warning, tip, important, etc.)
- **v1.2.0** - Code block options (linenos, caption, emphasize-lines)
- **v1.3.0** - Advanced MyST features (fence-style, inline roles)

### v2.x Series (Future Major Changes)
Reserved for potential major architecture changes, such as:
- Complete rewrite for different architecture
- Major breaking changes to API/configuration
- Fundamental changes to how conversion works

---

## Comparison

### If We Used v2.0.0

```
v0.6.0 → v1.0.0 → v2.0.0
         ↑             ↑
     (identical)   (refactored)
     
Problem: v1.0.0 serves no purpose
```

### Using v1.0.0 (Our Choice)

```
v0.6.0 → v1.0.0 → v1.1.0 → v1.2.0 → ... → v2.0.0 (if needed)
         ↑         ↑         ↑                ↑
     (refactored) (MyST++)  (features)   (major change)
     
Benefit: Clear progression, room for growth
```

---

## Conclusion

**✅ This decision:**
- Makes semantic versioning clearer
- Better reflects the package's evolution
- Provides room for incremental improvements
- Reserves v2.x for future needs
- Eliminates an unnecessary v1.0.0 release

**The refactored code will be released as sphinx-tojupyter v1.0.0** - the first stable, 
focused release dedicated to high-quality Jupyter notebook generation.
