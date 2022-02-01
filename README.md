This is an example of conducting cross-section model comparisons with the MicroBooNE forward-folded cross-section result (Run 3). Minor modification is expected to compare the data with your predictions. This example is tested with python 2.7.

Thomas Mettler is the primary author of this tool. Yifan Chen (cyifan@slac.stanford.edu) and Christoph Rudolf Von Rohr (rudolf@lhep.unibe.ch) are the current maintainers.

#### Step 1: Make_true_rate_hist_example.py
Translate your model into true event rate in the cross-section bins. 
1. Make sure the events pass the signal definition:
    - Muon neutrino charged-current interaction
    - The vertex within fiducial volume (The fiducial volume is defined as at least 10 cm from all sides of the active LArTPC volume and 50 cm from its end of the active LArTPC with respect to the beam direction (downstream z).)
    - The muon momentum is above 150 MeV/c
2. Fill the events in the cross-section bins
    - theta_bins = [ -1.00, -0.50, 0.00, 0.28, 0.47, 0.63, 0.765, 0.865, 0.935, 1.00 ]
    - mom_bins = [[ 0.00, 0.18, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.18, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.18, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 1.28, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 1.28, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 1.28, 2.50 ]]
3. If you have cross-section value at hand, remember to convert it to event rate by multiplying the flux (1.58051E11) and number of targets (4.10331E31).
4. #### It's important to set up an overflow bin for events with muon momentum above 2.5 GeV/c. 
5. Store the histogram in a root file.


#### Step 2: Model_comparison_example.py
Compare your model with the measured forward-folded cross section.
1. The data, systematic variations are all stored in the 'input' folder
2. Based on the model to-be-compared, calculate the covariance matrices for various uncertainties. Each covariance matrix are computed with number of predicted events in reconstructed bins. The smearing matrix and background are paired in each uncertainty universe.
3. The total covariance is the summation of all these sub covariance matrices.
4. The chi2 test between the model and the cross section is carried out using the total covariance matrix.
5. A figure of event rate will be stored in the output path.
