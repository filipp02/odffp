import numpy as np
import nibabel as nib
import time
import os, sys
import pickle

from dipy.core.gradients import gradient_table
from dipy.io.image import load_nifti, save_nifti
from dipy.io.gradients import read_bvals_bvecs

from odffp.model import OdffpDictionary, OdffpModel
from dipy.reconst.gqi import GeneralizedQSamplingModel

from datetime import datetime

start_time = datetime.now()

dwi_file  = "dwi.nii.gz"
bvec_file = "dwi.bvec"
bval_file = "dwi.bval"

healthy_mask_file = "roi_brain_minus_edema.nii.gz"
edema_mask_file = "roi_edema.nii.gz"

output_dir = "output"
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
   

# ODF-dictionary

use_equal_fibers = False

odf_dict_size = 1000000
odf_recon_edge = 1.20
odf_dict_edge = 1.20
odf_max_peaks_num = 3

# microstructure parameter ranges
p_iso = [0.0,1.0]
p_fib = [0.0,1.0]
f_in  = [0.0,1.0] 
D_iso = [2.0,3.0]
D_a   = [1.5,2.5]
D_e   = [1.5,2.5]
D_r   = [0.5,1.5]
    
assert_faster_D_a = True # D_a > D_e
tortuosity_approximation = False
max_chunk_size = 1000 # Bigger chunks work faster, but use more RAM

runs_num = 1
fit_penalty = 1e-5  
healthy_peak_boost = 0.00 # Can be higher (e.g., 0.10)
edema_peak_boost = 0.15 # Can be higher (e.g., 0.30)

# Uncomment if you want the same ODF-dictionary at each run
# np.random.seed(0)


for run in range(runs_num):

    method = "dipy.dict%dk.kde.%s_edema_roi_qa_boost%03d.faster_da.penalty%06d" % (
        np.round(0.001*odf_dict_size),  
        'equal' if use_equal_fibers else 'full', 
        np.round(100*edema_peak_boost), 
        np.round(100000*fit_penalty)
    )
     
    output_file = "%s/dwi_edge-r%03d-d%03d_run%03d.fib.gz" % (output_dir, np.round(100*odf_recon_edge), np.round(100*odf_dict_edge), run)
    
    data, affine, voxel_size = load_nifti(dwi_file, return_voxsize=True)
    bvals, bvecs = read_bvals_bvecs(bval_file, bvec_file)

    # Flip bx, because DIPY is peculiar about b-vecs
    bvecs *= [-1,1,1]
    gtab = gradient_table(bvals, bvecs)
    
    healthy_mask, _ = load_nifti(healthy_mask_file)
    edema_mask, _ = load_nifti(edema_mask_file)
        
    print(datetime.now().strftime("%H:%M:%S"), "Loading ODF-dictionary...")
     
    recon_model = GeneralizedQSamplingModel(gtab, sampling_length=odf_recon_edge)
    dict_model = GeneralizedQSamplingModel(gtab, sampling_length=odf_dict_edge)
        
    odf_dict = OdffpDictionary(gtab)
    
    odf_dict.generate(
        dict_size=odf_dict_size, max_peaks_num=odf_max_peaks_num, equal_fibers=use_equal_fibers,
        p_iso=p_iso, p_fib=p_fib, f_in=f_in, 
        D_iso=D_iso, D_a=D_a, D_e=D_e, D_r=D_r,
        odf_recon_model=dict_model,
        assert_faster_D_a=assert_faster_D_a, tortuosity_approximation=tortuosity_approximation
    )
    
    print(datetime.now().strftime("%H:%M:%S"), "Fitting...")
    
    odffp = OdffpModel(
        gtab, odf_dict, drop_negative_odf=True, zero_baseline_odf=False, output_dict_odf=True, 
        odf_recon_model=recon_model
    )

    odffp_healthy_fit = odffp.fit(data, healthy_mask, penalty=fit_penalty, peak_boost=healthy_peak_boost, max_chunk_size=max_chunk_size)
    odffp_edema_fit = odffp.fit(data, edema_mask, penalty=fit_penalty, peak_boost=edema_peak_boost, max_chunk_size=max_chunk_size)
    
    odffp_healthy_fit.merge(odffp_edema_fit)
    
    print(datetime.now().strftime("%H:%M:%S"), "Exporting to FIB...")
    odffp_healthy_fit.save_as_fib(affine, voxel_size, output_file)    
    
    print(datetime.now().strftime("%H:%M:%S"), "DONE!")
    print("\nRUNTIME:", datetime.now() - start_time)
