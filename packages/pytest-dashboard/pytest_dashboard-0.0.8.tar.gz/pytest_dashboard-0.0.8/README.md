# pytest-dashboard

## usage
`python -m pytest`
by this command, you get `[datetime]-progress.yaml` file on working directory as realtime pytest progress report.

`python -m pytest --progress-path=[path/to/some-progress.yaml]`
by this command, you get `path/to/some-progress.yaml` file.

`python -m pytest-dashboard.tally PROGRESSES_DIR --entire_progress_path=[path/to/entire-progress.yaml]`
by this command, you get started to monitor changes of
the progress files (ends with `-progress.yaml`)
inside `PROGRESS_DIR` and save the state summary
to `path/to/entire-progress.yaml`.

So it is necessary to set `--progress-path` option of pytest
ending with `-progress.yaml`.
For example, `2024-04-22-progress.yaml`,

> **Note**
> if your `entire_progress_path` is ends with `-progress.yaml`,
> you cannot save the entire progress file to
> the same directory with each progress file.


`python -m pytest_dashboard.tally PROGRESS_DIR --notification=True`
By this command, you will get mail notification when entire progress is finished.
> **Note**
> Please make and implement pytest_dashboard.config
> that contains information abaout mail address and SMTP server.


`python -m pytest_dashboard.launch_pytest_dashboard`
NOT IMPLEMENTED!
