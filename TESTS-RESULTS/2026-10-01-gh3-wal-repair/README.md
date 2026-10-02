# Cold WAL reader repair

The extended existing readonly case fails against the old helper with Apple SQLite unable to open a cold file created by Homebrew SQLite. The candidate passes under both interpreters. DELETE refusal and missing-file noncreation remain asserted. Tests use synthetic temporary homes in a disposable full clone. Independent final QA and full gates are pending.
