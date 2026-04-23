# Mirror World Fixture Corpus

These fixtures are the first smoke-test corpus for the art-first public prototype.

They are not model benchmarks.

They are stable world seeds used to answer one question:

`Did we break the expected shape and feel of the world experience?`

## Fixture goals

- give backend and frontend the same seeded worlds
- make contract snapshots reviewable
- keep founder demos stable during heavy iteration

## Current fixtures

- `campus-public-opinion.json`
- `brand-crisis-response.json`
- `literary-branching-world.json`
- `manifest.json`

## Minimum smoke expectations

Every fixture should be able to produce:

- a world headline
- at least 3 key events
- at least 1 primary branch and 2 alternate branches on a key event
- at least 1 intervention path
- at least 1 consequence payload

## Usage

Short term:

- use these fixtures for manual founder demos
- use them for contract snapshots
- use them as smoke-test seeds when new APIs land

Longer term:

- wire them into automated smoke tests
- store expected event and branch snapshots beside them
