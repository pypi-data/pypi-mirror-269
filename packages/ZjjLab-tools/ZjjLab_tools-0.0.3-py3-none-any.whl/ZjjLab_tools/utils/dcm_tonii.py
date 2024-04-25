import os
from joblib import Parallel, delayed
__all__ = ['dcm_tonii']
def do_dcm2nii(input,output,dirname=True):
        os.makedirs(output,exist_ok=True)
        if dirname:
            tmp=input.split('/')
            output+='/'+tmp[-1]
            os.makedirs(output,exist_ok=True)
        os.system('/home/dell/mricron/dcm2niix -z o -o {}  {}'.format(output,input))
        print(output)

def dcm_tonii(listdrs,output,n=20,dirname=True):
    Parallel(n_jobs=n)(delayed(do_dcm2nii)(listdrs[i],output,dirname) for i in range(0, len(listdrs)))




