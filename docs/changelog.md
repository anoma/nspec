---
icon: octicons/log-16
social:
  cards: false
search:
    exclude: false
list_wikilinks: false
---

# Change Log

## v0.1.0

This is the first release of Anoma's Spec project, following the [[Versioning|semantic-versioning]] scheme.
This version includes all the changes from the creation of this repository. From
here on, we will keep a changelog of all the changes that are made to the
project per version, with better documentation and descriptions of the changes.

### BREAKING CHANGES

- [Node architecture](node)
  - [**#179**](https://github.com/anoma/nspec/pull/179): Reorganize node architecture
    documentation structure
- [Repository maintenance and CI](.)
  - [**#29**](https://github.com/anoma/nspec/pull/29): Remove unused libraries
  - [**#30**](https://github.com/anoma/nspec/pull/30): Remove juvix hook in pro of mkdos Juvix
    plugin
  - [**#53**](https://github.com/anoma/nspec/pull/53): Setup: require only python 3.9
  - [**#60**](https://github.com/anoma/nspec/pull/60): Restructure for v2
  - [**#64**](https://github.com/anoma/nspec/pull/64): Change KV Storage Deletion Documentation
  - [**#65**](https://github.com/anoma/nspec/pull/65): Delete Compute and Randomness Engines
  - [**#69**](https://github.com/anoma/nspec/pull/69): Remove outdates files from arch1 and fix
    formatting
  - [**#104**](https://github.com/anoma/nspec/pull/104): Refactor scope, basic types, and
    application architecture sections
  - [**#115**](https://github.com/anoma/nspec/pull/115): Refactor file and folder names: add
    snake_case convention
- [General specification changes](spec)
  - [**#192**](https://github.com/anoma/nspec/pull/192): Port identity engines to v2 template
- [System and node architecture](sys)
  - [**#210**](https://github.com/anoma/nspec/pull/210): Fix engine message, environment and
    behavior layout

### BUG FIXES

- [Repository maintenance and CI](.)
  - [**#4**](https://github.com/anoma/nspec/pull/4): Fix mike
  - [**#9**](https://github.com/anoma/nspec/pull/9): Add batch of fixes
  - [**#10**](https://github.com/anoma/nspec/pull/10): Fix Index: quick links and remove empty types
    pages
  - [**#18**](https://github.com/anoma/nspec/pull/18): Fix TODO, add todos.py script, and more
    formatting issues
  - [**#19**](https://github.com/anoma/nspec/pull/19): Remove todos on deploy, fix wikilinks warnings
  - [**#21**](https://github.com/anoma/nspec/pull/21): Fix whitespaces
  - [**#22**](https://github.com/anoma/nspec/pull/22): Fix indexes generation with macros and optimize
    caching
  - [**#24**](https://github.com/anoma/nspec/pull/24): Fix minors
  - [**#25**](https://github.com/anoma/nspec/pull/25): CI fixes
  - [**#74**](https://github.com/anoma/nspec/pull/74): Fix broken links in navigation bar and a few
    pages
  - [**#77**](https://github.com/anoma/nspec/pull/77): Fix CI: deploy website by PRs against main, v1,
    and v2
  - [**#78**](https://github.com/anoma/nspec/pull/78): Fix: CI doesnt trigger on edits
  - [**#91**](https://github.com/anoma/nspec/pull/91): Fix default views and deploys in the CI
  - [**#96**](https://github.com/anoma/nspec/pull/96): Fix navigation bar and more broken links due #60
  - [**#101**](https://github.com/anoma/nspec/pull/101): Fix typos and small improve wording
  - [**#105**](https://github.com/anoma/nspec/pull/105): Fix warnings messages due to recent refactors
  - [**#122**](https://github.com/anoma/nspec/pull/122): Fix support for Juvix Markdown snippets
  - [**#123**](https://github.com/anoma/nspec/pull/123): Fix merging conflicts chris-update-basic-types
  - [**#124**](https://github.com/anoma/nspec/pull/124): Fix tutorial nav structure and broken links in
    the footer
  - [**#132**](https://github.com/anoma/nspec/pull/132): Fix minor issues with directories and filenames

### FEATURES

- [Application documentation](apps)
  - [**#198**](https://github.com/anoma/nspec/pull/198): Add transparent RM implementation documentation
- [Python-related changes](python)
  - [**#133**](https://github.com/anoma/nspec/pull/133): Add support for multi-line wiki-style links
- [Repository maintenance and CI](.)
  - [**#2**](https://github.com/anoma/nspec/pull/2): Add better support for WikiLinks and other goodies
  - [**#3**](https://github.com/anoma/nspec/pull/3): Update README and run pre-commit
  - [**#5**](https://github.com/anoma/nspec/pull/5): Add Ubuntu dependencies to the CI
  - [**#6**](https://github.com/anoma/nspec/pull/6): Use site_url for link generation
  - [**#7**](https://github.com/anoma/nspec/pull/7): Add new hook for images
  - [**#8**](https://github.com/anoma/nspec/pull/8): Add lightboxes to images, fix local image loading
  - [**#11**](https://github.com/anoma/nspec/pull/11): Improve link resolution for urls outside nav
  - [**#14**](https://github.com/anoma/nspec/pull/14): Add Last updated time to the footer and other
    fixes
  - [**#15**](https://github.com/anoma/nspec/pull/15): Add a more explicit MathJax config
  - [**#17**](https://github.com/anoma/nspec/pull/17): Revised macros configuration
  - [**#20**](https://github.com/anoma/nspec/pull/20): Refactor hooks
  - [**#23**](https://github.com/anoma/nspec/pull/23): Add previews for PRs
  - [**#27**](https://github.com/anoma/nspec/pull/27): Fix url indexes and improve PR previews
  - [**#28**](https://github.com/anoma/nspec/pull/28): Add tutorial basic instructions
  - [**#31**](https://github.com/anoma/nspec/pull/31): Translate Haskell snippets to Juvix and fix typos
  - [**#51**](https://github.com/anoma/nspec/pull/51): Configuration Engine
  - [**#52**](https://github.com/anoma/nspec/pull/52): Add nix flake
  - [**#56**](https://github.com/anoma/nspec/pull/56): Add page on dynamic code loading
  - [**#58**](https://github.com/anoma/nspec/pull/58): Homogeneous consensus for V2
  - [**#59**](https://github.com/anoma/nspec/pull/59): Readme: tighten up install instructions
  - [**#61**](https://github.com/anoma/nspec/pull/61): Updates kudos spec
  - [**#63**](https://github.com/anoma/nspec/pull/63): Counter example
  - [**#68**](https://github.com/anoma/nspec/pull/68): Add New Engine Specifications from Anoma Elixir
    Database
  - [**#75**](https://github.com/anoma/nspec/pull/75): Add proof-of-stake example
  - [**#80**](https://github.com/anoma/nspec/pull/80): Re-introduced full execution machine for V2
  - [**#81**](https://github.com/anoma/nspec/pull/81): Add BibTeX entries and fix configuration
  - [**#84**](https://github.com/anoma/nspec/pull/84): Add templates for defining engine systems
  - [**#92**](https://github.com/anoma/nspec/pull/92): Add global table of contents
  - [**#95**](https://github.com/anoma/nspec/pull/95): Continue v2 updates
  - [**#97**](https://github.com/anoma/nspec/pull/97): Add git branching strategy
  - [**#98**](https://github.com/anoma/nspec/pull/98): Add citation instructions and restructure markdown
    tutorials
  - [**#99**](https://github.com/anoma/nspec/pull/99): Delete previews for closed PRs on gh-pages branch
  - [**#100**](https://github.com/anoma/nspec/pull/100): Split CI workflows: deploy, pull-request, clean-
    ups
  - [**#103**](https://github.com/anoma/nspec/pull/103): Additional reorganization & updates
  - [**#117**](https://github.com/anoma/nspec/pull/117): Tweaks to message types in basics
  - [**#120**](https://github.com/anoma/nspec/pull/120): Refactor tutorial organization and add a few
    more on conventions
  - [**#121**](https://github.com/anoma/nspec/pull/121): Improve look&feel, organized nav, hide extra
    links and move them to the footer
  - [**#127**](https://github.com/anoma/nspec/pull/127): Update basic abstractions
  - [**#131**](https://github.com/anoma/nspec/pull/131): Add RMv3 content
  - [**#135**](https://github.com/anoma/nspec/pull/135): Show PR number in the site name
  - [**#209**](https://github.com/anoma/nspec/pull/209): Add changelog management system
- [Tutorial and documentation](tutorial)
  - [**#134**](https://github.com/anoma/nspec/pull/134): Refactor tutorial for wiki-style links
- [Juvix types and updates](types)
  - [**#128**](https://github.com/anoma/nspec/pull/128): Add new Juvix definitions from PR-84
  - [**#130**](https://github.com/anoma/nspec/pull/130): Translate SML Identity definitions to Juvix

