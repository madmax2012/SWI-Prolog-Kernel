import os
import os.path as op
import tempfile
import IPython as ipy


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SwiplKernel)
