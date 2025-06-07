---
icon: material/book-open-variant
social:
  cards: false
search:
    exclude: false
tags:
  - changelog
---

# Change Log

## [v1.0.0](https://specs.anoma.net/v1.0.0/)

This release introduces significant new features and improvements to the Anoma
specification, focusing on:

- protocol adapter integration
- resource machine specifications
- application-specific documentation

## [v0.2.0](https://specs.anoma.net/v0.2.0/)

This release introduces significant new features and improvements to the Anoma specification, including protocol adapter integration, engine simulation capabilities, and major updates to the Resource Machine specifications. Key highlights include:

- Added comprehensive protocol adapter integration documentation
- Introduced interactive engine simulator with message passing support
- Updated Resource Machine specifications (post-HHH edition)
- Reorganized documentation structure and navigation
- Updated to Juvix stdlib v0.11.0
- Various CI/CD improvements and tooling updates

### Features

- **System architecture**
  -  [**#356**](https://github.com/anoma/nspec/pull/356): Add protocol adapter integration pages
  -  [**#359**](https://github.com/anoma/nspec/pull/359): Update RM specs (post-HHH edition)
  -  [**#369**](https://github.com/anoma/nspec/pull/369): Rename `resourceLogicProofs` to `logicVerifierInputs`
- **Node architecture**
  -  [**#347**](https://github.com/anoma/nspec/pull/347): Implement interactive engine simulator with message passing support
  -  [**#355**](https://github.com/anoma/nspec/pull/355): Add engine simulator with message passing and pretty printing
- **Repository maintenance and CI**
  -  [**#358**](https://github.com/anoma/nspec/pull/358): Deploy pages to another repo
  -  [**#367**](https://github.com/anoma/nspec/pull/367): Remove redundant deployment
  -  [**#374**](https://github.com/anoma/nspec/pull/374): EVM-PA: use permalinks and small improvements

### Fixes

- **Repository maintenance and CI**
  -  [**#343**](https://github.com/anoma/nspec/pull/343): Fix mkdocs nav
  -  [**#351**](https://github.com/anoma/nspec/pull/351): Fix/update github actions
  -  [**#363**](https://github.com/anoma/nspec/pull/363): Enforce pre-commit checks and remove auto-fix
  -  [**#364**](https://github.com/anoma/nspec/pull/364): Remove pull request template
- **Tutorial and documentation**
  -  [**#381**](https://github.com/anoma/nspec/pull/381): Reorganize navigation in mkdocs.yml

### Changes

- **Juvix types and updates**
  -  [**#361**](https://github.com/anoma/nspec/pull/361): Bump to stdlib 0.11.0 and name convention used for user-defined data types
- **Repository maintenance and CI**
  -  [**#365**](https://github.com/anoma/nspec/pull/365): Update project configuration and tooling

## [v0.1.4](https://specs.anoma.net/v0.1.4/)

This release focuses on improving the prose, layout, and documentation structure. Key changes include:

- Reorganized node architecture documentation for better clarity
- Reorganized the navigation bar to be more consistent and easier to use
- Added a new tutorial: [[Anomian]]
- Several prose improvements on engines, e.g: [[Mempool Worker Engine]],
  [[Executor Engine]], [[Shard Engine]]
- CSS changes to improve the layout and readability of the website, like
  better separation for headers and footers that improve, for example, the
  readability of message interfaces
- Updated Juvix type definitions to match latest standards
- Added new definitions for [[List of basic types|Prelude]]
- Improved template engine documentation for easier engine creation

### Features

- System architecture
  -  [**#334**](https://github.com/anoma/nspec/pull/334): Add deletion criterion to delete blobs immediately

### Fixes

- [Repository maintenance and CI](.)
  -  [**#297**](https://github.com/anoma/nspec/pull/297): Fixes for issues seen in [v0.1.3](https://specs.anoma.net/v0.1.3/ )
  -  [**#306**](https://github.com/anoma/nspec/pull/306): Add data structures and interfaces used by RM
  -  [**#307**](https://github.com/anoma/nspec/pull/307): Prose improvements for commitment, decryption, and identity
    management engines
  -  [**#308**](https://github.com/anoma/nspec/pull/308): The Little Anomian
  -  [**#309**](https://github.com/anoma/nspec/pull/309): Heindel has written up their two cents on the [[Anomian]]
  -  [**#310**](https://github.com/anoma/nspec/pull/310): Heindel/[[Anomian]] review v0.2 some ideas for improvements
  -  [**#311**](https://github.com/anoma/nspec/pull/311): Prose improvements for
    [[Mempool Worker Engine]], [[Executor Engine]], and [[Shard Engine]]'s descriptions.
  -  [**#312**](https://github.com/anoma/nspec/pull/312): nix flake update to
    support Juvix v0.6.9
  -  [**#313**](https://github.com/anoma/nspec/pull/313): Revision of all message interfaces but not for networking's
    engines
  -  [**#314**](https://github.com/anoma/nspec/pull/314): Add more fixes for message interfaces for consistency
  -  [**#315**](https://github.com/anoma/nspec/pull/315): Add a few corrections to the Anomian doc
  -  [**#320**](https://github.com/anoma/nspec/pull/320): Update Network subsystems' engine to comply standard
  -  [**#328**](https://github.com/anoma/nspec/pull/328): Move string comparison to prelude
  -  [**#331**](https://github.com/anoma/nspec/pull/331): RM type fixes
  -  [**#332**](https://github.com/anoma/nspec/pull/332): Improve layout, documentation structure, navigation and
    readability with indexes, tags and descriptions
  -  [**#336**](https://github.com/anoma/nspec/pull/336): some changes, proposed as a result of specs overall review
    (revamped)
  -  [**#337**](https://github.com/anoma/nspec/pull/337): Heindel/anthony/prose 3 suggestions for fixing the markdown
- System architecture
  -  [**#334**](https://github.com/anoma/nspec/pull/334): Add missing deletion criterion to delete blobs after the
    transaction
- Juvix types and updates
  -  [**#298**](https://github.com/anoma/nspec/pull/298): Update juvix v0.6.9
  -  [**#302**](https://github.com/anoma/nspec/pull/302): [[List of basic types|Prelude]] improvements
  -  [**#305**](https://github.com/anoma/nspec/pull/305): Add most of the types for RM specs
  -  [**#321**](https://github.com/anoma/nspec/pull/321): Add Runnable trait and make ordering engines parametric
  -  [**#329**](https://github.com/anoma/nspec/pull/329): Refactor type definitions to use simplified syntax

## [v0.1.3](https://specs.anoma.net/v0.1.3/)

The major change in this release is the gas payment system introduced in
[#286](https://github.com/anoma/nspec/pull/286), and the description of messages
in the Networking subsystem introduced in
[#294](https://github.com/anoma/nspec/pull/277).

### Fixes

- **Node architecture**
  -  [**#290**](https://github.com/anoma/nspec/pull/290): Fix english
    description for guards to match the Juvix types in [[Engine Behaviour]].
- **Repository maintenance and CI**
  -  [**#288**](https://github.com/anoma/nspec/pull/288): Improve primitive interfaces diagrams. Use LR mermaid option.
- **System architecture**
  -  [**#293**](https://github.com/anoma/nspec/pull/293): Fix formatting issues,
    typos, warnings, and broken links related to [[Proving system | Proving
    system definitions]].

- **Tutorial and documentation**
  -  [**#280**](https://github.com/anoma/nspec/pull/280): Guides: Add hard and soft
    requirements for writing pages in the Anoma Specification.
  -  [**#284**](https://github.com/anoma/nspec/pull/284): Add minimal version of
    the template (not visible in the website) and related refactors.

### Changes

- **Repository maintenance and CI**
  -  [**#296**](https://github.com/anoma/nspec/pull/296): Add next/prev buttons,
    fix footer, change font, add buttons to view/edit source code, and links to
    the GitHub repository.
- **Juvix types and updates**
  -  [**#294**](https://github.com/anoma/nspec/pull/294): Bump up Juvix version
    to v0.6.9 , reorder `MailboxID` alias, and update Stdlib to v0.9.0

### Features

- **Python-related changes**
  -  [**#291**](https://github.com/anoma/nspec/pull/291): Add new command tool
    `nspec` to create new engines based on the minimal version of the [[Template
    Engine]] files.
- **Repository maintenance and CI**
  -  [**#286**](https://github.com/anoma/nspec/pull/286): Incorporated gas
    payments description. Additionally, made several improvements such as
    switching to wiki-style links, adding icons, clarifying proof inputs, fixing
    rendering issues, and various other enhancements.
- **Tutorial and documentation**
  -  [**#292**](https://github.com/anoma/nspec/pull/292): Move template/template_minimum engines to
    docs/tutorial/engines folder. Update imports accordingly.


## [v0.1.2](https://specs.anoma.net/v0.1.2/)

Progress on translating the old specification to the new Juvix codebase, fixing
typechecking errors. Removed unsupported documents from the codebase. Building
specs no longer requires Juvix by default - use `PROCESS_JUVIX=true` flag with
mkdocs to process Juvix Markdown.

### Fixes

- **Node architecture**
  -  [**#235**](https://github.com/anoma/nspec/pull/235): Revisit [[Decryption Engine]]. Changes to the messages,
    environment, and behaviour types to conform the recent template changes.
  -  [**#236**](https://github.com/anoma/nspec/pull/236): Revisit [[Encryption Engine]] and [[Reads Engine]]. These are
    bundled since they rely on eachother's messages. Changes to the messages, environment, and behavior types to conform
    to the recent template changes
  -  [**#262**](https://github.com/anoma/nspec/pull/262): Update[[Engine writing
    conventions|writing conventions]], Fix [[Template Behaviour|template
    behaviour]] diagrams and update Mkdocs Na
  -  [**#263**](https://github.com/anoma/nspec/pull/263): To the [[Hardware
    Subsystem]] section, add [[Local Key Value Store Engine]] , [[Logging
    Engine]] and [[Local Time Series Storage Engine]], [[Wall Clock Engine]].
  -  [**#268**](https://github.com/anoma/nspec/pull/268): Add to [[Anoma Configuration]] section, the [[Identity Subsystem]].
  -  [**#269**](https://github.com/anoma/nspec/pull/269): Fix type error due to
    not making configs when spawning engines in [[Identity Management Engine]].
  -  [**#273**](https://github.com/anoma/nspec/pull/273): Replace X Machine by X
    Subsystem in the [[Node Architecture]] section.
- **Python-related changes**
  -  [**#271**](https://github.com/anoma/nspec/pull/271): update mkdocs juvix plugin v0.4.8
  -  [**#272**](https://github.com/anoma/nspec/pull/272): Update mkdocs juvix plugin v0.4.9
- **Repository maintenance and CI**
  -  [**#195**](https://github.com/anoma/nspec/pull/195): Optimize documentation build process and upgrade dependencies
  -  [**#262**](https://github.com/anoma/nspec/pull/262): Template fixes: diagrams, nav
  -  [**#266**](https://github.com/anoma/nspec/pull/266): Remove old
    documentation and update table of contents: Remove basic-abstractions,
    scope, applications, implementations, and several other files that were
    decided not to be included in this version of the specification.
- **Tutorial and documentation**
  -  [**#257**](https://github.com/anoma/nspec/pull/257): Add description of our
    [[Use Git and GitHub|Git workflow]] and new integration
    branches strategy.
  -  [**#265**](https://github.com/anoma/nspec/pull/265): Rename `TemplateCfg`
    to `TemplateLocalCfg`, add `TemplateCfg` similar to `TemplateEnv`, apply
    the same to `Ticker`.
  -  [**#274**](https://github.com/anoma/nspec/pull/274): Update engine writing
    conventions: [[Engine writing conventions|#update-the-table-of-contents]]
    and Table of Contents.
- **Juvix types and updates**
  -  [**#267**](https://github.com/anoma/nspec/pull/267): Fix all the type
    checking errors in engine definitions.

## [v0.1.1](https://specs.anoma.net/v0.1.1/)

Major revision of the engine definitions, the template, and the ticker engine.

### Features

- **Repository maintenance and CI**
  -  [**#217**](https://github.com/anoma/nspec/pull/217): Update template engine
    files to be more consistent, use backticks for Juvix terms/types in
    headlines, uncollapsed sections for type constructors arguments in template
    engine files, and auxiliary sections of Juvix code are always collapsed.

### Fixes

- **Node architecture**
  -  [**#219**](https://github.com/anoma/nspec/pull/219): Revisit [[Commitment Engine]]. Changes to the messages, environment, and behaviour types to conform the recent template changes.
  -  [**#253**](https://github.com/anoma/nspec/pull/253): Integration PR that
    combines multiple engine-related changes: [Engines: Use `ByteString` in
    crypto types #242](https://github.com/anoma/nspec/pull/242), [Engines:
    ByteString type definition #255](https://github.com/anoma/nspec/pull/255),
    [Engines: `EngineMsg` revision #241](https://github.com/anoma/nspec/pull/241),
    [EngineID: make `EngineName` compulsory #256](https://github.com/anoma/nspec/pull/256), [Engines: Engine type revision #244](https://github.com/anoma/nspec/pull/244), [ `EngineMsg`: add type param #258](https://github.com/anoma/nspec/pull/258), [Engines: add `GuardEval` and `ActionExec` #260](https://github.com/anoma/nspec/pull/260), and [Engines: Behaviour template revision #226](https://github.com/anoma/nspec/pull/226).
  -  [**#256**](https://github.com/anoma/nspec/pull/256): Make `EngineName`
    compulsory in `EngineID`.
- **Repository maintenance and CI**
  -  [**#218**](https://github.com/anoma/nspec/pull/218): Rename `EngineMessage`
     type to `EngineMsg` and `mkEngineMessage` to `mkEngineMsg`.
  -  [**#220**](https://github.com/anoma/nspec/pull/220): Fix the deployment of
     the latest version by deploying the website if the branch name is `main` or
     matches the semver pattern, and add information about the version and the
     commit hash to the title for reference.
  -  [**#222**](https://github.com/anoma/nspec/pull/222): Remove SML codebase as
    not used any more and any other reference in the markdown files
  -  [**#225**](https://github.com/anoma/nspec/pull/225): Fix navigation table
     for the identity component
  -  [**#227**](https://github.com/anoma/nspec/pull/227): Update Juvix version in Nix flake due to breaking changes, and
    also the input packages while at it.
  -  [**#250**](https://github.com/anoma/nspec/pull/250): Update policy on Juvix typechecking. The whole codebase in a
    PR should typecheck before merging
- **Tutorial and documentation**
  -  [**#257**](https://github.com/anoma/nspec/pull/257): Refactor the Git strategy: introduce integration PRs for
    better overview of complex changes
- **Juvix types and updates**
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

## [v0.1.0](https://specs.anoma.net/v0.1.0/)

This is the first release of Anoma's Spec project, following the [[Versioning|semantic-versioning]] scheme.
This version includes all the changes from the creation of this repository. From
here on, we will keep a changelog of all the changes that are made to the
project per version, with better documentation and descriptions of the changes.

### Breaking changes

- **Node architecture**
  - [**#179**](https://github.com/anoma/nspec/pull/179): Reorganize node architecture
    documentation structure
  - [**#192**](https://github.com/anoma/nspec/pull/192): Port identity engines to v2 template
- **System architecture**
  - [**#210**](https://github.com/anoma/nspec/pull/210): Fix engine message, environment and
    behavior layout
- **Repository maintenance and CI**
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

### Bug fixes

- **Repository maintenance and CI**
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

### Features

- Application documentation
  - [**#198**](https://github.com/anoma/nspec/pull/198): Add transparent RM implementation documentation
- **Python-related changes**
  - [**#133**](https://github.com/anoma/nspec/pull/133): Add support for multi-line wiki-style links
- **Repository maintenance and CI**
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
- **Tutorial and documentation**
  - [**#134**](https://github.com/anoma/nspec/pull/134): Refactor tutorial for wiki-style links
- **Juvix types and updates**
  - [**#128**](https://github.com/anoma/nspec/pull/128): Add new Juvix definitions from PR-84
  - [**#130**](https://github.com/anoma/nspec/pull/130): Translate SML Identity definitions to Juvix
