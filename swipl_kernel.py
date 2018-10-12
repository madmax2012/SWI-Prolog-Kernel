import os
import os.path as op
import tempfile
import IPython
import jupyter_client
from IPython.utils.process import getoutput
from backports import tempfile

def exec_swipl(code):
    temp_path, output_path, code_path = setup_env()
    preCode1 = 'doa([]).\n\n' 
    preCode2 = 'doa( [G|_] ) :-  write(\' \\n----------------------------------------- \\n Call of: \\t \'), write(G), call(G), write(\' \\n TRUE with:\\t \'), write(G), fail.\n\n'
    preCode3 = 'doa( [G|R] ) :- not(G), !, write(\' \\n FALSE!  \\t \'), write(G), doa(R).\n\n'
    preCode4 = 'doa( [_|R] ) :- doa(R).\n\n'
    emptyline = '\n'
    startQuery = ':- doa(['
    endQuery = ']).'
    with open(temp_path, 'w') as f: # 
        f.write(code)
    ''' Parser code begins here '''
    textlist = []
    textlist.append(preCode1)
    textlist.append(preCode2)
    textlist.append(preCode3)
    textlist.append(preCode4)
    textlist.append(emptyline)
    with open(temp_path) as f: 
        ''' 
        some hacky logic to enable students to simply add queries
        after defining their ruleset. 
        '''
        for line in f:
            textlist.append(line)
            if 'QUERYSTART' in line:
                textlist.pop() # get rid of start marker
                textlist.append(startQuery) 
            if 'QUERYEND' in line:
                textlist.pop() # get rid of end marker
                textlist.append(endQuery) 
    print(''.join(textlist))
    with open(code_path, 'w') as rules:
        rules.write(''.join(textlist))

    os.system("swipl {0:s} > {1:s}  2>&1 ".format(code_path, output_path)) 
    l = open(output_path, 'r')
    lines = l.readlines()
    l.close()
    lines = lines[:-9]
    t = open(output_path, 'w')
    for line in lines:
        t.write(line)

    t.close()
    f = open(output_path, 'r')
    
    return f.read()

def setup_env():
    dirpath =  tempfile.mkdtemp()
    temp_path = op.join(dirpath, 'temp.pl')
    output_path = op.join(dirpath, 'out.txt')
    code_path = op.join(dirpath, 'code.pl')
    return temp_path, output_path, code_path 


    

"""SWI-Prolog kernel wrapper"""
from ipykernel.kernelbase import Kernel

class SwiplKernel(Kernel):
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


