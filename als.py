import argparse
import gzip
import xml.etree.ElementTree as ET
from itertools import chain


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to .als project file')
    args = parser.parse_args()

    res = {}

    print('[x] Extracting gzipped .als to memory')
    with gzip.open(args.file, 'rb') as f:
        data = f.read()

    print('[x] Parsing XML')
    root = ET.fromstring(data)

    for track in root.find('.//Tracks'):
        plugins = set()
        for vst in track.findall('.//VstPluginInfo'):
            props = {c.tag: dict(c.items()) for c in list(vst)}
            plugins.add(props['PlugName']['Value'] + ' [VST2]')

        for vst3 in track.findall('.//Vst3PluginInfo'):
            plugins.add(vst3.find('Name').attrib['Value'] + ' [VST3]')

        if plugins:
            # res[f"{track.find('Name/UserName').get('Value')}#{track.get('Id')}"] = plugins
            track_name = track.find('Name/EffectiveName').get('Value')
            res[f"{track_name}#{track.get('Id')}"] = plugins

    if not res:
        print('[x] No VST plugins found')
    else:
        plugins = set(sorted(chain(*res.values())))

        print('[x] All plugins:')
        print('\n'.join(plugins))

        print('\n[x] Tracks containing each plugin:')
        for p in plugins:
            print(p)
            print('\n'.join(f'\t{t}' for t in [k for k in res.keys() if p in res[k]]))

        print('\n[x] Plugins in each track:')
        for track, plugins in res.items():
            print(track)
            print('\n'.join(f'\t{p}' for p in plugins))


if __name__ == '__main__':
    main()
