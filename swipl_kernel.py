import os
import os.path as op
import tempfile
import IPython as ipy

from IPython.utils.process import getoutput

def exec_swipl(code):


    dirpath = '/home/max/.local/share/jupyter/kernels/swi/temp'  # tempfile.mkdtemp()

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
    

"""SWI-Prolog kernel wrapper"""
from ipykernel.kernelbase import Kernel

class SwiplKernel(Kernel):

    # Kernel information.
    implementation = 'SWI-Prolog'
    implementation_version = '0.0'
    language = 'Prolog'
    language_version = '1.0'
    language_info = {'name': 'swipl',
                     'mimetype': 'text/plain'}
    banner = "SWI-Prolog Kernel"

    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):
        """This function is called when a code cell is
        executed."""
        if not silent:
            # We run the Prolog code and get the output.
            output = exec_swipl(code)

            # We send back the result to the frontend.
            stream_content = {'name': 'stdout',
                              'text': output}
            self.send_response(self.iopub_socket,
                              'stream', stream_content)
        return {'status': 'ok',
                # The base class increments the execution
                # count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SwiplKernel)
