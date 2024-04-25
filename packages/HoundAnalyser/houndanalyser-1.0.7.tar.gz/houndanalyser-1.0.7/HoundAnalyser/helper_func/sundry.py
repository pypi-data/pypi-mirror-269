import os
import textwrap as tw
from copy import deepcopy


def _find_tool(tool_name: str):
    """
        Uses system shell to locate `tool_name', and return the
        absolute path of the tool.
    """
    cmd_output = os.popen('whereis ' + tool_name).read()
    if len(cmd_output.split(' ')) > 1:
        if tool_name == str('samtools') and \
         str('samtools.pl') in cmd_output.split(' ')[1].strip('\n'):
            # Check samtools.pl is not returned. If it does, take next
            # entry (typically /usr/bin/samtool)
            return cmd_output.split(' ')[2].strip('\n') + str(' ')

        return cmd_output.split(' ')[1].strip('\n') + str(' ')
    else:
        msg = str("(Hound *BARKED*) Program %s is not in the system PATH."
                  % tool_name)
        raise ValueError(tw.fill(msg))
        os.sys.exit(-2)


def _is_indexed(input_seq: str):
    """
        Checks if a sequence has been indexed, and if it is not... index it.
    """
    PATH = str('/').join(input_seq.split('/')[:-1])
    FILE = input_seq.split('/')[-1]
    INTPUT_LIST = [f for f in os.listdir(PATH) if FILE.split('.')[0] in f]
    if len(INTPUT_LIST) > 1:
        print("Sequence already indexed, nothing done.")
    else:
        print("Indexing reference sequence...")
        bwa = _find_tool('bwa')
        os.system(bwa + 'index ' + input_seq)


def _check_project_exists(illumina_rds: str, project_name: str) -> str:
    """
        For the case where readings are mapped onto a reference, checks
        whether project directory exists---if not, create it.
    """
    ALN_dir = str('alignments')
    UNALN_dir = ALN_dir + str('/') + str('unmapped_reads')
    # SPAdes results in a .fa before .bam, not here.
    ASSEMBLY_dir = str('assemblies/reference_mapped')

    # This arrangement prioritises 'project_name'. To use directory name
    # from illumina reads, ignore 'project_name' (defaults to 'None')
    if project_name is not None:
        root_path = illumina_rds[:illumina_rds.find(project_name)]  # Includes /
        PRJ_PATH = root_path + project_name
    else:
        raise ValueError("(Hound *BARKED*) I need a project name to proceed.")
        os.sys.exit(-3)

    rd_fName = illumina_rds.split('/')[-1]
    if os.path.exists(PRJ_PATH) is False:
        os.makedirs(PRJ_PATH)  # Can create parent and child at once
    else:
        msg = str("(Hound *GROWLED*) Project directory already exists, " \
                  "beware that any existing data will be overwritten.")
        print(tw.fill(msg))
    if os.path.exists(PRJ_PATH + '/' + ALN_dir) is False:
        os.mkdir(PRJ_PATH + '/' + ALN_dir)
        os.mkdir(PRJ_PATH + '/' + UNALN_dir)
    if os.path.exists(PRJ_PATH + '/' + ASSEMBLY_dir) is False:
        os.makedirs(PRJ_PATH + '/' + ASSEMBLY_dir)
    return rd_fName, PRJ_PATH, ALN_dir, UNALN_dir, ASSEMBLY_dir


def _check_directory(template: str, dir_name: str, target_dir: str,\
                     export_filename=True) -> str:
    """
        For the case where readings are assembled de novo, check directory
        exists---if not, create it.
    """
    # Sanitise template name by removing filename included
    tmp = template.split('/')[:-1]
    fName = template.split('/')[-1]
    template = str('/').join(tmp)

    # Check/create directory as needed
    if len(target_dir) > 0 and target_dir.isspace() is False:
        newdir_name = template.replace(target_dir, dir_name)
    else:
        newdir_name = template

    if os.path.exists(newdir_name) is False:
        print(newdir_name)
        os.makedirs(newdir_name)

    if export_filename is True:
        return str('/').join([newdir_name, fName])
    else:
        return newdir_name


def _cleanup_path(input_file: str, project_name: str):
    """
        Detect project name in path given by *input_file* to allow
        better manipulation of relative paths within a project.
    """
    p_id = input_file.find(project_name)
    tmp = input_file[p_id+len(project_name)+1:]  # +1 to avoid including '/'
    filename = tmp.split('/')[-1]
    relative_path = str('/').join(tmp.split('/')[:-1])
    return relative_path, filename
