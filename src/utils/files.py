import os
import shutil
import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor


def clear_data_directory(data_path: str, keep: str) -> None:
    """
    Clears all data except from keep string

    Args:
        data_path (str): The path that will be cleared.
        keep (str): Data to keep.
    """
    for item in os.listdir(data_path):
        item_path = os.path.join(data_path, item)
        if item != keep:
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"Deleted {item_path}")
            except Exception as e:
                print(f"Failed to delete {item_path}. Reason: {e}")


def copy_image(patient_id: str, target: int, input_dir: str, output_dir: str) -> None:
    """
    Copy images based on the target label to appropriate folders.

    Args:
        patient_id (str): Patient ID.
        target (int): Target label (1 for pneumonia, 0 for normal).
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory to save copied images.
    """
    input_file = os.path.join(input_dir, f"{patient_id}.jpeg")
    if target == 1:
        output_folder = os.path.join(output_dir, "pneumonia")
    else:
        output_folder = os.path.join(output_dir, "normal")

    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except FileExistsError:
            pass

    output_file = os.path.join(output_folder, f"{patient_id}.jpeg")

    if os.path.exists(input_file):
        shutil.copy(input_file, output_file)
        print(f"Copied {input_file} to {output_file}")
    else:
        print(f"File {input_file} not found.")


def delete_directory(directory: str) -> None:
    """
    Delete a directory and all its contents.

    Args:
        directory (str): Path to the directory to delete.
    """
    try:
        shutil.rmtree(directory)
        print(f"Deleted directory {directory}")
    except Exception as e:
        print(f"Failed to delete directory {directory}. Reason: {e}")


def process_csv(
    csv_file: str, input_dir: str, output_dir: str, max_workers: int = 12
) -> None:
    """
    Process the CSV file and copy images concurrently.

    Args:
        csv_file (str): Path to the CSV file containing patientId and target columns.
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory to save copied images.
        max_workers (int): Maximum number of threads to use.
    """
    df = pd.read_csv(csv_file)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                copy_image, row["patientId"], row["Target"], input_dir, output_dir
            )
            for _, row in df.iterrows()
        ]

        for future in futures:
            future.result()


def sort_and_rename_files(directory: str) -> None:
    """
    Sort files in a directory alphabetically and rename them in order.

    Args:
        directory (str): Path to the directory to organize files.
    """
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]

    files.sort()

    for i, filename in enumerate(files, start=1):
        new_filename = f"{i:04d}.jpeg"
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)

        os.rename(old_file, new_file)
        print(f"Renamed {old_file} to {new_file}")


def move_files(src_dir: str, dest_dir: str, dest_prefix: str = "") -> None:
    """
    Move all files from the source directory to the destination directory.

    Args:
        src_dir (str): Path to the source directory.
        dest_dir (str): Path to the destination directory.
        dest_prefix (str): String to append before the filename in the destine.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(dest_dir, dest_prefix + filename)

        if os.path.isfile(src_file):
            shutil.move(src_file, dest_file)
            print(f"Moved {src_file} to {dest_file}")


def move_random_files(
    src_dir: str,
    dest_dir: str,
    num_files: int,
    seed: int | None = None,
    dest_prefix: str = "",
) -> None:
    """
    Move a specified number of random files from the source directory to the destination directory.

    Args:
        src_dir (str): Path to the source directory.
        dest_dir (str): Path to the destination directory.
        num_files (int): Number of random files to move.
        seed (int, optional): Seed for the random number generator.
        dest_prefix (str): String to append before the filename in the destine.
    """
    if seed is not None:
        random.seed(seed)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # List all files in the source directory
    files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]

    # Select a random subset of files
    random_files = random.sample(files, min(num_files, len(files)))

    # Move each file to the destination directory
    for filename in random_files:
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(dest_dir, dest_prefix + filename)

        shutil.move(src_file, dest_file)
        print(f"Moved {src_file} to {dest_file}")


def main() -> None:
    pass


if __name__ == "__main__":
    main()
