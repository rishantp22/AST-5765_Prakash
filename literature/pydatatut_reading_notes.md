# Python tutorial reading notes

Codex reviewed chapters 1–2, pages 8–48, of *Using Python for Interactive Data
Analysis*, Perry Greenfield and Robert Jedrzejewski, STScI, May 10, 2007.
The course copy is in Webcourses `Files/Demos_lectures/week_2/pydatatut/`.
`pydatatut_NRAO.pdf` is a public mirror with matching title, date and page
count; binary identity with the course file has not been established.
Source: https://safe.nrao.edu/wiki/pub/ALMA/RI_CASATips/pydatatut.pdf

Chapter 1 covers FITS images and headers, array types, zero-based indexing,
slices, broadcasting and vectorized operations. Assignment creates another
reference; `.copy()` preserves independent original data. Changing numeric
type uses `.astype()`. These points explain HW2's floating-point conversion
and preserved ramp.

Chapter 2 covers FITS table columns, sequences, dictionaries, plotting,
overplots, labels, legends and `savefig`. HW2 applies these plotting practices.

The tutorial uses historical Python-2/PyFITS interfaces. The homework uses
the installed Python-3/NumPy/Matplotlib interfaces. This records an assisted
reading review, not completion of every practice exercise by the student.
