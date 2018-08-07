import os
import os.path as op
import tempfile
import IPython as ipy

from IPython.utils.process import getoutput

def exec_swipl(code):


    dirpath = '~/.local/share/jupyter/kernels/swi/temp'  # tempfile.mkdtemp()

    #code = 'return 0;'
    # We define the source and executable filenames.
    source_path = op.join(dirpath, 'temp.pl')
    target_path = op.join(dirpath, 'out.txt')
    program_path = op.join(dirpath)
    #print(str(source_path))
    #print((program_path))
    with open(source_path, 'w') as f:
        f.write(code)

    os.system("swipl {0:s} > {1:s}".format(source_path, target_path))  # source_path, program_path))
    #result = ipy.get_ipython().getoutput(os.system("swipl {0:s} ".format(source_path)), split=True)  # source_path, program_path))

    #output = open(target_path, "r")
    return getoutput(target_path)
    


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SwiplKernel)
