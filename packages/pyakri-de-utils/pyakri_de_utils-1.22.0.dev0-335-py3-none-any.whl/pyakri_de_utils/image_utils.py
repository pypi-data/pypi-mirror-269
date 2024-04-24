from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import PIL
import pydicom
from numpy import ndarray
from PIL import Image
from PIL import ImageOps
from PIL import ImageFile
from PIL import UnidentifiedImageError
from pyakri_de_utils import logger
from pydicom.errors import InvalidDicomError

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImgReadError(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return f"AKRI_ERROR: {self._msg}"


class ImgFormatUnknownError(ImgReadError):
    pass


def image_exception_handler(func):
    def meth(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImgFormatUnknownError as ex:
            logger.debug(f"Unknown image format {ex}")
            raise ex
        except Exception as ex:
            logger.debug(f"Error reading image file {ex}")
            raise ImgReadError(f"Error Reading image {str(ex)}")

    return meth


class ImageUtils:
    @classmethod
    def default_read(cls, file_path: Path):
        try:
            with Image.open(file_path) as img:
                img.load()
                if hasattr(img, "_getexif"):
                    img = ImageOps.exif_transpose(img)
                return img
        except UnidentifiedImageError as ex:
            raise ImgFormatUnknownError(str(ex))
        except Exception as ex:
            raise ImgReadError(str(ex))

    @classmethod
    def dicom_read(cls, file_path: Path):
        try:
            # Read the dcm file
            dcm_img = pydicom.dcmread(file_path)

            # If no image data, then treat the file as corrupted file to skip processing
            if "PixelData" not in dcm_img:
                logger.info(f"No pixel data in {file_path}")
                raise ImgReadError(f"Not dicom image file {file_path}")
            img = dcm_img.pixel_array.astype(float)

            # Fetch the 1st frame if there are more than 1 frames
            if dcm_img.get("NumberOfFrames", 1) > 1:
                img = img[0, :, :]

            # scale Image
            scaled_img = (
                (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
            ).astype(np.uint8)

            # Convert ndarray to PIL.Image
            pil_img = Image.fromarray(scaled_img)
            return pil_img
        except InvalidDicomError as ex:
            raise ImgFormatUnknownError(str(ex))
        except Exception as ex:
            raise ImgReadError(str(ex))

    @staticmethod
    def get_image_from_file(file: Path) -> Image:
        if file.suffix.lower() == ".dcm":
            return ImageUtils.dicom_read(file)
        return ImageUtils.default_read(file)

    @classmethod
    def is_image_corrupted(cls, file: Path) -> bool:
        try:
            cls.get_image_from_file(file)
            return False
        except Exception as e:
            logger.info(
                "Failure in is_image_corrupted for file:%s with error %r", file, e
            )
            return True

    @classmethod
    def get_image_size(cls, file: Path) -> Optional[Tuple[int, int]]:
        try:
            img = cls.get_image_from_file(file)
            return img.size
        except Exception as e:
            logger.info("Failure in get_image_size for file:%s with error %r", file, e)
            return None

    @classmethod
    @image_exception_handler
    def get_image_thumbnail(
        cls, file: Path, resize_dim: Tuple[int, int], resample_algo=Image.BICUBIC
    ) -> Image:

        img = cls.get_image_from_file(file=file)
        img = cls.convert_image_to_rgb(img)
        img.thumbnail(resize_dim, resample=resample_algo)

        return img

    @classmethod
    @image_exception_handler
    def resize_image_file(
        cls,
        file: str,
        resize_dim: Tuple[int, int],
        resample_algo=Image.BICUBIC,
        flatten_img=True,
    ) -> ndarray:
        img = cls.get_image_from_file(file=file)
        return cls.resize(
            img=img,
            resize_dim=resize_dim,
            resample_algo=resample_algo,
            flatten_img=flatten_img,
        )

    @staticmethod
    @image_exception_handler
    def convert_image_to_rgb(img: Image) -> Image:
        return img.convert("RGB")

    @staticmethod
    @image_exception_handler
    def convert_image_to_grayscale(img: Image) -> Image:
        return img.convert("L")

    @staticmethod
    @image_exception_handler
    def get_image_array(img: Image) -> ndarray:
        return np.asarray(img)

    @staticmethod
    @image_exception_handler
    def get_image_from_array(np_image: ndarray, dtype=np.uint8) -> Image:
        return Image.fromarray(np_image.astype(dtype))

    @classmethod
    def resize_image(
        cls,
        img_array: ndarray,
        resize_dim: Tuple[int, int],
        resample_algo=Image.BICUBIC,
        flatten_img=True,
        dtype=np.uint8,
    ) -> ndarray:
        img = cls.get_image_from_array(np_image=img_array, dtype=dtype)
        return cls.resize(
            img=img,
            resize_dim=resize_dim,
            resample_algo=resample_algo,
            flatten_img=flatten_img,
        )

    @staticmethod
    @image_exception_handler
    def resize(
        img: PIL.Image,
        resize_dim: Tuple[int, int],
        resample_algo=Image.BICUBIC,
        flatten_img=True,
    ) -> ndarray:
        img = img.resize(resize_dim, resample=resample_algo)
        im_np = np.array(img)

        if flatten_img:
            im_arr = im_np.flatten()
            im_arr = im_arr / 255
            return im_arr

        return im_np
