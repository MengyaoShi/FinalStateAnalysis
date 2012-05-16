#!/usr/bin/env python
'''

Convert ROOT trees into an HDF5 File

'''

from RecoLuminosity.LumiDB import argparse
from progressbar import ETA, ProgressBar, FormatLabel, Bar
import glob
import logging
import os
import sys
import tables
import time

log = logging.getLogger("convertHD5")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    input_grp = parser.add_argument_group('input')

    input_grp.add_argument('tree', metavar='path_to_tree', type=str,
                        help='Path to TTree in data files')

    input_grp.add_argument('inputs', metavar='input.root', type=str,
                        nargs='+', help="Input file globs")

    input_grp.add_argument('--chainsize', default=100, type=int,
                        help="Group input files into chunks of size (MB)")

    output_grp = parser.add_argument_group('output')

    output_grp.add_argument('--output', required=True,
                        type=str, help='Output .h5 file')

    output_grp.add_argument('--name', default='data',
                        type=str, help='Table name')

    output_grp.add_argument('--where', default='/',
                        type=str, help='Group output')

    output_grp.add_argument('--complib', default='blosc',
                        type=str, help='Compression type')

    output_grp.add_argument('--complevel', default=5,
                        type=int, help='Compression level')

    parser.add_argument('--verbose', action='store_const', const=True,
                        default=False, help='Print debug output')

    args = parser.parse_args()

    sys.argv[:] = []
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    log.info("Loading ROOT libraries")
    import ROOT
    from rootpy.root2array import tree_to_recarray

    flat_files = []
    for fileglob in args.inputs:
        flat_files.extend(glob.glob(fileglob))

    log.info("Merging %i input ROOT files", len(flat_files))

    chain = ROOT.TChain(args.tree)
    for file in flat_files:
        chain.Add(file)

    entries = chain.GetEntries()
    log.info("There are %i rows in the input", entries)

    filters = tables.Filters(complib=args.complib, complevel=args.complevel)

    pbar = ProgressBar(widgets=[
        FormatLabel('Processed %(value)i/' + str(len(flat_files)) + ' files. '),
        ETA(), Bar('>')], maxval=len(flat_files)).start()

    # Chunk files into TChains
    def chunk_files(input_files, max_size):
        current_size = 0
        current_chunk = []
        for file in input_files:
            current_chunk.append(file)
            current_size += os.path.getsize(file)/1e6
            if current_size > max_size:
                yield current_chunk
                current_chunk = []
                current_size = 0
        yield current_chunk

    table = None

    ROOT.TTreeCache.SetLearnEntries(1)

    time_in_read = 0
    time_in_append = 0
    processed_files = 0

    log.info("Opening output file: %s", args.output)
    try:
        hfile = tables.openFile(filename=args.output, mode="w", title="Data",
                                filters=filters)

        for file_chunk in chunk_files(flat_files, args.chainsize):
            t1 = time.time()
            chunk_chain = ROOT.TChain(args.tree)
            chunk_chain.SetCacheSize(10000000)
            for file in file_chunk:
                chunk_chain.Add(file)
            recarray = tree_to_recarray(chunk_chain, None, False)
            t2 = time.time()
            time_in_read += t2 - t1

            t1 = time.time()
            if table is None:
                log.info("Creating table")
                table = hfile.createTable(args.where, args.name,
                                          recarray,
                                          "", filters=filters,
                                          expectedrows=entries)
            else:
                table.append(recarray)
            table.flush()
            t2 = time.time()
            time_in_append += t2 - t1

            processed_files += len(file_chunk)
            pbar.update(processed_files)

    except KeyboardInterrupt:
        print
        print "Caught Ctrl-c"
    finally:
        log.info("%0.0f seconds spent reading TTrees", time_in_read)
        log.info("%0.0f seconds spent writing Tables", time_in_append)
        log.info("Wrote %i rows", table.nrows)
        log.info("Closing file")
        hfile.close()

