# pytest-dashboard

## usage
`python -m pytest`
by this command, you get `[datetime]-progress.yaml` file on working directory as realtime pytest progress report.

`python -m pytest --progress-path=[path/to/some-progress.yaml]`
by this command, you get `path/to/some-progress.yaml` file.

`python -m pytest-dashboard.tolly PROGRESSES_DIR --entire_progress_path=[path/to/entire-progress.yaml]`
by this command, you get started to monitor changes of
the progress files (ends with `-progress.yaml`)
inside `PROGRESS_DIR` and save the state summary
to `path/to/entire-progress.yaml`.

So it is recommended to set `--progress-path` option of pytest
ending with `-progress.yaml`.
For example, `2024-04-22-progress.yaml`,

> **Note**
> if your `entire_progress_path` is ends with `-progress.yaml`,
> you cannot save the entire progress file to
> the same directory with each progress file.

`python -m pytest_dashboard.tolly --progress-dir=[dir/contains/progress.yaml_files]`
by this command, you monitor -progress.yaml files
inside `dir/contains/progress.yaml_files`
and continurous update to tolly them
to `--entire-progress-path` (optional, default to `entire-progress.yaml`) file.

`python -m pytest_dashboard.launch_pytest_dashboard`
NOT IMPLEMENTED!
