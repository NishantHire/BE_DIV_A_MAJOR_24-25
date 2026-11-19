# Fashion Attire Recommendation System

Undergraduate project archive exploring webcam-based virtual try-on with Python, Flask, OpenCV, and a desktop Tkinter interface.

## Recovery status

The coursework ZIP contains **five Python source files**. They have been extracted into [recovered-source](recovered-source/) so the implementation can be browsed and reviewed without downloading the ZIP.

**This is an incomplete historical snapshot, not a runnable release.** The original archive and presentation remain in [the original coursework folder](GR13_NishantHire_Sem%20VIII_2024-25/).

## Recovered components

| File | Purpose |
| --- | --- |
| `camera.py` | Captures webcam frames and encodes JPEG output |
| `main.py` | Flask page routes, video streaming, cart state, and desktop try-on launchers |
| `tryOn.py` | MediaPipe face-landmark prototype with a Tkinter overlay interface |
| `test.py` | Legacy dlib-based accessory and garment-overlay GUI; this is an application, not an automated test suite |
| `tkinter_scroll.py` | Tkinter scrolling and window utilities |

## Missing from this snapshot

The source references resources that are absent from the ZIP:

- Flask HTML templates and website assets.
- Garment/accessory images, `logo.png`, and the default overlay.
- Haar cascade and dlib landmark data files.
- A dependency manifest, environment lockfile, and automated tests.

The recovered files do not establish a working payment integration or independently reproduce historical performance measurements.

## Issues to resolve before running

- The Flask launch routes concatenate request-controlled text into shell commands. Replace them with validated, allow-listed inputs and shell-free subprocess invocation before any use.
- `/tryall` does not return its rendered response.
- `tryOn.py` references `rotate_bound` without importing it.
- Some overlay dimensions and coordinates are hard-coded; frame boundaries and vertical landmark pairs need explicit handling.
- Tkinter widgets are updated from a worker thread. Move UI updates to the Tk event loop.
- Several camera reads and image loads lack failure handling.

Do not expose the archived Flask application as a network service.

## Validation performed

All five extracted Python files were parsed successfully with Python's `ast.parse`. Their contents are preserved from the ZIP.

No webcam, GUI, model inference, installation, or end-to-end workflow has been run as part of this recovery. Syntax checks do not establish runtime correctness.

## Next steps

1. Recover the original templates, images, model assets, and dependency versions.
2. Document team contributions and any upstream components or asset licenses.
3. Repair the launchers, resource handling, and overlay calculations.
4. Add focused tests, run the application on real hardware, and document measured results.

This repository remains a coursework archive while recovery is in progress.
