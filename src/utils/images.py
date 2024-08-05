import os
import imagehash
import shutil
from PIL import Image


def is_image_file(file_path):
    """
    Check if a file is a valid image file.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file is a valid image file, False otherwise.
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError) as e:
        print(f"File {file_path} is not a valid image file. Reason: {e}")
        return False


def remove_corrupted_images(directory):
    """
    Remove all corrupted images in a directory.

    Args:
        directory (str): Path to the directory to check for corrupted images.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            if not is_image_file(file_path):
                try:
                    os.remove(file_path)
                    print(f"Removed corrupted image: {file_path}")
                except Exception as e:
                    print(f"Failed to remove corrupted image {file_path}. Reason: {e}")


def compute_hash(image_path: str) -> None | imagehash.ImageHash:
    """
    Compute the perceptual hash of an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: The computed hash of the image.
    """
    try:
        with Image.open(image_path) as img:
            return imagehash.average_hash(img)
    except Exception as e:
        print(f"Failed to compute hash for {image_path}. Reason: {e}")
        return None


def store_hashes(image_paths, hash_file):
    """
    Compute and store hashes of given images in a file.

    Args:
        image_paths (list): List of image file paths.
        hash_file (str): Path to the file where hashes will be stored.
    """
    with open(hash_file, "w") as f:
        for image_path in image_paths:
            image_hash = compute_hash(image_path)
            if image_hash:
                f.write(f"{image_hash}\n")
                print(f"Stored hash for {image_path}")


def find_and_remove_duplicates(directory: str) -> None:
    """
    Find and remove duplicate images in a directory.

    Args:
        directory (str): Path to the directory to check for duplicates.
    """
    hashes = {}
    duplicates = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            image_hash = compute_hash(file_path)
            if image_hash:
                if image_hash in hashes:
                    duplicates.append(file_path)
                else:
                    hashes[image_hash] = file_path

    for duplicate in duplicates:
        try:
            os.remove(duplicate)
            print(f"Removed duplicate image: {duplicate}")
        except Exception as e:
            print(f"Failed to remove {duplicate}. Reason: {e}")


def load_hashes(hash_file):
    """
    Load hashes from a file into a set.

    Args:
        hash_file (str): Path to the file containing hashes.

    Returns:
        set: A set of hashes.
    """
    with open(hash_file, "r") as f:
        return set(line.strip() for line in f)


def is_duplicate(image_path, stored_hashes):
    """
    Check if an image is a duplicate based on stored hashes.

    Args:
        image_path (str): Path to the image file.
        stored_hashes (set): Set of stored hashes.

    Returns:
        bool: True if the image is a duplicate, False otherwise.
    """
    image_hash = compute_hash(image_path)
    return str(image_hash) in stored_hashes


def filter_dataset(dataset_dir, hash_file, output_dir):
    """
    Filter out duplicate images from a dataset.

    Args:
        dataset_dir (str): Path to the dataset directory.
        hash_file (str): Path to the file containing hashes to filter.
        output_dir (str): Path to the directory to save filtered images.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    stored_hashes = load_hashes(hash_file)

    for filename in os.listdir(dataset_dir):
        file_path = os.path.join(dataset_dir, filename)
        if os.path.isfile(file_path):
            if not is_duplicate(file_path, stored_hashes):
                shutil.copy(file_path, os.path.join(output_dir, filename))
                print(f"Copied {file_path} to {output_dir}")
            else:
                print(f"Filtered out duplicate image: {file_path}")


def resize_and_crop_image(
    input_file: str, output_file: str, target_size: int = 256, crop_size: int = 224
) -> None:
    """
    Resize an image to the target size and then crop the center to the crop size.

    Args:
        input_file (str): Path to the input image file.
        output_file (str): Path to the output image file.
        target_size (int): Size to resize the image to (default is 256x256).
        crop_size (int): Size to crop the center of the image (default is 224x224).
    """
    with Image.open(input_file) as img:
        img = img.resize((target_size, target_size), Image.LANCZOS)

        left = (target_size - crop_size) / 2
        top = (target_size - crop_size) / 2
        right = (target_size + crop_size) / 2
        bottom = (target_size + crop_size) / 2

        img = img.crop((left, top, right, bottom))

        img.save(output_file, "JPEG")


def process_image_file(input_file: str, output_file: str) -> None:
    resize_and_crop_image(input_file, output_file)
    print(f"Processed {input_file} to {output_file}")


def process_image_directory(
    input_dir: str, output_dir: str, max_workers: int = 12
) -> None:
    """
    Process all image files in a directory, resize and crop them, and save them to the output directory.

    Args:
        input_dir (str): Path to the directory containing image files.
        output_dir (str): Path to the directory to save processed image files.
        max_workers (int): Maximum number of threads to use.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith((".jpeg", ".jpg", ".png")):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(
                        output_dir, os.path.splitext(file)[0] + ".jpeg"
                    )
                    futures.append(
                        executor.submit(process_image_file, input_file, output_file)
                    )

        for future in futures:
            future.result()


def main() -> None:
    pass


if __name__ == "__main__":
    main()
