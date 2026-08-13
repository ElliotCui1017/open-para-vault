# Public Release Checklist

## Privacy and history

- [x] Public tree was created by allowlist in a new Git repository.
- [x] Maintainer private notes, attachments, credentials, and local state are excluded.
- [x] No personal absolute paths remain in the public tree.
- [x] Demo content is fictional.
- [ ] Maintainer has reviewed every commit in the new public history.
- [ ] `python scripts/preflight_public.py .` passes immediately before push.
- [ ] `python scripts/validate_repo.py .` passes immediately before push.

## Usability

- [x] README explains the project and quick start.
- [x] Setup supports demo and private-vault installation.
- [x] One capture-to-archive workflow is documented.
- [x] Templates and optional automation are documented.
- [ ] Instructions have been tested by a second person on a clean machine.

## Open-source hygiene

- [x] License, contribution, security, and conduct files exist.
- [x] Issue and pull request templates exist.
- [x] Changelog, roadmap, release notes, and initial issues exist.
- [x] CI runs publication checks.
- [ ] GitHub repository owner, name, description, and topics are confirmed.

## Release

- [ ] Add the intended public remote.
- [ ] Push only the clean repository.
- [ ] Confirm the default branch and branch protection.
- [ ] Tag `v0.1.0` after CI passes.
- [ ] Publish the GitHub Release using `RELEASE_NOTES_v0.1.0.md`.
- [ ] Create selected issues from `docs/initial-issues.md`.
