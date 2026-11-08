# HybridNutrientModel

This repository contains the Python scripts used to temporally downscale annual-level simulation data of TP and TN concentration from IMAGE-GNM (Beusen et al., 2015; Beusen et al., 2016; Beusen et al., 2022a, Beusen et al., 2022b) to the monthly-scale with machine learning (random forest) methods for the periods 1980-2010 and 2010-2070. The monitoring data of TP and TN concentration used for training, validation and applying the downscaling approach is consistent with those obtained in Graham et al (2024) and processed to the monthly level specifically for rivers. The hybrid nutrient modelling framework for temporal downscaling is fully described in the study of Graham et al. (2026). Furthermore, the Shared Socio-economic Pathways (SSPs) and Representative Concentration Pathways (RCPs) associated with the annual TP and TN simulations and hydrological variables are described in Beusen et al. (2022). The historical data of annual TP and TN concentration from Beusen et al. (2016) over the period 1980-2010 and for future scenarios (Beusen et al., 2022) for 2010-2070 are both downscaled to the monthly level using the python scripts provided in this repository.

Description of scripts.

Script_Nutrients_1.py: Merging TP monitoring data with TP simulation data from IMAGE-GNM

Script_Nutrients_2.py: Training and saving the random forest model for TP

Script_Nutrients_3.py: Applying the hybrid model (without mass balance) for the historic period 1980-2010 and TP

Script_Nutrients_4.py: Merging TN monitoring data with TN simulation data from IMAGE-GNM

Script_Nutrients_5.py: Training and saving the random forest model for TN

Script_Nutrients_6.py: Applying the hybrid model (without mass balance) for the historic period 1980-2010 and TN

Script_Nutrients_7.py: Applying the hybrid model (without mass balance) for the period 2010-2015 and TP

Script_Nutrients_8.py: Applying the hybrid model (without mass balance) for the period 2010-2015 and TN

Script_Nutrients_9.py: Applying the hybrid model (without mass balance) for the period 2015-2100 and TP

Script_Nutrients_10.py: Applying the hybrid model (without mass balance) for the period 2015-2100 and TN

Script_Nutrients_MB1.py: Applying mass balance constraint for historic period (1980-2010) and TP

Script_Nutrients_MB2.py: Applying mass balance constraint for period 2010-2015 and TP

Script_Nutrients_MB3.py: Applying mass balance constraint for period 2015-2070 and TP

Script_Nutrients_MB4.py: Applying mass balance constraint for historic period (1980-2010) and TN

Script_Nutrients_MB5.py: Applying mass balance constraint for period 2010-2015 and TN

Script_Nutrients_MB6.py: Applying mass balance constraint for period 2015-2070 and TN

Script_Nutrients_SSPs_Merge_P.py: Combining the hybrid outputs for 2010-2015 and 2015-2070 for TP

Script_Nutrients_SSPs_Merge_N.py: Combining the hybrid outputs for 2010-2015 and 2015-2070 for TN

References

Beusen, A.H.W., van Beek, L.P.H., Bouwman, A.F., Mogollón, J.M., Middelburg, J.J., 2015. Coupling global models for hydrology and nutrient loading to simulate nitrogen and phosphorus retention in surface water - Description of IMAGE-GNM and analysis of performance. Geosci Model Dev 8, 4045–4067. https://doi.org/10.5194/GMD-8-4045-2015

Beusen, A.H.W., Bouwman, A.F., van Beek, L.P.H., Mogollón, J.M., Middelburg, J.J., 2016. Global riverine N and P transport to ocean increased during the 20th century despite increased retention along the aquatic continuum. Biogeosciences 13, 2441–2451. https://doi.org/10.5194/BG-13-2441-2016

Beusen, A.H.W., Doelman, J.C., van Beek, L.P.H., van Puijenbroek, P.J.T.M., Mogollón, J.M., van Grinsven, H.J.M., Stehfest, E., van Vuuren, D.P., Bouwman, A.F., 2022a. Exploring river nitrogen and phosphorus loading and export to global coastal waters in the Shared Socio-economic pathways. Global Environmental Change 72, 102426. https://doi.org/10.1016/J.GLOENVCHA.2021.102426

Beusen, A.H.W., Bouwman, A.F., 2022b. Future projections of river nutrient export to the global coastal ocean show persisting nitrogen and phosphorus distortion. Frontiers in Water 4, 893585. https://doi.org/10.3389/FRWA.2022.893585/TEXT

Graham, D.J., Bierkens, M.F.P., van Vliet, M.T.H., 2024. Impacts of droughts and heatwaves on river water quality worldwide. J Hydrol (Amst) 629, 130590. https://doi.org/10.1016/J.JHYDROL.2023.130590

Graham, D.J., Beusen, A.H.W., Bierkens, M.F.P., van Vliet, M.T.H., 2026. Effects of droughts and warm months on phosphorus and nitrogen concentrations in surface waters globally. J Hydrol (Amst) 681, 136635. https://doi.org/10.1016/J.JHYDROL.2026.136635
