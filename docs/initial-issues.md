# Initial GitHub Issues

These issues describe genuine follow-up work after `v0.1.0`. Copy a section into a separate GitHub issue only when the maintainer is ready to schedule that work.

## test: render templates and validate generated frontmatter

**Problem**

The current structural validator checks source templates but does not render Obsidian placeholders into finished notes.

**Scope**

Build a standard-library test fixture that substitutes deterministic title/date values, parses the resulting frontmatter subset, and verifies required properties for each template type.

**Acceptance criteria**

- covers every file in `templates/`;
- reports the template path and missing/invalid property;
- runs on Windows, macOS, and Linux;
- adds no private fixtures or heavyweight runtime dependency.

## test: verify QuickAdd example compatibility

**Problem**

QuickAdd's internal configuration schema can change, and the repository does not run the plugin itself.

**Scope**

Document a repeatable compatibility check against a supported QuickAdd release and decide whether UI setup instructions should remain primary.

**Acceptance criteria**

- starts from a disposable fictional vault;
- verifies both example capture choices append correctly;
- records the tested plugin release without vendoring plugin code;
- contains no provider key, auth state, or machine-specific path.

## ci: exercise bootstrap behavior across platforms

**Problem**

The bootstrap helper is PowerShell-based, while CI currently validates only the repository content on Linux.

**Scope**

Add a CI matrix that creates an empty temporary destination, runs the bootstrap helper, and validates the result without configuring a remote.

**Acceptance criteria**

- covers Windows and at least one Unix runner;
- confirms `.git` from the source is never copied;
- confirms non-empty and in-source destinations fail safely;
- leaves no published artifact or external side effect.

## feat: generate a downloadable starter vault

**Problem**

Non-Git users would benefit from a release artifact that can be opened directly in Obsidian.

**Scope**

Generate a zip from `examples/demo-vault/` during release CI rather than committing binary archives.

**Acceptance criteria**

- artifact is generated from a tagged source tree;
- preflight and structural validation run before packaging;
- archive contains no workspace state, plugin binary, or credential-bearing file;
- installation steps are added to the release notes.
