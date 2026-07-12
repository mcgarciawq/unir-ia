# Story Point Estimation Guide

## Purpose

This document defines the organization's internal approach for estimating user stories.

Story points represent the relative effort required to implement a feature.

The estimation considers three factors simultaneously:

- implementation effort;
- technical complexity;
- uncertainty.

Story points should never be interpreted as development hours.

---

# Estimation Scale

The organization uses the following Fibonacci-based scale:

- 1
- 2
- 3
- 5
- 8

Larger values indicate greater effort and uncertainty.

Stories requiring more than 8 story points should normally be divided into smaller stories.

---

# Story Point Definitions

## 1 Story Point

Very small improvement.

Characteristics:

- minimal implementation effort;
- almost no uncertainty;
- isolated change;
- limited testing required.

Typical examples:

- update a label;
- add a simple validation;
- modify a report column.

Estimated effort:

2–4 hours.

---

## 2 Story Points

Small feature.

Characteristics:

- limited business logic;
- few dependencies;
- straightforward implementation.

Typical examples:

- create a basic form;
- add a filter;
- export a small report.

Estimated effort:

4–8 hours.

---

## 3 Story Points

Medium-sized functionality.

Characteristics:

- several business rules;
- moderate testing effort;
- interaction with multiple components.

Typical examples:

- manage user profiles;
- upload documents;
- configure notifications.

Estimated effort:

8–16 hours.

---

## 5 Story Points

Large feature.

Characteristics:

- multiple business rules;
- moderate technical complexity;
- several integration points;
- extensive testing.

Typical examples:

- implement user management;
- create approval workflows;
- generate analytical dashboards.

Estimated effort:

16–24 hours.

---

## 8 Story Points

Very large feature.

Characteristics:

- high uncertainty;
- significant business impact;
- complex workflow;
- multiple integrations;
- increased implementation risk.

Examples:

- complete authentication module;
- payment processing;
- enterprise reporting system.

Estimated effort:

24–40 hours.

Stories larger than this should normally be divided into multiple user stories.

---

# Factors That Influence Estimation

When estimating a story, consider:

- business complexity;
- number of business rules;
- integration with existing modules;
- uncertainty;
- testing effort;
- security requirements;
- expected validation effort.

Avoid estimating based solely on implementation time.

---

# Consistency

Stories with similar complexity should receive similar story point values.

Consistency across the project is more important than perfect precision.

---

# Estimation Best Practices

Always estimate:

- functionality;
- complexity;
- uncertainty;
- validation effort.

Do not estimate:

- individual developer speed;
- overtime;
- deadlines;
- team availability.

---

# Quality Checklist

A well-estimated story:

✓ has realistic story points;

✓ has proportional effort hours;

✓ reflects implementation uncertainty;

✓ considers business complexity;

✓ can be completed within a sprint.
