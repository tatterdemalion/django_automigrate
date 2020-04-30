### automigrate

This script lets you undo migrations in your current branch, switch to target branch and run migrations on that branch.

#### Usage:

```
automigrate.py <target_branch>

```

if you want to use your local installation instead of Docker, set `$AUTOMIGRATE_LOCATION` environment variable to `local` before running the script.

**Important:** Keep in mind you should commit all your migrations before this.
