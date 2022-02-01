from ROOT import *
import math

## No need to see the plots appear here
#gROOT.SetBatch(1)
gStyle.SetLineWidth(1)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(0)
TGaxis.SetMaxDigits(3)

gStyle.SetTextSize(0.06)
gStyle.SetLabelSize(0.05,"xyzt")
gStyle.SetTitleSize(0.06,"xyzt")

gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
# gStyle.SetNdivisions(505, "XY")

gROOT .ForceStyle()

TH1.SetDefaultSumw2()

TGaxis.SetMaxDigits(5)
        
def make_GiBUU_example(filename):

    inFile = [None]*len(filename)
    inTree = [None]*len(filename)

    bin_size = [None] * Nbin_true

    h_poly = [None]*len(filename)

    h_rate = [None]*len(filename)

    cc2 = TCanvas("cc2","cc2",1600,400)

    # calculate bin size
    i_bin = 0
    for x in range(len(theta_bins)-1):
        for y in range(len(mom_bins[x])-1):
            bin_size[i_bin] = (theta_bins[x+1] - theta_bins[x]) * (mom_bins[x][y+1] - mom_bins[x][y])
            i_bin = i_bin + 1
    
    for i_file in range(len(filename)):
        inFile[i_file] = TFile("input/" + filename[i_file] + ".root", "READ")
        inTree[i_file] = inFile[i_file].Get("FlatTree_VARS")

        h_poly[i_file] = TH2Poly()

        # define bins
        for x in range(len(theta_bins)-1):
            for y in range(len(mom_bins[x])-1):
                h_poly[i_file].AddBin(theta_bins[x], mom_bins[x][y] , theta_bins[x+1], mom_bins[x][y+1])  
       
        h_poly[i_file].AddBin(-1,2.5,1,15)

        for i in range(inTree[i_file].GetEntries()):
            inTree[i_file].GetEntry(i)

            if inTree[i_file].cc != '\x01': 
                continue

            # define signal
            index = 0
            signal = True
            num_p = 0
            for pdg in inTree[i_file].pdg:
                # print pdg
                if pdg == 13:
                    if math.sqrt(inTree[i_file].px[index]*inTree[i_file].px[index] + inTree[i_file].py[index]*inTree[i_file].py[index] + inTree[i_file].pz[index]*inTree[i_file].pz[index]) < 0.15:
                        signal = False
                        break

            if signal:
                mu_mom = math.sqrt(inTree[i_file].ELep*inTree[i_file].ELep - 0.105658*0.105658)

                h_poly[i_file].Fill(inTree[i_file].CosLep, mu_mom, inTree[i_file].InputWeight)


        h_poly[i_file] .Scale(1e-38)
        h_rate[i_file] = TH1F("h_rate_" + str(i_file),"", Nbin_true, 0, Nbin_true)


        for i_bin in range(Nbin_true):
            h_rate[i_file].SetBinContent(i_bin+1, h_poly[i_file].GetBinContent(i_bin+1) * flux * N_target)

        
        cc2.cd()
        if i_file == 0:
            gPad .SetRightMargin(0.04)
            gPad .SetBottomMargin(0.12)
            gPad .SetLeftMargin(0.1)
            Bin = h_rate[i_file].GetMaximumBin()
            Max = h_rate[i_file].GetBinContent(Bin)
            h_rate[i_file].SetMaximum(1.4 * Max)

            h_rate[i_file].GetXaxis().SetLabelSize(0.08)
            h_rate[i_file].GetYaxis().SetLabelSize(0.08)

            h_rate[i_file].GetYaxis().SetTitle("Event rate")
            h_rate[i_file].GetYaxis().SetTitleOffset(0.7)  
        
        h_rate[i_file].SetLineWidth(2)
        h_rate[i_file].SetLineColor(line_color[i_file])
        h_rate[i_file].Draw("hist, same")

        f_out = TFile("input/FF_pred.root", "Recreate")
        h_rate[i_file].Write("h_true_rate_GiBUU")

        f_out.Close()

        
    # rate
    cc2.cd()  
    cc2.SaveAs("plots/GiBUU/CCinc_GiBUU_true_rate.pdf")

    return 

if __name__ == '__main__':

    # bin boundaries
    mom_bins = [[ 0.00, 0.18, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.18, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.18, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 1.28, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 1.28, 2.50 ], [ 0.00, 0.30, 0.45, 0.77, 1.28, 2.50 ]]
    theta_bins = [ -1.00, -0.50, 0.00, 0.28, 0.47, 0.63, 0.765, 0.865, 0.935, 1.00 ]

    Nbin_true = 1 # count the overflow bin
    for mom_i in mom_bins:
        Nbin_true = Nbin_true + len(mom_i) - 1

    flux = 1.58051e11 # from Thomas thesis

    # rho = 1.3837 #g/cm3
    # Volume = dx * dy * dz #cm3
    # NA = 6.022140857E23 #molec/mol
    # Nnucleons = 40
    # mmol = 39.95 # g/mol

    # N_target = rho * Volume * NA * Nnucleons / mmol

    N_target = 4.10331e31  # from Thomas thesis per nucleons

    filename = ["GiBUURooTracker.202104_NUISFLAT"]

    line_color = [417]


    make_GiBUU_example(filename)

