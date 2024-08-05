from better_bing_image_downloader import downloader

# ATTENTION: No wrapper for this one, this is just an example on how to use it.

if __name__ == "__main__":
    downloader.download(
        "Search Term",
        limit=100,
        output_dir="output",
        force_replace=False,
        timeout=2,
        verbose=True,
    )
