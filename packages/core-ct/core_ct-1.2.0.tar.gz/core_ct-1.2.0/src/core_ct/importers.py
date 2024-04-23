"""Methods that assist in importing CT scans of rock cores."""

from core_ct.core import Core
from core_ct.slice import Slice
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

    This is used to load a set of images into one core object. All images must
    come from the same CT scan of the same core.

    Files containing the DICOM dataset can be specified by providing a directory
    or a list of files. If both `dir` and `files` are provided, `dir` will be
    ignored.

    When specifying a directory all files in that directory will be treated as
    part of the DICOM dataset. If this is undesirable, use `files` instead.

    Subfolders/directories are ignored. All dicom data files must be explicitly
    specified via `files` or located in the `dir` provided.

    Arguments
    ---------
    dir : str
        Path to directory containing DICOM dataset; ignored if `files` is
        specified

    files : list[str]
        List of filepaths belonging to DICOM dataset

    force : bool
        If set to `True`, files that produce errors will be ignored

    ignore_hidden_files : bool
        If set to `True`, hidden files (names starting with ".") will be ignored
    
    Raises
    ------
    ValueError
        If no files are found. Caused by providing an empty directory (`dir`) or
        an empty `files` list. Also raised when files are missing header
        information.
    RuntimeError
        If no data was loaded. Happens when no files can be parsed and `force` is set to
        `True`
    pydicom.InvalidDicomError
        If `pydicom` fails to parse a file
    """
    # if files was not provided, load files from the provided directory
    if files is None or len(files) == 0:
        # throw error if directory not provided
        if dir is None:
            raise ValueError("Must provide a directory (`dir`) when not using `files`")
        # get the list of files for the core
        files = [os.path.join(dir, file_name) for file_name in listdir(dir)]
    
    # remove invalid files
    for f in files:
        f_name = os.path.basename(f)
        # get the basename of the file and then check if it is a hidden file
        if ignore_hidden_files and f_name.startswith("."):
            files.remove(f)
        # ignore subdirectories
        if os.path.isdir(f):
            files.remove(f)

    if len(files) == 0:
        raise ValueError(
            "No files found. This could mean an empty directory (`dir`) was provided "
            "or `files` is empty.")

    # skip files with no SliceLocation information (should be a float)
    slices = []
    skipped: list[str] = []
    for f in files:
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
        except AttributeError:
            skipped.append(f)

    if not force and len(skipped) > 0:
        raise ValueError(
            f"Failed to load {len(skipped)} files, invalid or missing SliceLocation: "
            f"{skipped}"
        )

    # make sure we actually loaded data
    if len(slices) == 0:
        raise RuntimeError(
            "No data loaded. This could mean no files could be parsed and `force` was "
            "set to `True`"
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

def dicom_slice(
    file: str,
    force: bool = False,
) -> Slice:
    """
    Load a DICOM dataset into a `Slice` object.

    This function should be used when you only want to load one image/scan instead of a
    collection.

    Arguments
    ---------
    file : str
        Path to file to load DICOM data from

    force : bool
        If set to `True`, files that produce errors will be ignored
    
    Raises
    ------
    ValueError
        If the file is missing header information.
    pydicom.InvalidDicomError
        If `pydicom` fails to parse the file
    """
    # try to read slice
    try:
        ds = dcmread(file, force=force)
    except InvalidDicomError:
        if not force:
            # forward pydicom exception so the stack trace is more useful
            raise

    # make sure SliceLocation exists in the slice
    try:
        if not isinstance(ds.SliceLocation, float):
            raise ValueError("File could not be parsed (incorrect SliceLocation type)")
    # in case SliceLocation isn't an attribute of ds
    except AttributeError as e:
        if not force:
            raise ValueError(
                "File does not contain SliceLocation in header, it may not be a valid "
                "dicom file"
            ) from e

    # pixel dimensions
    x_dim: float = float(ds.PixelSpacing[0])
    y_dim: float = float(ds.PixelSpacing[1])
    z_dim: float = float(ds.SliceThickness)

    return Slice(data=ds.pixel_array, 
                 pixel_dimensions=(x_dim, y_dim), 
                 thickness=z_dim)
