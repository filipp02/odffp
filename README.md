Orientation Distribution Function Fingerprinting (ODF-FP)
=========================================================

This is a Python implementation of ODF-FP – a dictionary-based white matter fiber reconstruction algorithm that implements the forward modeling approach to diffusion MRI [1,2]. By replacing the common ODF-peak finding mechanism with pattern matching, ODF-FP can identify fibers crossing at shallow angles below 40 degrees [1]. 

Standard ODF-dictionary is generated randomly with the uniform distribution of tissue microstructure parameters [2]. The stepwise stochastic dictionary mechanism [3] enables generation of ODF-dictionaries drawn with a posterior distribution of parameters inferred from the input dMRI. 

An additional anisotropy boosting factor [4] is used to counterbalance the drop of diffusion anisotropy in edematous regions to improve white matter fiber identification in proximity to brain tumors.


References
----------

* [1] Baete, S.H., Cloos, M.A., Lin, Y.C., Placantonakis, D.G., Shepherd, T. and Boada, F.E., Fingerprinting Orientation Distribution Functions in diffusion MRI detects smaller crossing angles. Neuroimage, 198, pp. 231-241, 2019, https://doi.org/10.1016/j.neuroimage.2019.05.024 

* [2] Filipiak, P., Shepherd, T., Lin, Y.C., Placantonakis, D.G., Boada, F.E. and Baete, S.H., Performance of orientation distribution function‐fingerprinting with a biophysical multicompartment diffusion model. Magnetic Resonance in Medicine, 88(1), pp.418-435, 2022, https://doi.org/10.1002/mrm.29208

* [3] Filipiak, P., Shepherd, T., Basler, L., Zuccolotto, A., Placantonakis, D.G., Schneider, W., Boada, F.E. and Baete, S.H., Stepwise Stochastic Dictionary Adaptation Improves Microstructure Reconstruction with Orientation Distribution Function Fingerprinting. International Workshop on Computational Diffusion MRI (CDMRI'22), Springer Nature Switzerland, pp. 89-100, 2022, https://doi.org/10.1007/978-3-031-21206-2_8

* [4] Filipiak, P., Shepherd, T.M., Clarke, K., Ressa, G., Placantonakis, D.G., Boada, F.E. and Baete, S.H., Clinically Feasible White Matter Fiber Tractography in Peritumoral Zones With Cerebral Vasogenic Edema. Magnetic Resonance in Medicine, 2026, https://doi.org/10.1002/mrm.70314
