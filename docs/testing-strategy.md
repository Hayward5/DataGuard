# DataGuard Rebuild Testing Strategy

## Week 7 Testing Goals

Week 7 emphasizes software testing evidence over feature breadth.

### Methods Used

- TDD: Every new production module starts with a failing test.
- Equivalence Class Testing: CSV/JSON/JSONL parsing, required fields, string/integer validation.
- Boundary Value Testing: integer min/max and string length edges.
- Input Space Partitioning: valid / invalid / edge fixtures for `validate`.
- Integration Testing: one end-to-end `validate` smoke flow.

## Week 7 Deliverables

- parser unit tests
- schema/validator unit tests
- CLI argument contract tests
- one validate integration test
- coverage report
