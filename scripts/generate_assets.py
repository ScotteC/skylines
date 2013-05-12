#!/usr/bin/python

import os
import sys
import gzip
from argparse import ArgumentParser
from skylines import assets
from skylines.config import environment

# Build paths
base_path = os.path.dirname(sys.argv[0])

# Create argument parser
parser = ArgumentParser(description='Generate concatenated and minified CSS and JS assets.')
parser.add_argument('conf_path', nargs='?', metavar='config.ini',
                    help='path to the configuration INI file')
parser.add_argument('bundles_module', nargs='?', metavar='skylines.assets.bundles',
                    help='path to the bundles Python module')

# Parse arguments
args = parser.parse_args()

# Load config from file
conf = environment.load_from_file(args.conf_path)
if not conf:
    parser.error('Config file "{}" not found.'.format(args.conf_path))

# Create assets environment
env = assets.Environment(conf)

# Load the bundles from the YAML file
if args.bundles_module is None:
    args.bundles_module = conf['webassets.bundles_module']

print 'Loading bundles from {}'.format(args.bundles_module)
env.load_bundles(args.bundles_module)

# Generate the assets/bundles
for bundle in env:
    print 'Generating bundle: {}'.format(bundle.output)
    bundle.build()

    # Generate GZipped bundles for nginx static gzip serving
    bundle_path = bundle.resolve_output()
    compressed_path = bundle_path + '.gz'
    print 'Compressing bundle: {} -> {}'.format(os.path.basename(bundle_path),
                                                os.path.basename(compressed_path))
    with open(bundle_path, 'rb') as f_in, \
            gzip.open(compressed_path, 'wb') as f_out:
        f_out.writelines(f_in)