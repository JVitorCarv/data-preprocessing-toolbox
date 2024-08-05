import os
import numpy as np
import pydicom
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from pydicom.pixel_data_handlers.util import apply_voi_lut


def convert_dcm_to_jpeg(dicom_file: str, output_file: str) -> None:
    """
    Convert a DICOM file to JPEG format.

    Args:
        dicom_file (str): Path to the DICOM file.
        output_file (str): Path to the output JPEG file.
    """
    dicom = pydicom.dcmread(dicom_file)

    # Apply VOI LUT if present
    if "WindowWidth" in dicom and "WindowCenter" in dicom:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array

    data = data - np.min(data)
    data = data / np.max(data) * 255.0
    data = data.astype(np.uint8)

    image = Image.fromarray(data)
    image.save(output_file, "JPEG")


def process_file(dicom_file: str, output_file: str) -> None:
    convert_dcm_to_jpeg(dicom_file, output_file)
    print(f"Converted {dicom_file} to {output_file}")


def process_directory(input_dir: str, output_dir: str, max_workers: int = 12) -> None:
    """
    Process all DICOM files in a directory and convert them to JPEG format.

    Args:
        input_dir (str): Path to the directory containing DICOM files.
        output_dir (str): Path to the directory to save JPEG files.
        max_workers (int): Maximum number of threads to use.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(".dcm"):
                    dicom_file = os.path.join(root, file)
                    jpeg_file = os.path.join(
                        output_dir, os.path.splitext(file)[0] + ".jpeg"
                    )
                    futures.append(executor.submit(process_file, dicom_file, jpeg_file))

        for future in futures:
            future.result()


def main() -> None:
    pass


if __name__ == "__main__":
    main()
