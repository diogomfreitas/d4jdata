import tarfile
import os.path
import gzip
import shutil

from src import outcomeMatrixToKillMatrix

ERROR_PARTITION_SCHEMES = {
  'all',
  'type',
  'type+message',
  'type+message+location',
  'exact',
  'passfail'
}

def run_outcomeMatrixToKillMatrix(error_partition_scheme, path, program, versions):
    for v in range(0, int(versions)):
        outcomeMatrixToKillMatrix.genKillage(error_partition_scheme,
                                                     path + "/" + program + "/" + str(v+1) + "/killmap.csv",
                                                     path + "/" + program + "/" + str(v+1) + "/mutants.log",
                                                     path + "/" + program + "/" + str(v+1) + "/killage.csv")

#A ordem de preferencia dos killmaps eh: 168h, 32h-unoptimized e então 32h
def unzipKillmaps(dataDir, program, versions):
    for v in range(0, int(versions)):
        file_path = dataDir + program + "/" + str(v+1) + "/"
        file_path_killmaps = dataDir + "killmaps/" + program + "/" + str(v+1) + "/"
        file_path_killmaps_unoptimized = dataDir + "killmaps-unoptimized/" + program + "/" + str(v+1) + "/"
        tarFileName = "32h-unoptimized-killmap-files.tar.gz"


        if not os.path.isfile(file_path + tarFileName):
            tarFileName = "32h-killmap-files.tar.gz"

            if not os.path.isfile(file_path + tarFileName):
                tarFileName = "168h-killmap-files.tar.gz"


        with tarfile.open(file_path + tarFileName) as tar:
            subdir_and_files = [
                tarinfo for tarinfo in tar.getmembers()
                if tarinfo.name.endswith('killmap.csv.gz')
            ]
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, members=subdir_and_files, path=dataDir)

        with tarfile.open(file_path + tarFileName) as tar:
            subdir_and_files = [
                tarinfo for tarinfo in tar.getmembers()
                if tarinfo.name.endswith("mutants.log")
            ]
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, members=subdir_and_files, path=dataDir)


        if tarFileName.find("unoptimized") != -1:
            unzip_gz_file(file_path_killmaps_unoptimized, file_path, "killmap.csv")

            # move mutants.log from killmaps-unoptimized/ to data/ dir:
            shutil.move(file_path_killmaps_unoptimized + "mutants.log", file_path + "mutants.log")
        else:
            unzip_gz_file(file_path_killmaps, file_path, "killmap.csv")

            # move mutants.log from killmaps/ to data/ dir:
            shutil.move(file_path_killmaps + "mutants.log", file_path + "mutants.log")


def unzip_gz_file(file_path_before, file_path_after, filename):
    fp = open(file_path_after + filename, "wb")
    with gzip.open(file_path_before + filename + ".gz", "rb") as f:
        bindata = f.read()
    fp.write(bindata)
    fp.close()


def unzip_gzolgars(dataDir, program, versions):
    for v in range(0, int(versions)):
        file_path = dataDir + program + "/" + str(v+1) + "/"
        ziped_file_path = dataDir + "gzoltars/" + program + "/" + str(v + 1) + "/"
        tarFileName = "gzoltar-files.tar.gz"


        with tarfile.open(file_path + tarFileName) as tar:
            subdir_and_files = [
                tarinfo for tarinfo in tar.getmembers()
                if tarinfo.name.endswith('matrix')
            ]
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, members=subdir_and_files, path=dataDir)

        # move matrix file from gzolgars/ to data/ dir:
        shutil.move(ziped_file_path + "matrix", file_path + "matrix")

        with tarfile.open(file_path + tarFileName) as tar:
            subdir_and_files = [
                tarinfo for tarinfo in tar.getmembers()
                if tarinfo.name.endswith("spectra")
            ]
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, members=subdir_and_files, path=dataDir)

        # move spectra file from gzolgars/ to data/ dir:
        shutil.move(ziped_file_path + "spectra", file_path + "spectra")

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--error-partition-scheme', required=True, choices=ERROR_PARTITION_SCHEMES)
    parser.add_argument('--dataDir', required=True, help='path to the root directory')
    parser.add_argument('--program', required=True, help='name of the program')
    parser.add_argument('--versions', required=True, help='number of versions')

    args = parser.parse_args()

    unzipKillmaps(args.dataDir, args.program, args.versions)
    run_outcomeMatrixToKillMatrix(args.error_partition_scheme, args.dataDir, args.program, args.versions)

    unzip_gzolgars(args.dataDir, args.program, args.versions)
