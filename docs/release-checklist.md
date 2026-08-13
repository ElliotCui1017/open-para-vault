# Public Release Checklist

## Privacy and history

- [x] Public tree was created by allowlist in a new Git repository.
- [x] Maintainer private notes, attachments, credentials, and local state are excluded.
- [x] No personal absolute paths remain in the public tree.
- [x] Demo content is fictional.
- [x] Maintainer has reviewed every commit in the public history.
- [x] Maintainer Git author and committer metadata use the GitHub noreply identity.
- [x] `python scripts/preflight_public.py .` passes on the current public history.
- [x] `python scripts/validate_repo.py .` passes on the current tree.

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
- [x] GitHub repository owner and name are confirmed.
- [ ] Repository description and topics are confirmed in GitHub settings.

## Release

- [x] Add the intended public remote.
- [x] Push only the clean repository.
- [x] Confirm `main` as the default branch.
- [ ] Decide whether branch protection is appropriate for the initial release.
- [x] Tag and publish the frozen `v0.1.0` release.
- [ ] Confirm the target release-notes file exists before creating a new version tag.
- [ ] Confirm the deterministic starter ZIP and checksum reproduce locally.
- [ ] Create the version tag only after CI and maintainer review.
- [ ] Review the workflow-created Draft Release and its matching-tag assets.
- [ ] Publish the GitHub Release manually after verifying its notes and checksum.
- [ ] Create selected issues from `docs/initial-issues.md`.
