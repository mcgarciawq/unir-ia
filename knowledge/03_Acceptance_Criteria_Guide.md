# Acceptance Criteria Guide

## Purpose

Acceptance criteria define the conditions that must be satisfied before a user story can be considered successfully implemented.

They provide a shared understanding between business stakeholders, developers and testers.

Acceptance criteria eliminate ambiguity and allow objective validation of delivered functionality.

Although acceptance criteria are not part of the user story itself, they should always be considered while writing the story.

---

# Characteristics of Good Acceptance Criteria

Acceptance criteria should be:

- clear;
- concise;
- measurable;
- testable;
- understandable by both technical and business teams.

Each criterion should describe observable system behavior rather than implementation details.

---

# Functional Behaviour

Acceptance criteria describe what the system should do.

Examples include:

- displaying information;
- validating user input;
- storing business data;
- sending notifications;
- calculating business values;
- preventing invalid operations.

They should never describe internal implementation.

---

# Business Rules

Business rules should appear as acceptance criteria whenever they affect system behaviour.

Examples:

- only administrators may delete users;
- inactive accounts cannot authenticate;
- mandatory fields must always be completed;
- duplicate identifiers are not allowed.

Business rules help developers understand expected behaviour.

---

# Error Handling

Acceptance criteria should consider common error situations.

Examples include:

- invalid credentials;
- missing required information;
- unavailable resources;
- duplicated records;
- insufficient permissions.

Considering exceptional situations improves software quality.

---

# Validation

Acceptance criteria should allow objective verification.

The implementation should clearly satisfy or fail each criterion.

Avoid vague expressions such as:

- user-friendly;
- fast enough;
- intuitive;
- modern.

Instead, describe observable outcomes.

---

# Common Structure

Acceptance criteria often follow a simple structure.

Given a specific situation,

When the user performs an action,

Then the system produces an expected result.

This structure helps maintain consistency and simplifies testing.

---

# Relationship with User Stories

A user story describes:

- who needs the functionality;
- what functionality is requested;
- why the functionality provides value.

Acceptance criteria describe:

- how success will be evaluated.

Both elements complement each other.

---

# Common Mistakes

Avoid criteria that:

- describe database design;
- specify APIs;
- mention frameworks;
- define programming languages;
- include implementation details.

Acceptance criteria focus on externally observable behaviour.

---

# Quality Checklist

Good acceptance criteria:

✓ describe expected behaviour;

✓ can be objectively verified;

✓ cover normal and exceptional scenarios;

✓ support testing activities;

✓ reduce misunderstandings during development;

✓ improve communication between stakeholders and developers.
