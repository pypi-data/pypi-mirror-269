"""Methods that assist in importing CT scans of rock cores."""

from .core import Core
from pydicom import dcmread
from pydicom.errors import InvalidDicomError
from os import listdir
import os.path
import numpy as np


def dicom(
    dir: str | None = None,
    files: list[str] | None = None,
    force: bool = False,
    ignore_hidden_files: bool = True,
    ignore_file_extensions: bool = False
) -> Core:
    """
    Load a DICOM dataset into a `Core` object.

    Files containing the DICOM dataset can be specified by providing a directory or a
    list of files. If both `dir` and `files` are provided, `dir` will be ignored.

    When specifying a directory all files in that directory will be treated as
    part of the DICOM dataset. If this is undesirable, use `files` instead.

    Subfolders/directories are ignored. All dicom data files must be explicitly
    specified via `files` or located in the `dir` provided.

    By default, only files with the `.dcm` file extension are read. If this is
    undesirable, set `ignore_file_extensions` to `False`.

    Arguments
    ---------
    dir : str
        Path to directory containing DICOM dataset; ignored if `files` is specified

    files : list[str]
        List of filepaths belonging to DICOM dataset

    force : bool
        If set to `True`, files that produce errors will be ignored

    ignore_hidden_files : bool
        If set to `True`, hidden files will be ignored

    ignore_file_extensions : bool
        If set to `False`, only files with the extension `.dcm` will be read.
    """
    # if files was not provided, load files from the provided directory
    if files is None or len(files) == 0:
        # throw error if directory not provided
        if dir is None:
            raise ValueError("Must provide a non-empty directory or file list")
        # get the list of files for the core
        files = [os.path.join(dir, file_name) for file_name in listdir(dir)]

    # skip files with no SliceLocation information (should be a float)
    slices = []
    skipped: list[str] = []
    for f in files:
        # get the basename of the file and then check if it is a hidden file
        f_name = os.path.basename(f)
        if ignore_hidden_files and f_name.startswith("."):
            continue
        # check file extension
        if not ignore_file_extensions and not f_name.endswith(".dcm"):
            continue
        # ignore subdirectories
        if os.path.isdir(f):
            continue

        # try to read slice
        try:
            ds = dcmread(f, force=force)
        except InvalidDicomError:
            if not force:
                # forward pydicom exception so the stack trace is more useful
                raise
            else:
                continue

        # make sure SliceLocation exists in the slice
        try:
            if isinstance(ds.SliceLocation, float):
                slices.append(ds)
            else:
                skipped.append(f)
        # in case SliceLocation isn't an attribute of ds
        except UnboundLocalError:
            skipped.append(f)

    if not force and len(skipped) > 0:
        raise ValueError(
            f"Failed to load {len(skipped)} files, missing SliceLocation: {skipped}"
        )

    # make sure we actually loaded data
    if len(slices) == 0:
        raise RuntimeError(
            "No data loaded. This could mean an empty directory was provided, "
            "no files could be parsed, or no files had the `.dcm` file "
            "extension (if `ignore_file_extensions` is set to `False`)."
        )

    # re-sort to put the slices in the right order
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    # pixel dimensions, assuming all slices are the same
    x_dim: float = float(slices[0].PixelSpacing[0])
    y_dim: float = float(slices[0].PixelSpacing[1])
    z_dim: float = float(slices[0].SliceThickness)

    # create 3D array
    img_shape: list[int] = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d: np.typing.NDArray[np.float64] = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d

    return Core(data=img3d, pixel_dimensions=(x_dim, y_dim, z_dim))
