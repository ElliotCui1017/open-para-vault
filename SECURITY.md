# Security and Privacy Policy

## Reporting a vulnerability

Please avoid posting exploitable vulnerabilities, secrets, or private user data in a public issue.

When reporting a bug publicly, provide a minimal fictional reproduction.

## Sensitive content

This project is designed around a strict separation between public system components and private knowledge content.

Never commit:

- API keys;
- OAuth tokens;
- passwords;
- session cookies;
- SSH keys;
- private certificates;
- `.env` files;
- exported browser profiles;
- personal vault contents;
- real identity, health, finance, employment, academic, or contact records.

## Accidental secret publication

If a secret is committed:

1. revoke or rotate the secret immediately;
2. remove the secret from the current tree;
3. rewrite Git history if the repository has already been pushed;
4. assume the old secret is compromised even after history is rewritten.

Deleting a file in a later commit does not remove it from earlier Git history.
