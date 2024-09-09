import argparse
import os
from datetime import datetime
import shutil
from tqdm import tqdm
from . import (_genome_id_parser,
               get_link_to_genome_folder,
               downloader_full,
               renamer,
               file_mover,
               unzipper,
               downloader_unzipper, 
               version_printer)

def argument_parser() -> argparse.ArgumentParser: 
    parser = argparse.ArgumentParser(
        prog='Bulk Genome Assembly Downloader',
        description= 'Programm to download genome assemblies. \
                        From NCBI through FTP'
    )
    
    parser.add_argument('-i', 
                        '--input',
                        help='Path to file with assembly ID. \
                            All of them should be in one column',
                        type=str)
    parser.add_argument('-o',
                        '--output',
                        help='Path to folder to store genomes',
                        type=str,
                        required=True)
    
    parser.add_argument('-m',
                        '--mode',
                        help='Full or light download from ftp.\
                            Full == all files from FTP, Lite == genome, proteome from NCBI DATASET.\
                            Lite version much faster.',
                        type=str,
                        default='full',
                        choices=['lite', 'full'])
    return parser


def main():
    parser = argument_parser()
    args = parser.parse_args()

    input_abs_path = os.path.abspath(args.input)
    output_abs_path = os.path.abspath(args.output)

    terminal_size = shutil.get_terminal_size()
    start_time = datetime.now()
    version_printer(terminal_size)

    with open(input_abs_path, 'r') as read_file:
        assemblies_lst = [i.strip('\n').replace('"', '').strip()
                          for i in read_file.readlines()]

    all_assembly_folder = os.path.join(output_abs_path, 'assemblies')
    all_proteomes_folder = os.path.join(output_abs_path, 'proteomes')
    all_nucleotide_folder = os.path.join(output_abs_path, 'nucleoitede')

    try:
        os.mkdir(all_assembly_folder)
        os.mkdir(all_proteomes_folder)
        os.mkdir(all_nucleotide_folder)
    except FileExistsError:
        pass #passet exeption

    for assembly in tqdm(assemblies_lst, desc='Downloading...'):
        files_to_unzip = ()
        genome_folder = os.path.join(all_assembly_folder, assembly)
        assembly_url = get_link_to_genome_folder(assembly)

        os.mkdir(genome_folder)

        #options
        if args.mode == 'full':
            downloader_full(assembly_url, genome_folder)
            files_to_unzip += file_mover(genome_folder, all_proteomes_folder, all_nucleotide_folder)

            for path in files_to_unzip:
                unzipper(path)

        elif args.mode == 'lite':
            downloader_unzipper(assembly, all_assembly_folder,
                                all_proteomes_folder, all_nucleotide_folder)

    for file in os.listdir(all_proteomes_folder):
        renamer(all_proteomes_folder, file)

    print('-' * terminal_size[0])
    print(f'Script working time: {datetime.now() - start_time}')
    print('-' * terminal_size[0])
    