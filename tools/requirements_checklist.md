# Homework completion audit - 9 September 2026

**Local HW2 solution complete. Remote and submission requirements pending.**
This file reports verified actions, not an estimate of a grade.

## Course materials reviewed

All 34 original supplied files were inventoried. All 16 PDFs were read by
text extraction; the image-only HW1 sheet was also rendered and visually
read. The cumulative log, software scripts, Slurm template, test program,
lecture notebooks and module examples were inspected. Original file hashes are
saved in the parent `audit/all_original_files.json`.

Primary requirements: Fall 2026 syllabus; `hw1_the_installations_f26.pdf`;
`hw2_python_refresh_f26.pdf`; homework format and worklog handouts; Anaconda,
GitHub and Mac installation instructions; updated GitHub and Stokes notes.

## HW1 - laptop setup

The assignment-specific format is **ZIP**, overriding the general tar.gz rule.
Its listed deadline was Monday, August 31, 2026 at 2:30 pm.

| Requirement | Status and evidence |
| --- | --- |
| 1. Create homework folder and start log | Done: `homework/hw1_prakash/`; appended session in master log |
| 2a. Launch Python environment; report version; save screenshot | Done: Python 3.14.7; executed `hw1_prakash_environment.ipynb`; actual `hw1_prakash_problem2_python.png` |
| 2b. GitHub Desktop or terminal `git status` screenshot | Git installed, repository initialized; exact screenshot still pending |
| 3. Log into Stokes and save screenshot | Pending password authentication; August 30 announcement confirms course accounts exist and waives typing commands for HW1 |
| 4. Explain log copy, ZIP creation and Webcourses submission | Instructions prepared in master log and `stokes_steps.md`; actual submission pending |
| Final closed log copy and ZIP | Local draft packaging only until missing evidence is added |

## HW2 - Python practice

The assignment-specific format is a **tar.gz created on Stokes**.
The listed deadline is Wednesday, September 9, 2026 at 2:30 pm.

| Requirement | Status and evidence |
| --- | --- |
| 1. Folder, main .py, identifying header, problem numbers | Done: `homework/hw2_prakash/hw2_prakash.py`; prints Problems 1-7 |
| Commit and push periodically | Done: initial commit `84cc8f1` pushed to private `rishantp22/AST-5765_Prakash` |
| 2a. Integers 0 through 1000, count, dtype, min/max | Done: 1001 elements; int64; bounds 0 and 1000 |
| 2b. Rescale existing x variable to 0 through 2*pi | Done with explicit float dtype promotion then in-place scaling; bounds 0 and 6.283185307179586 |
| 2c. Compute sine array | Done, vectorized |
| 2d. Print element 234, distinguish ordinal counting | Done: y[234] = 0.994951016981300; index 234 is the 235th element |
| 3a. Publication-ready sine plot | Done: labeled axes, radians, pi ticks and readable styling |
| 3b. Save PNG from Python, not a screenshot | Done: `hw2_prakash_problem3_sine.png` |
| 4a. Ramp with 101 points; clip to +/-0.5 without loops | Done: original preserved; clipping in place; spacing 0.02 |
| 4b. Original and clipped curves on one plot; save PDF | Done: `hw2_prakash_problem4_ramp.pdf` |
| 5. Two free Python astronomy packages, URLs and paragraphs | Done: Astropy and Photutils; cited sources; printed triple-single-quoted string |
| 6a-6d. Stokes login, folder, transfer and execution | Pending password authentication; Stokes is reachable; Slurm file and steps prepared |
| 6e-6f. Git commit/push explanation and history screenshot | Done locally: actual pushed commit, folder screenshot and history screenshot; copies still need transfer to Stokes |
| 6g. Copy all required files to Stokes | Pending authenticated Stokes connection |
| 6h. Explain log copy, archive, download and upload | Prepared in `stokes_steps.md` and master log |
| 6i. Copy closed log and create tar.gz on Stokes | Pending authenticated Stokes connection; a local draft is not this requirement |
| 7. Submit to Webcourses and verify receipt | Not performed |

## Validation performed

- Main HW2 source has no for/while loops or comprehensions and no lines over
  80 characters. It has no notebook-only magic commands or external data paths.
- A source-only copy ran from a fresh directory. Endpoint, cardinal-point,
  index, spacing, clipping and output-file checks passed.
- Both figures were visually checked, including a Poppler render of the PDF.
- The instructor's unchanged `test.py` ran locally and printed its success
  message. A local test is not a Stokes test.
- Original source hashes and original HW0 log bytes were preserved.

## Installation decisions and handout differences

- This is an Apple Silicon Mac. Windows WSL, Windows MobaXterm, Ubuntu BIOS
  and VirtualBox instructions are alternative platform paths, not required
  installations for the native macOS route used here.
- `/opt/anaconda3` already has all required scientific packages, Jupyter and
  Spyder. A reinstall or a full update of unrelated packages was unnecessary.
- Git 2.39.5 and Apple Command Line Tools already work. Homebrew is absent;
  it is not needed to reinstall already working Git or use Jupyter.
- VS Code is installed; Jupyter is the chosen editor. Emacs is an alternative.
- Existing `.bash_prePHZ3150` backup and `.bash_aliases` were found and left
  intact. The task did not overwrite the prior backup. The course launcher
  selects the working Python without rewriting global shell configuration.
- The class notebook explicitly says DS9/pyds9 is optional. No extra image
  viewer, VM or operating system was installed.
- The old `unix_github.pdf` contains a malformed example remote URL; the
  actual verified repository URL is used instead.
- The original Slurm example uses the TA's NID and `test.py`; the prepared
  HW2 Slurm file activates a named environment and runs `hw2_prakash.py`.

## Readings and other files

The Matplotlib tutorial and NumPy-100 repository were opened and reviewed as
resources. Practice exercises are separate from the homework hand-in.
The course specifically says not to hand in those exercises. The initially missing `pydatatut` tutorial was located in Webcourses
`Files/Demos_lectures/week_2/pydatatut/`. Its rendered text was saved for
review, and a public NRAO mirror was saved in `literature/pydatatut_NRAO.pdf`.
Chapters 1-2 were reviewed; see `literature/pydatatut_reading_notes.md`. The
Webcourses example files were located but not successfully downloaded.

The L04 work and filled-in notebooks are classroom references, including
intentional error demonstrations, optional DS9 cells and incomplete practice
cells. They were preserved, not relabeled as homework submissions. The
`Pi_approx.ipynb` is an existing lecture exercise; no separate grading prompt
for it was supplied. The existing HW0 log and ZIP remain unchanged.
The syllabus lists later assignments, but no HW3+ problem sheets were supplied;
their questions and due-date changes cannot be invented from schedule titles.

Resources reviewed (accessed 2026-09-09):

- Matplotlib Development Team (2026): https://matplotlib.org/stable/tutorials/pyplot.html
- Nicolas P. Rougier and contributors (ongoing): https://github.com/rougier/numpy-100
- NumPy Developers (2026): https://numpy.org/doc/stable/reference/
- Astropy Developers (2026): https://docs.astropy.org/en/stable/
- Photutils Developers (2026): https://photutils.readthedocs.io/en/stable/
- UCF ARCC (2026): https://arcc.ist.ucf.edu/docs/access/

## Current Webcourses and Stokes update

The signed-in course assignments page currently lists HW0, HW1 and HW2.
HW0 has already been graded. HW1 and HW2 show no submission. Two required
HW0 peer-review links also appear; no peer reviews were opened or sent here.
HW2's assignment page confirms the 2026-09-09 14:30 deadline and requires
`.tar.gz` even though the upload field accepts the final `.gz` extension.

Joseph Harrington's **August 30 announcement** says he already requested the
course Stokes accounts and staff completed them. **Do not submit a new account
request.** It also says HW1 only requires a screenshot after login; no remote
commands are required. This supersedes the earlier generic registration advice.
Source: https://webcourses.ucf.edu/courses/1513831/discussion_topics/8665175

The login NID is `ri061277`. An SSH check reached Stokes and its welcome
banner, then required password/keyboard-interactive authentication. A successful
login has not yet been verified. `tools/connect_stokes.sh` opens a password prompt in Terminal and share the connection for the authorized
homework commands. No password is stored in this repository.
