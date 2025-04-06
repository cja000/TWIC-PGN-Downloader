import re
import requests
import argparse
from datetime import datetime

from pathlib import Path
from bs4 import BeautifulSoup

URL_TWIC = "https://theweekinchess.com/twic/"
URL_TWIC_ZIP = "https://theweekinchess.com/zips/twic"
CURRENT_DATETIME = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_id_regex = re.compile(r".*twic([0-9]*)g.zip")


def sort_strings_by_numbers(string_list):
    # Define a custom key function to extract the numeric part
    def extract_number(item):
        # Use regex to find the numeric part of the string
        match = re.search(r"\d+", item)
        return (
            int(match.group()) if match else float("inf")
        )  # Default to infinity if no number found

    # Sort the list using the custom key
    sorted_list = sorted(string_list, key=extract_number)

    return sorted_list


def get_pgn_urls(url_twic):
    """Get all the URLs of the PGN in zip format

    Parameters:
    -----------
    url_twic: str
        String with the URL of the TWIC page with the PGN zips
    Returns:
    --------
    zips_urls: list
        List with all the urls of the PGN zips
    """
    zip_urls = []
    session = requests.Session()
    session.headers.update({"User-Agent": "Custom user agent"})

    try:
        html = session.get(url_twic).content
        soup = BeautifulSoup(html, "html.parser")
        zip_file = re.compile(r".*g\.zip")
        for link in soup.find_all("a"):
            url = link.get("href")
            if zip_file.search(url):
                zip_urls.append(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
    return sort_strings_by_numbers(list(set(zip_urls)))


def download_zip(id, force=False, folder=Path.cwd()):
    """Download the zip file of the PGN
    https://theweekinchess.com/zips/twic123g.zip

    Parameters:
    -----------
    id: str or int
        ID of the zip file to download (for example, for twic123g.zip pass 123)
    force: bool
        If the ZIP exists, overwrite it
    folder: Path
        Folder where the zip file will be saved
    Returns:
    --------
    filename: str
        Filename of the zip file downloaded
    """
    url = f"{URL_TWIC_ZIP}{id}g.zip"
    filename = f"twic{id}g.zip"
    filepath = folder / filename
    # Check if the file exists and if overwrite is False
    if filepath.exists() and not force:
        print(f"File {filepath} already exists. Use --overwrite to overwrite.")
        return
    session = requests.Session()
    session.headers.update({"User-Agent": "Custom user agent"})
    try:
        data = session.get(url).content
        with open(filepath, "wb") as f:
            f.write(data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def get_positon_in_list(id, url_list):
    for idx, url in enumerate(url_list):
        if str(id) in url:
            return idx
    print(f"ID {id} not found in the list")
    return None


def get_min_max_idxs(args, pgn_urls):
    
    if args.all:
        start = int(zip_id_regex.search(pgn_urls[0]).group(1))
        end = int(zip_id_regex.search(pgn_urls[-1]).group(1))
    elif args.start is not None or args.end is not None:
        start = args.start
        end = args.end

        if start is None:
            start = end
        if end is None:
            end = start
        if start > end:
            start, end = end, start
            print(f"Start and end values are swapped. Start: {start}, End: {end}")
    else:
        print("Please provide a valid argument. Use -h for help.")
    start = min(start, end)
    end = max(start, end)
    start_idx = get_positon_in_list(start, pgn_urls)
    end_idx = get_positon_in_list(end, pgn_urls)
    if end_idx is None:
        end_idx = len(pgn_urls)
    return (start_idx, end_idx, start, end)


def argument_parser():
    parser = argparse.ArgumentParser(description="Download TWIC PGNs")
    parser.add_argument(
        "-a", "--all", action="store_true", help="Download all PGN ZIP files"
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        help="Start of the range. If there is no end it will be only one PGN ZIP file to download",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        help="End of the range. If there is no start it will be only one PGN ZIP file to download",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="If the ZIP exists, overwrite it"
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="Output directory for the downloaded files"
    )

    args = parser.parse_args()

    if args.all and (args.start is not None or args.end is not None):
        parser.error("--all cannot be used with --start or --end")

    return args


def main():
    args = argument_parser()
    pgn_urls = get_pgn_urls(URL_TWIC)
    start_idx, end_idx, start, end = get_min_max_idxs(args, pgn_urls)
    print(f"Downloading PGNs from {start} to {end}")
    print(f"Total PGNs to download: {end_idx - start_idx + 1}")
    

    if args.output is not None:
        output_folder = args.output
        
    else:
        output_folder = Path.cwd() / f"TWIC-{CURRENT_DATETIME}-{start}_{end}"
    output_folder.mkdir(parents=True, exist_ok=True)
    print(f"Output folder: {output_folder}")
    for url in pgn_urls[start_idx:end_idx+1]:
        print(f"Downloading {url}")
        id = zip_id_regex.search(url).group(1)
        download_zip(id,folder=output_folder)


if __name__ == "__main__":
    main()
