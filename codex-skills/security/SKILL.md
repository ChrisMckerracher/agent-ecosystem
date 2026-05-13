---
name: security
description: Use when auditing code for vulnerabilities, reviewing auth/authz/crypto/secrets/dependency changes, or before merging security-sensitive work.
---

# Security

Use this skill for security review. Security findings can block merge when risk is critical.

## Review Targets

- Authentication, authorization, sessions, permissions, tenancy, secrets, cryptography, payment, webhooks, input validation, file upload, SSRF, deserialization, dependency changes, and infrastructure config.
- Any change that affects trust boundaries or sensitive data flow.

## Workflow

1. Read the diff, linked design, relevant standards, and existing security notes.
2. Map entry points, trust boundaries, data stores, auth checks, and privilege transitions.
3. Use `$spelunk --for=security --focus="<area>"` when source context is broad or reusable docs would help.
4. Check OWASP Top 10 classes, secrets, dependency vulnerabilities, insecure defaults, logging of sensitive data, and missing validation.
5. Verify tests cover security-critical behavior or request follow-up tests.
6. Return approve/block with severity, exploit path, and fix guidance.

## Spelunk Inputs

Security-focused spelunk should produce:

- `docs/spelunk/trust-zones/<focus>.md`
- `docs/spelunk/contracts/<focus>.md`

Use these reports to verify auth flow, validation boundaries, and protected resource access.

## Severity

- Critical: exploitable auth bypass, secret exposure, remote code execution, data exfiltration, or privilege escalation.
- High: likely exploitable validation, authorization, injection, or sensitive data flaws.
- Medium: defense-in-depth gaps, incomplete tests, unsafe patterns with limited exploitability.
- Low: hardening and hygiene issues.

## Output

Findings first, with file/line references and concrete impact. Include a veto/block statement for critical issues and list verification performed.
