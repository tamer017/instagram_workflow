# Fixed: Install moviepy using python -m pip in GitHub Actions

This ZIP updates the workflow to use `python -m pip install ...` ensuring packages are installed into the same Python interpreter the steps run with. It also adds debug output to check that `moviepy` is importable.

### Key fixes
- Use `actions/setup-python` and then `python -m pip install ...` (not plain `pip`) so the correct interpreter gets the packages.
- Install dependencies: moviepy, imageio, imageio-ffmpeg, pillow, numpy.
- Set `IMAGEIO_FFMPEG_BINARY=/usr/bin/ffmpeg` when generating to ensure imageio uses system ffmpeg.
- Added a debug step that prints python version, pip version, and whether `moviepy` can be found.

If you still get `ModuleNotFoundError`, check the workflow logs for the debug step — it will show whether `moviepy` was installed into the Python used by the runner.
