#!/usr/bin/env python3

import argparse
import re
import os
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Samples code and injects the samples into a Reveal.js Markdown file.'
)
parser.add_argument(
    '--in-file', type=str, default='index.html.in',
    help='The input file into which code samples are injected.  This file must ' +
    'end in ".in".  The output file will be the same as the input, without the ' +
    '".in".'
)
parser.add_argument(
    '--cpp-root', type=str,
    help='The path under which all samples may be found.'
)
args = parser.parse_args()


if not args.in_file.endswith('.in'):
    print('error: --in-file {0} does not end with ".in"'.format(args.in_file))
    exit(1)

sample_begin_regex = re.compile(r' *// *sample *[(] *([^ )]+) *[)] *\n')
sample_end_regex = re.compile(r' *// *end-sample *[(] *([^ )]+) *[)] *\n')
def get_sample(filename, name):
    lines = open(os.path.join(args.cpp_root, filename), 'r').readlines()
    chunk = '<!-- Sampled from {0} {1} -->\n```c++\n'.format(filename, name)
    in_chunk = False
    for line in lines:
        match = sample_begin_regex.match(line)
        if match and match.group(1) == name:
            in_chunk = True
            continue
        match = sample_end_regex.match(line)
        if match and match.group(1) == name:
            chunk += '```\n<!-- End sample -->\n'
            return chunk
        if in_chunk:
            chunk += line
    raise SyntaxError('Bad sample (nonexistent or not closed)')

sample_ref_regex = re.compile(r' *%%% *([^ #]+) *# *([^ %]+) *%%% *\n')

lines = open(args.in_file, 'r').readlines()
out_contents = ''
for line in lines:
    match = sample_ref_regex.match(line)
    if match:
        out_contents += get_sample(match.group(1), match.group(2))
    else:
        out_contents += line

output_path = Path(args.in_file[:-3])
output_path = (output_path.parent / '..' / output_path.name).resolve()
open(str(output_path), 'w').write(out_contents)
