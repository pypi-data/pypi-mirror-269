import subprocess
import datetime
import re
import os

__in_ext__ = "in"
__out_ext__ = "out"
__ans_ext__ = "ans"

# utility
def dropExtension(filename: str, extension: str):
    return filename.rstrip(extension)

def getFileName(filename, default):
    if filename is None:
        return default
    return filename

# === Run Each ===
def execute(sourceName: str,
            ioFileName: str = None,
            timeout: float = None,
            verbose: bool = True,
            ) -> (bool, int):
    rawName = dropExtension(sourceName, ".py")  # Drop extension

    # Direct file
    input_file = getFileName(ioFileName, rawName) + "." + __in_ext__
    output_file = getFileName(ioFileName, rawName) + "." + __out_ext__

    (fin, fout) = (None, None)
    try:
        fin = open(input_file, "r")
        fout = open(output_file, "w")

        start = datetime.datetime.now()     # execute target source code
        subprocess.call(
            f"python {rawName}.py",
            stdin=fin,
            stdout=fout,
            timeout=timeout
        )
        end = datetime.datetime.now()
        elapse = (end - start).microseconds // 1000     # check elapsed time

        if verbose:
            print(f"Executed '{sourceName}' for '{ioFileName}': {elapse}ms")
        return True, elapse
    except FileNotFoundError as e:          # There is not a file
        print(f"There is not file '{e.filename}'")
    except subprocess.TimeoutExpired:       # Limited time out
        if verbose:
            print(f"Timeout '{sourceName}' for '{ioFileName}'")
        return False, timeout
    finally:
        if fin is not None:     # close files
            fin.close()
        if fout is not None:
            fout.close()
    return False, 0

def test(sourceName: str,
            ioFileName: str = None,
            timeout: float = None,
            verbose: bool = True
            ):
    rawName = dropExtension(sourceName, ".py")  # Drop extension

    # execute
    (state, elapse) = execute(sourceName, ioFileName=ioFileName, timeout=timeout, verbose=False)
    if(not state):  # Run Fail
        if elapse == timeout and verbose:   # Timeout
            print(f"Timeout '{sourceName}' for '{ioFileName}'")
        return state, elapse

    # Direct file
    submit_file = getFileName(ioFileName, rawName) + "." + __out_ext__
    answer_file = getFileName(ioFileName, rawName) + "." + __ans_ext__

    (fsub, fans) = (None, None)
    try:
        fsub = open(submit_file, "r")
        fans = open(answer_file, "r")

        while True:
            # readline and normalization
            while subLine := fsub.readline():
                subLine = re.sub("\\s+", " ", subLine)
                subLine = subLine.strip()
                if len(subLine) > 0:
                    break
            while ansLine := fans.readline():
                ansLine = re.sub("\\s+", " ", ansLine)
                ansLine = ansLine.strip()
                if len(ansLine) > 0:
                    break

            if not subLine and not ansLine:     # Pass
                print(f"Passed {sourceName} for '{ioFileName}': {elapse}ms")
                return (True, elapse)
            elif subLine or ansLine:    # Continuous
                if subLine == ansLine:
                    pass
                else:   # Fail: unmatched
                    print(f"Failed {sourceName} for '{ioFileName}': {elapse}ms")
                    break
            else:   # Fail: unmatched
                print(f"Failed {sourceName} for '{ioFileName}': {elapse}ms")
                break

        return (False, elapse)
    except FileNotFoundError as e:
        print(f"There is not file '{e.filename}'")
    finally:
        if fsub is not None:
            fsub.close()
        if fans is not None:
            fans.close()


# === Run All ===
def executeAll(filename: str, ioPath: str = None, timeout: float = None, verbose: bool = True):
    if ioPath is None:
        ioPath = os.path.dirname(filename)

    for file in os.listdir(ioPath):
        if re.match("\\w+\\."+__in_ext__, file):
            ioFile = ioPath + '/' + dropExtension(file, "." + __in_ext__)
            execute(filename, ioFileName=ioFile, timeout=timeout, verbose=verbose)


def testAll(filename: str, ioPath: str = None, timeout: float = None, verbose: bool = True):
    if ioPath is None:
        ioPath = os.path.dirname(filename)

    for file in os.listdir(ioPath):
        if re.match("\\w+\\."+__in_ext__, file):
            ioFile = ioPath + '/' + dropExtension(file, "." + __in_ext__)
            test(filename, ioFileName=ioFile, timeout=timeout, verbose=verbose)
