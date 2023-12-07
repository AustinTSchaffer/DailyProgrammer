#!/usr/bin/env python

import os
import pathlib
import argparse
import shutil
import datetime

import aocd
import requests
import bs4
import markdownify

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--day', '-d', dest='day', required=False)
    argparser.add_argument('--year', '-y', dest='year', required=False)
    argparser.add_argument('--dir', dest='dir', required=False)
    argparser.add_argument('--session', dest='session', required=False)

    args = argparser.parse_args()

    today = datetime.datetime.now()
    year = int(args.year or today.year)
    day = int(args.day or today.day)
    session = args.session or os.getenv("AOC_SESSION")

    this_script_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    output_dir = pathlib.Path(args.dir) if args.dir else pathlib.Path(this_script_dir / '..' / '..' / str(year) / f'day_{day:02d}')

    os.makedirs(output_dir, mode=0o755, exist_ok=True)

    prompt_resp = requests.get(f"https://adventofcode.com/{year}/day/{day}", headers={'cookie': f'session={session}'})
    assert prompt_resp.ok
    soup = bs4.BeautifulSoup(prompt_resp.text, features="html.parser")
    main_article = soup.article
    prompt_md = markdownify.markdownify(str(main_article))
    with open(output_dir / "prompt.md", "w") as f:
        f.write(prompt_md)

    input_data = aocd.get_data(session=session, day=day, year=year)
    with open(output_dir / "input.txt", "w") as f:
        f.write(input_data)

    if not os.path.isfile(output_dir / 'sln.py'):
        shutil.copyfile(this_script_dir / 'sln.py', output_dir / 'sln.py')

if __name__ == '__main__':
    main()
