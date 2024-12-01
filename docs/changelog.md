---
icon: octicons/log-16
social:
  cards: false
search:
    exclude: false
list_wikilinks: false
---

# Change Log

## v0.1.1

Major revision of the engine definitions, the template, and the ticker engine.

### FEATURES

- [Repository maintenance and CI](.)
  -  [**#217**](https://github.com/anoma/nspec/pull/217): Update template engine
    files to be more consistent, use backticks for Juvix terms/types in
    headlines, uncollapsed sections for type constructors arguments in template
    engine files, and auxiliary sections of Juvix code are always collapsed.

### FIXES

- [Node architecture](node)
  -  [**#219**](https://github.com/anoma/nspec/pull/219): Revisit [[Commitment Engine]]. Changes to the messages, environment, and behaviour types to conform the recent template changes.
  -  [**#253**](https://github.com/anoma/nspec/pull/253): Integration PR that
    combines multiple engine-related changes: [Engines: Use `ByteString` in
    crypto types #242](https://github.com/anoma/nspec/pull/242), [Engines:
    ByteString type definition #255](https://github.com/anoma/nspec/pull/255),
    [Engines: `EngineMsg` revision #241](https://github.com/anoma/nspec/pull/241),
    [EngineID: make `EngineName` compulsory #256](https://github.com/anoma/nspec/pull/256), [Engines: Engine type revision #244](https://github.com/anoma/nspec/pull/244), [ `EngineMsg`: add type param #258](https://github.com/anoma/nspec/pull/258), [Engines: add `GuardEval` and `ActionExec` #260](https://github.com/anoma/nspec/pull/260), and [Engines: Behaviour template revision #226](https://github.com/anoma/nspec/pull/226).
  -  [**#256**](https://github.com/anoma/nspec/pull/256): Make `EngineName`
    compulsory in `EngineID`.
- [Repository maintenance and CI](.)
  -  [**#218**](https://github.com/anoma/nspec/pull/218): Rename `EngineMessage` type to `EngineMsg` and `mkEngineMessage` to `mkEngineMsg`.
  -  [**#220**](https://github.com/anoma/nspec/pull/220): Fix the deployment of the latest version by deploying the website if the branch name is `main` or matches the semver pattern, and add information about the version and the commit hash to the title for reference.
  -  [**#222**](https://github.com/anoma/nspec/pull/222): Remove SML codebase as
    not used any more and any other reference in the markdown files
  -  [**#225**](https://github.com/anoma/nspec/pull/225): Fix navigation table for the identity component
  -  [**#227**](https://github.com/anoma/nspec/pull/227): Update Juvix version in Nix flake due to breaking changes, and
    also the input packages while at it.
  -  [**#250**](https://github.com/anoma/nspec/pull/250): Update policy on Juvix typechecking. The whole codebase in a
    PR should typecheck before merging
- [Tutorial and documentation](tutorial)
  -  [**#257**](https://github.com/anoma/nspec/pull/257): Refactor the Git strategy: introduce integration PRs for
    better overview of complex changes
- [Juvix types and updates](types)
  -  [**#221**](https://github.com/anoma/nspec/pull/221): Update the prelude to
    incorporate the latest changes in the `Stdlib`, including the addition of
    applicative and monad traits, and the integration of the `containers` library.
    This update also includes changes to data type definitions, with the `@`
    syntax now used for declaration, creation, and matching on records, and other
    removals like `: Type` for implicit arguments and function-style declarations.
  -  [**#226**](https://github.com/anoma/nspec/pull/226): Update [[Template Engine|Template]] & [[Ticker Behaviour|Ticker Behaviour]] according to the engine & message type changes. The examples have been improved with better clarity. The documentation now uses headlines instead of collapsible boxes and definition lists instead of tables. A new diagram template has been added that illustrates conditions and effects of actions.
  -  [**#241**](https://github.com/anoma/nspec/pull/241): `EngineMsg`-related changes: rename `MessageID` to `EngineMsgID`, add `getEngineMsgFrom(Timestamped)Trigger`, and rename `getMessageFrom(Timestamped)Trigger` to `getMsgFrom(Timestamped)Trigger`.
  -  [**#242**](https://github.com/anoma/nspec/pull/242): Use `ByteString` in crypto types.
  - [**#244**](https://github.com/anoma/nspec/pull/244): Major refactoring of
    engine-related types. The `Engine` type now includes a `cfg` field of type
    `EngineConfig` containing static configuration (engine name and local node
    ID). For consistency, `EngineEnvironment` has been renamed to `EngineEnv`. The
    `EngineBehaviour` type has undergone several changes: the conflict solver has
    been removed (to be replaced by new mechanism in
    [#246](https://github.com/anoma/nspec/pull/246)), precomputation results are
    now passed directly as action arguments, and the `action` field has been
    replaced with action labels defined by label type.
    
  -  [**#249**](https://github.com/anoma/nspec/pull/249): Remove `name` field in Engine instances due to PR 242
  -  [**#255**](https://github.com/anoma/nspec/pull/255): Make ByteString `String` instead of `Nat`
  -  [**#258**](https://github.com/anoma/nspec/pull/258): Engine-related changes: add type parameter to parameterized the type of message and [rename `EngineConfig` to `EngineCfg`](https://github.com/anoma/nspec/pull/258/commits/e35d75f8a187155629fa1b0a5b72ea6983a49e2d)
  -  [**#260**](https://github.com/anoma/nspec/pull/260): Revise engine behaviour type: add `GuardEval (Seq)` and `ActionExec (First & Any)`, `EngineCfg`: add `getEngineIDFromEngineCfg`. Partially addresses [#246](https://github.com/anoma/nspec/issues/246).

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
  -  [**#214**](https://github.com/anoma/nspec/pull/214): Add GitHub template for creating PRs
- [Tutorial and documentation](tutorial)
  - [**#134**](https://github.com/anoma/nspec/pull/134): Refactor tutorial for wiki-style links
- [Juvix types and updates](types)
  - [**#128**](https://github.com/anoma/nspec/pull/128): Add new Juvix definitions from PR-84
  - [**#130**](https://github.com/anoma/nspec/pull/130): Translate SML Identity definitions to Juvix

