# CloudShield Detection Rules

## Rule 001 — Brute Force Detection

### Objective

Detect repeated failed authentication attempts originating from
the same source IP within a short period of time.

### Detection Logic

Trigger a brute-force alert when:

- The event type is `login_failed`
- More than 5 failed login attempts occur
- The attempts originate from the same source IP
- The attempts occur within a 2-minute window

### Severity

HIGH

### Example

6 failed login attempts from:

`192.168.1.42`

within 2 minutes.

### Alert

Type: Brute Force Attack  
Severity: HIGH

### Recommended Investigation

- Investigate the source IP
- Identify the targeted account
- Review surrounding authentication events
- Check whether a successful login occurred after the failures
- Determine whether the activity is legitimate or malicious