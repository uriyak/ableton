import argparse
import gzip
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Path to .als project file')
args = parser.parse_args()

plugins = set()

print('[x] Extracting gzipped .als to memory')
with gzip.open(args.file, 'rb') as f:
    data = f.read()

print('[x] Parsing XML')
root = ET.fromstring(data)

print('[x] Searching for VstPluginInfo tags')
for vst in root.findall('.//VstPluginInfo'):
    props = {c.tag: dict(c.items()) for c in list(vst)}
    plugins.add(props['PlugName']['Value'])

print(plugins and ('[x] Found VSTs:\n' + '\n'.join(sorted(plugins))) or '[x] VSTs not found')
