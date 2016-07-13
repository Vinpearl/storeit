Workflow
--------

### Introduction
The idea behind this proposal is to completely achieve an Agile-like workflow. Feel free to give or opinion about it.

Thanks to Waffle we now have Kanban boards which is a great improvement. As a summary it allows us to:
* sync Github issues with Waffle cards in the *To Do* column
* move issues to *In Progress* with branches
* link issues to pull requests to *Review*
* archive finished tasks (ie: merged PR) in *Done*

To take benefit of the synchronization with Waffle, please follow the guidelines below.

### New issue

* Create a Waffle card in the **To Do** column, or alternatively write a new Github issue 
* Flag it with the **bug** label or the **feature** label depending on its nature
* Use the label(s) associated to the part it's related with (ex: android, ios...)
* Assign it to the correct person
* Associate it with a milestone

### Work on an issue

1. Create your local dev branch with: `git checkout -b <label>/#<issue_number>-<type> [start_commit]`
2. Create the branch on the remote: `git push -u origin <label>/#<issue_number>-<type>`

Where label can be one of the following:
* server
* desktop
* android
* ios
* web
* site

And type one of the following:
* feat
* fix

This will automatically move the Waffle card in the **In Progress** column.

Example: 
``` bash
git checkout -b android/#1-feat master # switch to new branch feature/#1 which starts at master
git push -u origin android/#1-feat # create the new branch on the server
# work on your branch !
```

### Request merge in master
1. Resolve possible conflicts with master branch: `git pull --rebase origin master`
2. Once ready for merge, submit a pull request using the proper Github keywords in its title (example: `close #1`)

**Tip**: if you want to be lazy, you should know that the last commit message on your branch can be reused as the PR title since it will be the default title.

This will automatically move the Waffle card in the **Review** column.

### Review

Finally, once a PR have been reviewed, it will be merged in master.
The associated issue is closed and card is automatically moved to the **Done** column.
Dev branches should be deleted once merged.
