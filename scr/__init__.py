from typing import Tuple
import os
import subprocess
import shutil
from glob import glob
def _genome_id_parser(assembly_id:str) -> Tuple[str, str]:
    """
    Function to parse assembly id into two parts: prefix and numbers.
    
    Parameters
    ----------
    assembly_id : str
        String with assembly id, e.g. GCA_003841505.1
    
    Returns
    -------
    Tuple[str, str]
        A tuple with two strings: prefix and numbers. e.g. (GCA, 003841505) 
    """
    prefix, numbers = assembly_id.split('_')
    numbers = numbers.split('.')[0]
    return prefix, numbers


def get_link_to_genome_folder(assembly_id:str) -> str:
    """
    Formats link to download genome assembly from NCBI FTP server.
    
    Parameters
    ----------
    assembly_id : str
        String with assembly id, e.g. GCA_003841505.1
    
    Returns
    -------
    str
        A string with link to download genome assembly.
    """
    genome_id_prefix, genome_number = _genome_id_parser(assembly_id)
    num_splited = [genome_number[i:i+3] for i in range(0, len(genome_number), 3)]
    pre_link = (f'https://ftp.ncbi.nlm.nih.gov/genomes/all/{genome_id_prefix}/',
                f'{num_splited[0]}/{num_splited[1]}/{num_splited[2]}/')
    pre_link_join = ''.join(pre_link)

    return pre_link_join


def downloader_full(url:str, path_assembly:str) -> None:
    """
    Downloads all files from given URL (NCBI FTP server) 
    into folder path_assembly. 

    Parameters
    ----------
    url : str
        URL of FTP server of NCBI, where genomes 
        and addtion files are stored.
    path_assembly : str
        Folder where all files will be downloaded.

    Returns
    -------
    None
    """
    subprocess.run(['wget', '-r', '-q', '-nd','--no-parent', '-e robots=off', url],
                   cwd=path_assembly,
                   check=True)


def unzipper(file_path:str) -> None:
    """
    Unzips a single .gz file.
    Uses build in 'gunzip' command.
    Parameters
    ----------
    file_path : str
        Path to the file to be unzipped.
    """
    subprocess.run(['gunzip', '-q', file_path], check=True)


def downloader_unzipper(assembly_id:str, path_assembly:str,
                        prot:str, assembly:str) -> None:
    """Downloading assemblies from NCBI through CURL thoroug NCBI API. 

    Args:
        assembly_id (str): ID of assembly. e.g. GCA_000000000.1
        path_assembly (str): Directory where curl store archives and zip unzip them 
        prot (str): Path to the folder where is proteome will be plced.
        assembly (str): Path to the folder where is assembly will be plced.
    """
    subprocess.run(['curl', '-OJX',  'GET',
                    f"https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{assembly_id}/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename={assembly_id}.zip"], 
                    cwd=path_assembly, check=False)
    subprocess.run(['unzip', '-q', f'{assembly_id}.zip'],
                   cwd=path_assembly, check=False)
    subprocess.run(['cp', f'./ncbi_dataset/data/{assembly_id}/protein.faa',
                    f'{prot}/{assembly_id}.faa'],
                   cwd=path_assembly, check=False)
    
    fna_file_path = glob(f'{path_assembly}/ncbi_dataset/data/{assembly_id}/*_genomic.fna')[0]

    subprocess.run(['cp', f'{fna_file_path}',
                    f'{assembly}/'],
                   cwd=path_assembly, check=False)
    subprocess.run(['cp', '-r', f'./ncbi_dataset/data/{assembly_id}',
                    f'{path_assembly}/'],
                   cwd=path_assembly, check=False)
    subprocess.run(['rm', 'README.md'],
                   cwd=path_assembly, check=False)
    subprocess.run(['rm', 'md5sum.txt'],
                   cwd=path_assembly, check=False)
    subprocess.run(['rm', '-r', './ncbi_dataset'],
                   cwd=path_assembly, check=False)
    subprocess.run(['rm', f'{assembly_id}.zip'],
                   cwd=path_assembly, check=False)


def renamer(old_path:str, prot:str) -> None:
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


def file_mover(path_assembly:str, prot_path:str,
               nucl_path:str) -> Tuple[str, str]:
    """
    Moves protein and nucleotide files from one folder to two different
    folders.
    
    Args:
        path_assembly (str): Path to folder where assembly is placed.
        prot_path (str): Path to folder where proteome will be placed.
        nucl_path (str): Path to folder where nucleotide sequence will be placed.
    
    Returns:
        Tuple[str, str]: Paths to moved files.
    """
    folder_files = os.listdir(path_assembly)
    protein_file_suf = None
    nucl_file_suf = None

    for i in folder_files:
        if '_protein.faa.gz' in i:
            protein_file_suf = i
        if '_genomic.fna.gz' in i:
            nucl_file_suf = i
            
    if protein_file_suf is None or nucl_file_suf is None:
        raise FileNotFoundError('Protein or nucleotide file not found.')

    shutil.copy(os.path.join(path_assembly, protein_file_suf),
                os.path.join(prot_path, protein_file_suf))
    
    shutil.copy(os.path.join(path_assembly, nucl_file_suf),
                os.path.join(nucl_path, nucl_file_suf))
    
    return (os.path.join(prot_path, protein_file_suf), os.path.join(nucl_path, nucl_file_suf))


def version_printer(terminal_size:Tuple[int, int]) -> None:
    """
    Prints version and author information of script.
    
    Parameters
    ----------
    terminal_size : Tuple[int, int]
        Size of terminal window.
    """
    script_name = 'Bulk Genome Assembly Downloader'
    version = 'Version: 0.03'
    last_update = 'Updated: 18.10.24'
    author = 'Tulenkov A.S.'
    affiliation = 'Winogradsky Institute of Microbiology, RAS'

    name_margin = terminal_size[0]//2 - len(script_name)//2
    version_margin = terminal_size[0]//2 - len(version)//2
    update_margin = terminal_size[0]//2 - len(last_update)//2
    author_margin = terminal_size[0]//2 - len(author)//2
    affiliation_margin = terminal_size[0]//2 - len(affiliation)//2

    #printing
    print('-' * terminal_size[0])
    print(f"{' ' * name_margin}{script_name}{' ' * name_margin}")
    print(f"{' ' * version_margin}{version}{' ' * version_margin}")
    print(f"{' ' * update_margin}{last_update}{' ' * update_margin}")
    print(f"{' ' * author_margin}{author}{' ' * author_margin}")
    print(f"{' ' * affiliation_margin}{affiliation}{' ' * affiliation_margin}")
    print('-' * terminal_size[0])
