# Bulk Prokariotic Genome Assembly Downloader

A terminal tool to download multiple genome assemblies from NCBI FTP server.

The terminal tool is written in `Python3` it uses:
* `requests` library to download files from the NCBI FTP server.
* `wget` to download files from the NCBI FTP server (in `full` mode)
* `curl` to download some filess from the NCBI DATASET server (in `lite` mode)

## Installation

Just download repisitory and unzip it in some folder.

Command to use:

`python ./ncbi_downloader.py -h`

It will open mannual in the terminal and show avalable options.

## Outputs

Three folders:
1. assemblies -- Folder with all files from FTP/NCBI DATASETS
2. proteomes -- .faa files for in silico proteomes. Name contains microorganim name
3. nucleotides -- .fna file from genome

## Mention

Perhaps it will work not only with prokaryotic genome but with eukaryotic, however I did not try it.