import argparse
import pymupdf
import shutil

from pathlib import Path

def process(input_file_path: Path, output_dir_path: Path):
    """process a file

    Args:
        input_file_path (Path): path to input pdf
        output_dir_path (Path): path to output dir

    Returns:
        bool: True if succeed for opening pdf, otherwise False
    """

    try:
        # Open pdf
        pdf = pymupdf.open(input_file_path)

    except Exception as e:
        # When cannot open
        print(f"Failed to read PDF file: {e}")

        return False

    for page in pdf:
        pix = page.get_pixmap(dpi=dpi)
        output_file_path = output_dir_path / f"page-{page.number}.png"

        try:
            pix.save(output_file_path)
        except Exception as e:
            print(f"Failed to write image file: {e}")

    return True

# Parse command-line parameters
parser = argparse.ArgumentParser(description='Render PDF file pages and output image files')
parser.add_argument('input_path', type=Path, help='path to the input PDF file or directory')
parser.add_argument('--dpi', dest='dpi', type=int, default=150, help='dpi of output images')
args = parser.parse_args()

input_path: Path = args.input_path
dpi: int = args.dpi

input_file_paths: list[Path] = []

if input_path.is_dir():
    for input_file_path in input_path.glob('*.pdf'):
        input_file_paths.append(input_file_path)
else:
    input_file_paths.append(input_path)

for input_file_path in input_file_paths:
    output_dir_path = input_file_path.with_suffix('')
    if output_dir_path.exists():
        print('Directory already exists:', output_dir_path)
        conf = input('Overwrite? (Y/n): ')
        if conf != 'Y':
            continue

        shutil.rmtree(output_dir_path)

    output_dir_path.mkdir()

    process(input_file_path, output_dir_path)
