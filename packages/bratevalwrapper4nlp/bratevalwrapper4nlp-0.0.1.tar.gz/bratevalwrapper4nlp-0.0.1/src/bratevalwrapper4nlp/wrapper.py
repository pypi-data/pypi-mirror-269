import os, shutil
import subprocess as sp
from glob import glob

GIT_BRATEVAL = "https://github.com/READ-BioMed/brateval"
GIT_BRATEVAL_BRANCH = "v0.3.2"

dpath = os.path.dirname(__file__)
git_dir = os.path.join(dpath, "git")
bin_dir = os.path.join(dpath, "bin")
bin_path = os.path.join(bin_dir, "brateval.jar")

def jarfile():
    ensure_jar()
    return bin_path

def validate_java(silent=False):
    try: sp.check_call(["java", "-version"], stderr=sp.DEVNULL if silent else None)
    except: return False
    return True

def validate_maven():
    try: sp.check_call(["mvn", "-version"])
    except: return False
    return True

def validate_git():
    try: sp.check_call(["git", "--version"])
    except: return False
    return True

def clone_compile_copy():
    assert validate_git(), "Git is not installed."
    # remove old data
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, ignore_errors=True)

    # clone repo
    ec = sp.check_call([
        "git", "clone", "-b", GIT_BRATEVAL_BRANCH, GIT_BRATEVAL, git_dir
    ])
    assert ec == 0, "Exit code was {} for git clone".format(ec)

    # compile
    assert validate_java(), "Java is not installed."
    assert validate_maven(), "Maven is not installed."
    ec = sp.check_call(["mvn", "-Dmaven.test.skip=true", "install"], cwd=git_dir)
    assert ec == 0, "Exit code was {} for mvn install".format(ec)

    # copy to bin directory
    jar_file = list(glob(os.path.join(git_dir, "target", "brateval-*-SNAPSHOT.jar")))
    assert len(jar_file) == 1, "Found {} jar files but expected exactly 1 jar file.".format(len(jar_file))
    jar_file = jar_file[0]

    os.makedirs(bin_dir, exist_ok=True)
    shutil.copyfile(jar_file, bin_path)

    # clean up repo
    shutil.rmtree(git_dir, ignore_errors=True)

def ensure_jar():
    if not os.path.exists(bin_path):
        clone_compile_copy()
    assert validate_java(silent=True), "Java is not installed."
    assert os.path.exists(bin_path), "JAR should be available at {} but is not there.".format(os.path.abspath(bin_path))
