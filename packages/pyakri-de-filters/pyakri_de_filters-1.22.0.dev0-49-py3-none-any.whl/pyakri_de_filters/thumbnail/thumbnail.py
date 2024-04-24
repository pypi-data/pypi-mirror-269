from pyakri_de_utils import Constants
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import create_parent_directory
from pyakri_de_utils.file_utils import get_dest_file_path
from pyakri_de_utils.file_utils import get_input_files_dir
from pyakri_de_utils.image_utils import ImageUtils


DEFAULT_RESIZED_WIDTH, DEFAULT_RESIZED_HEIGHT = Constants.DEFAULT_THUMBNAIL_RESIZED_DIM


class ThumbnailFilter:
    def __init__(
        self, width: int = DEFAULT_RESIZED_WIDTH, height: int = DEFAULT_RESIZED_HEIGHT
    ):
        self.init(height=height, width=width)

    def init(self, **kwargs):
        self._width = int(kwargs.get("resized_width", DEFAULT_RESIZED_WIDTH))
        self._height = int(kwargs.get("resized_height", DEFAULT_RESIZED_HEIGHT))

    def run(self, src_dir, dst_dir):
        files = get_input_files_dir(directory=src_dir, filter_extensions=set(".csv"))
        if not files:
            raise ValueError("No input files found!")

        create_directory(dst_dir)

        # Generate and save thumbnail
        for file in files:
            img = ImageUtils.get_image_thumbnail(
                file=file, resize_dim=(self._width, self._height)
            )

            dst_path = get_dest_file_path(
                file_path=file, src_dir=src_dir, dst_dir=dst_dir
            )

            create_parent_directory(dst_path)

            img.save(
                dst_path,
                format=Constants.DEFAULT_THUMBNAIL_OUTPUT_FORMAT,
                quality=Constants.DEFAULT_THUMBNAIL_QUALITY,
            )
