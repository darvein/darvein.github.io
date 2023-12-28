# Compression notes

There are different ways to compress in a linux environment with general compression algorithms and so.

## Tar and GZIP

tar:
> GNU 'tar' saves many files together into a single tape or disk archive, and can restore individual files from the archive.

gzip
> Compress or uncompress FILEs (by default, compress FILES in-place).

Both are different tools, but `tar` can call `bzip` in order to compress an archived file.

## Compression

Currently exists a variaty of compression techniques and algorithms.

The popular ones:

gzip:
> Compress or uncompress FILEs (by default, compress FILES in-place).

gzip2:
> bzip2, a block-sorting file compressor.  Version 1.0.8, 13-Jul-2019.

lzma / xz:
Compress or decompress FILEs in the .xz format.

All of them supports the same preset of compressions which are from 1 (fast) to 9 (best).

## Performance

The features to consider while testing the performance are: Compression file size, Compression ratio and Comprestion time.

Basically a comparision between, gzip, gzip2 and lzma/xz

- gzip: compression ratio is low and compresion time is slow
- lzma: compression ratio is high and compression time is fast (decompression is very low, twice as gzip)
- bzip2: sits in the middle of gzip and lzma, it is a block-based compression

## Benchmarks:

- https://catchchallenger.first-world.info/wiki/Quick_Benchmark:_Gzip_vs_Bzip2_vs_LZMA_vs_XZ_vs_LZ4_vs_LZO
- https://www.rootusers.com/gzip-vs-bzip2-vs-xz-performance-comparison/
