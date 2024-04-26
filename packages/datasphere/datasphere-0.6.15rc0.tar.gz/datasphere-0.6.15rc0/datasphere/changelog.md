# 0.7.0 (2024-04-19)

- Added support for directories as input and output files.
- Added `fork` command, which allows to use another job as a template, overriding input/output files, environment
  variables, docker image, working storage or cloud instance type.

# 0.6.12 (2024-04-03)

- Added commands to get and list projects – `project get`, `project list`.
- Added options for command output – `-o` to specify output file path (stdout by default) and `--format` to specify
  data format (tabular or json).

# 0.6.11 (2024-03-25)

- Support use case when main script is not in current working directory.
