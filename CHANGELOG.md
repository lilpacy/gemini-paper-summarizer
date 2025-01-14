# Changelog

## [0.5.1] - 2025-01-14
### Added
- `--version` option to display package version
- Added examples

## [0.5.0] - 2025-01-14
### Added
- Multilingual support for `de`, `en`, `es`, `fr`, `ja`, `ko`, `zh` language modules
- Support for processing multiple PDF files in a single run
- Output directory option (`-d` or `--output-dir`)

### Improved
- Enhanced Gemini API call reliability with retry mechanism and logging
- Added Windows file globbing support

## [0.4.0] - 2025-01-11
### Changed
- Refactored project structure to use `gp_summarize` package
- Standardized test cases using pytest format
- Reorganized statistical display items and calculated TPS (Tokens Per Second)

## [0.3.0] - 2025-01-06
### Changed
- Updated system prompt to output in a more formal Japanese style (だ・である調)
- Modified intermediate file generation to save files in the same location as the specified output file

## [0.2.0] - 2025-01-05
### Changed
- Restructured section files to be created in source-named directories to distribute numerous files
- Limited API requests to 10 per minute (65 seconds margin) to align with Gemini's free tier limitations

## [0.1.0] - 2025-01-04
### Added
- Initial release of the project
