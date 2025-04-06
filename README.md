
# TWIC PGN Downloader

This script downloads Portable Game Notation (PGN) ZIP files from The Week in Chess (TWIC) website.
It allows users to download all available PGN files or a specific range of files based on their IDs.

## Features

- Download all PGN ZIP files or a specific range.
- Specify output directory for downloaded files.
- Option to overwrite existing files.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/twic-pgn-downloader.git
   cd twic-pgn-downloader
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script using the command line:

```bash
python twic_downloader.py [options]
```

### Options

- `-a`, `--all`: Download all PGN ZIP files.
- `-s`, `--start`: Start of the range. If there is no end, it will download only one PGN ZIP file.
- `-e`, `--end`: End of the range. If there is no start, it will download only one PGN ZIP file.
- `-f`, `--force`: If the ZIP exists, overwrite it.
- `-o`, `--output`: Output directory for the downloaded files.

### Examples

- Download all PGN ZIP files:

  ```bash
  python twic_downloader.py --all
  ```

- Download a specific range of PGN ZIP files:

  ```bash
  python twic_downloader.py --start 100 --end 110
  ```

- Download a single PGN ZIP file:

  ```bash
  python twic_downloader.py --start 100
  ```

- Specify an output directory:

  ```bash
  python twic_downloader.py --all --output /path/to/directory
  ```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please contact [your email].
