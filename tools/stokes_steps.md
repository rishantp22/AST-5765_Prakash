# Finish the required Stokes and GitHub steps

Prepared with Codex assistance on 9 September 2026. These are instructions,
not a claim that the remote actions have happened. Keep the master work log
open and append actual commands, dates, results, errors and job IDs as you go.

## GitHub

The student created `rishantp22/AST-5765_Prakash`, and it was made **private**
with explicit approval. GitHub CLI authentication completed on this Mac.
The local repository contains course materials and homework, and its origin is
`https://github.com/rishantp22/AST-5765_Prakash.git`. Do not create another
repository or add another origin. The initial commit is `84cc8f1`.

Repository-local author settings are already configured with Rishant Prakash
and GitHub's no-reply email derived from the verified account ID. For future
changes, run:

```bash
cd /Users/cosmic-rishant/Desktop/HW_AST_5765C/ast5765
git add .gitignore 0-ast5765-prakash.log homework tools
git commit -m 'Describe the changes you made'
git push origin master
git status
git log --oneline -5
```

If `origin` already exists, inspect it with `git remote -v` before changing it.
Do not put passwords or tokens in commands, logs or screenshots. The handout's
username/password authentication uses a personal access token in the password
prompt, not the GitHub account password. GitHub Desktop or GitHub CLI browser
authentication is another option. A browser login alone does not authenticate
command-line Git.

Capture actual terminal output of `git status` for HW1 as
`homework/hw1_prakash/hw1_prakash_problem2_git.png`.
For HW2, show `pwd`, `ls homework/hw2_prakash`, `git log --oneline -5`, and
`git status` after a successful commit and push. Save a genuine screenshot as
`homework/hw2_prakash/hw2_prakash_problem6_git_history.png`.
On macOS, Command-Shift-4 then Space captures a window. Move the saved PNG
from your Desktop to the appropriate homework folder and log the method.
Add the screenshots and updated log in another commit and push.

## Connect to Stokes and capture HW1 evidence

The instructor's August 30 announcement says course accounts are already
created; **do not submit a new registration request**. Use UCF internet or
connect to the UCF VPN when necessary. The Stokes server was reachable from
this Mac during verification. The student supplied NID `ri061277`.

To authenticate for this assisted session, run in your own Terminal:

```bash
bash /Users/cosmic-rishant/Desktop/HW_AST_5765C/ast5765/tools/connect_stokes.sh ri061277
```

Enter your password only at the SSH prompt and leave that window open.
The helper allows subsequent authorized commands to reuse the connection
without exposing the password. An ordinary login for future sessions is:

```bash
ssh ri061277@stokes.ist.ucf.edu
hostname
pwd
ls
```

Complete password/MFA prompts yourself. The course announcement only
requires a screenshot after login for HW1; the diagnostic commands above are
optional. Capture the real remote terminal as `hw1_prakash_problem3_stokes.png`, place it in the local HW1 folder,
and append the successful login and screenshot details to the master log.
Never substitute a local `ls` screenshot for Stokes evidence.

## Create the Stokes Python environment

Follow the supplied `stokes_setup/stokes_updated.txt`, with `ast5765` as the
environment name. The local verified Python version is 3.14.7. On Stokes:

```bash
module load anaconda
srun --pty bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda create -n ast5765 python=3.14.7
conda activate ast5765
conda install numpy scipy matplotlib pandas
python --version
python -c 'import numpy, scipy, matplotlib, pandas; print("Imports passed")'
exit
exit
```

The first exit leaves the compute allocation; the second returns to your Mac.
Inspect `conda env list` first if you already created the environment; do not
recreate or overwrite it. If that Python version or module is unavailable,
record the error and use a version approved by course staff. Use
`module avail anaconda` to identify the available module. If a qualified module
name is required, update the `module load` line in `hw2_prakash.slurm` as well.
The current ARCC guide requires compute-node access for installations.

## Copy HW2 and run it through Slurm

From your Mac:

```bash
cd /Users/cosmic-rishant/Desktop/HW_AST_5765C/ast5765
ssh ri061277@stokes.ist.ucf.edu 'mkdir -p ~/hw2_prakash'
scp -r homework/hw2_prakash/. ri061277@stokes.ist.ucf.edu:~/hw2_prakash/
ssh ri061277@stokes.ist.ucf.edu
cd ~/hw2_prakash
sbatch hw2_prakash.slurm
```

Record the returned job ID, then inspect the job using your actual ID:

```bash
squeue -j YOUR_JOB_ID
sacct -j YOUR_JOB_ID --format=JobID,State,ExitCode
cat hw2_prakash_stokes-YOUR_JOB_ID.out
cat hw2_prakash_stokes-YOUR_JOB_ID.err
ls -lh hw2_prakash_problem3_sine.png hw2_prakash_problem4_ramp.pdf
```

Only mark the Stokes test complete when the job reports COMPLETED and exit
code 0:0 and both figures exist. Debug any nonzero exit before packaging.
The instructor's unmodified `test.py` is also in `handouts/stokes_setup/` and
was tested locally; it may be copied and submitted in the same way as a smoke
test. The homework job must run `hw2_prakash.py`, not just `test.py`.

## Record plans, close the log, copy it, then archive

In the master log explain the copy, archive, download and Webcourses steps
**before** copying the log. Include actual local/Stokes results, Git commit
IDs, screenshot filenames and AI disclosure. Close the entry with an OUT
timestamp. Make the latest log copy locally and on Stokes:

```bash
# Mac
cd /Users/cosmic-rishant/Desktop/HW_AST_5765C/ast5765
cp -p 0-ast5765-prakash.log homework/hw2_prakash/
scp 0-ast5765-prakash.log ri061277@stokes.ist.ucf.edu:~/hw2_prakash/
ssh ri061277@stokes.ist.ucf.edu
```

On Stokes, use a new archive name if preserving an earlier submission:

```bash
cd ~
tar -czvf hw2_prakash.tar.gz \
  --exclude='__pycache__' --exclude='.ipynb_checkpoints' \
  --exclude='.DS_Store' hw2_prakash
tar -tzf hw2_prakash.tar.gz
exit
```

From your Mac, only download into a new, unoccupied archive path:

```bash
cd /Users/cosmic-rishant/Desktop/HW_AST_5765C/ast5765
scp ri061277@stokes.ist.ucf.edu:~/hw2_prakash.tar.gz handin/
tar -tzf handin/hw2_prakash.tar.gz
```

Upload that archive to the HW2 assignment in Webcourses, click Submit, and
verify the submission receipt. Save the receipt separately and append a new
log entry; never rewrite the already submitted archive. HW1 is the exception
that requests **ZIP**. Once its missing screenshots exist, copy the closed
log into `homework/hw1_prakash/` and use:

```bash
cd /Users/cosmic-rishant/Desktop/HW_AST_5765C/ast5765
cp -p 0-ast5765-prakash.log homework/hw1_prakash/
cd homework
zip -r ../handin/hw1_prakash.zip hw1_prakash \
  -x '*/.ipynb_checkpoints/*' '*/__pycache__/*' '*/.DS_Store'
```

Use an unused archive name to preserve earlier handins. Upload the resulting
ZIP to HW1. Its PDF due date was August 31; the syllabus says no late work is
accepted. Submission availability or an exception must be verified in the
course, not assumed.

Sources: supplied HW1/HW2 PDFs; `github_updated_instructions.pdf`;
`worklog_instructions.pdf`; `homework_format_rules_25.pdf`;
`stokes_setup/stokes_updated.txt`; UCF ARCC, 2026 (accessed 2026-09-09):
https://arcc.ist.ucf.edu/docs/access/linux/ and
https://arcc.ist.ucf.edu/docs/software/anaconda/ .
