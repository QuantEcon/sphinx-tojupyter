# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2025-11-14

### Added
- **MyST-NB Glue Support**: Full support for MyST-NB's glue functionality
  - Text and number glue with format specifications (e.g., `{glue:text}`var:.2f``)
  - Figure glue for matplotlib plots (e.g., `{glue:figure}my_plot`)
  - **Base64 Image Embedding**: Glued figures are now embedded as base64 data URIs by default, creating truly standalone notebooks that are easy to distribute
  - **Configurable Image URLs**: Optional `tojupyter_glue_urlpath` and `tojupyter_glue_images_urlpath` settings to reference images from web URLs instead of embedding
  - **Automatic Image Copying**: When using URL paths, glued images are automatically copied to `_build/jupyter/glue/` for easy CDN deployment
  - Inline glue references within paragraphs
  - Graceful handling of cross-document glue references
  - Added `visit_inline()` and `depart_inline()` methods to `JupyterTranslator`
  - Added `visit_PendingGlueReference()` and `depart_PendingGlueReference()` methods
  - Added `_image_to_base64()` helper method for image embedding
  - Added `_copy_glued_image()` helper method for URL-based workflows
  - Comprehensive test suite in `tests/glue/`

### Changed
- None

### Fixed
- None

### Known Limitations
- Cross-document glue references (`{glue:text}`other_doc::key``) are not fully resolved by the jupyter builder (MyST-NB limitation)
