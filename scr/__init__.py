from typing import Tuple
import os
import subprocess
import shutil

def _genome_id_parser(id:str) -> Tuple[str, str]:
    #examople id GCA_003841505.1
    prefix, numbers = id.split('_')
    numbers = numbers.split('.')[0]
    return prefix, numbers


def get_link_to_genome_folder(id:str) -> str:
    #formats link to download
    genome_id_prefix, genome_number = _genome_id_parser(id)
    num_splited = [genome_number[i:i+3] for i in range(0, len(genome_number), 3)]
    pre_link = (f'https://ftp.ncbi.nlm.nih.gov/genomes/all/{genome_id_prefix}/',
                f'{num_splited[0]}/{num_splited[1]}/{num_splited[2]}/')
    pre_link_join = ''.join(pre_link)

    return pre_link_join


def downloader(url, path_assembly):
    #Will download and unpack everything 
    # to specific folders
    subprocess.run(['wget', '-r', '-q', '-nd','--no-parent', '-e robots=off', url],
                   cwd=path_assembly)

def downloader_lite():
    pass


def unzipper(file_path):
    subprocess.run(['gunzip', '-q', file_path])


def renamer(old_path, prot):
    """Renames protein file of microbe to reflect its name.

    This function will take protein file and rename it based on the
    first line of it's FASTA header. The new name will be in format:
    '_microbe_name.faa' where microbe_name is the name of microbe
    in FASTA header.

    Args:
        old_path (str): Path to folder where protein file is placed.
        prot (str): Name of protein file.
    """
    fpath_proteome = os.path.join(old_path, prot)
    with open(fpath_proteome, 'r', encoding='utf8') as proteome_file:
        first_line = proteome_file.readline()

    microbe_name = f"_{first_line.split('[')[-1].split(']')[0].strip().replace(' ', '_')}.faa"

    new_assemblie_name = prot.replace('.faa', microbe_name)
    updated_path = os.path.join(old_path, new_assemblie_name)
    os.rename(fpath_proteome, updated_path)


def file_mover(path_asembly, prot_path, nucl_path):
    folder_files = os.listdir(path_asembly)
    for i in folder_files:
        if '_protein.faa.gz' in i:
            protein_file_suf = i
        if '_genomic.fna.gz' in i:
            nucl_file_suf = i

    shutil.copy(os.path.join(path_asembly, protein_file_suf),
                os.path.join(prot_path, protein_file_suf))

    shutil.copy(os.path.join(path_asembly, nucl_file_suf),
                os.path.join(nucl_path, nucl_file_suf))
    
    subprocess.run(['gunzip', '-q', os.path.join(prot_path, protein_file_suf)])
    subprocess.run(['gunzip', '-q', os.path.join(nucl_path, nucl_file_suf)])

  