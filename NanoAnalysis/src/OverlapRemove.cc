#include "OverlapRemove.h"
//double dR(double eta1, double phi1, double eta2, double phi2);

//double secondMinDr(int myInd, const MyAnalysis* tree)
std::vector<double> OverlapRemove::minGenDr(int myInd, std::vector<int> ignorePID){
    double myEta = GenPart_eta[myInd]; 
    double myPhi = GenPart_phi[myInd];
    int myPID = GenPart_pdgId[myInd];
    
    double mindr = 999.0;
    double dr;
    int bestInd = -1;
    for( int oind = 0; oind < nGenPart; oind++){
        if(oind == myInd) continue;
        if(GenPart_status[oind] != 1) continue; // check if it's final state
        if(GenPart_pt[oind] < 5)  continue;
        if(abs(GenPart_pt[oind] - GenPart_pt[myInd]) < 0.01 && (GenPart_pdgId[oind] == GenPart_pdgId[myInd]) && abs(GenPart_eta[oind] - GenPart_eta[myInd]) < 0.01)  continue; // skip if same particle
        int opid = abs(GenPart_pdgId[oind]);
        if(opid == 12 || opid == 14 || opid == 16) continue; // skip neutrinos
	if(std::find(ignorePID.begin(),ignorePID.end(),opid) != ignorePID.end()) continue; //skip any pid in ignorePID vector
        dr = dR(myEta, myPhi, GenPart_eta[oind], GenPart_phi[oind]);
        if( mindr > dr ) {
	    //check if the second particle is a decay product of the first
	    int genParentIdx = GenPart_genPartIdxMother[oind];
	    bool isDecay = false;
	    while (genParentIdx>=myInd){
		if (genParentIdx==myInd) isDecay = true;
		genParentIdx = GenPart_genPartIdxMother[genParentIdx];
	    }
	    if (isDecay) continue;

            mindr = dr;
            bestInd = oind;
        }
    }
    vector<double> v;
    v.push_back(mindr);
    v.push_back((double)bestInd);
    return v;
}

bool OverlapRemove::overlapRemoval(double Et_cut, double Eta_cut, double dR_cut, bool verbose){
    bool haveOverlap = false;
    vector<int> extraPIDIgnore={22};
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
        if(GenPart_pdgId[mcInd]==22){
	    
	    bool parentagePass=false;
	    vector<double> minDR_Result = {-1.,0.};
	    bool Overlaps = false;
	    int maxPDGID = 0;
	    if (GenPart_pt[mcInd] >= Et_cut &&
		fabs(GenPart_eta[mcInd]) <= Eta_cut){
	    
		Int_t parentIdx = mcInd;
		int motherPDGID = 0;
		bool fromTopDecay = false;
		while (parentIdx != -1){
		    motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
		    maxPDGID = std::max(maxPDGID,motherPDGID);
		    parentIdx = GenPart_genPartIdxMother[parentIdx];
		}

		bool parentagePass = maxPDGID < 37;
		if (parentagePass) {
		    minDR_Result= minGenDr(mcInd, extraPIDIgnore);
		    if(minDR_Result.at(0) > dR_cut) {
			haveOverlap = true;
			Overlaps = true;
		    }
		}
	    }
	    if (verbose){
		cout << " gen particle idx="<<mcInd << " pdgID="<<GenPart_pdgId[mcInd] << " status="<<GenPart_status[mcInd] << " pt="<<GenPart_pt[mcInd] << " eta=" << GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
	    }
	}
    }
    return haveOverlap;
}

bool OverlapRemove::overlapRemoval_2To3(double Et_cut, double Eta_cut, double dR_cut, bool verbose){
    bool haveOverlap = false;
    vector<int> extraPIDIgnore={22};
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
	if(GenPart_pdgId[mcInd]==22) {
	    // TGJets doesn't include photons from top decay, so if gmom is top continue (don't remove)
	    
	    Int_t parentIdx = GenPart_genPartIdxMother[mcInd];
	    bool fromTopDecay = false;
	    vector<double> minDR_Result = {-1.,0.};
	    bool Overlaps = false;
	    int maxPDGID = 0;
	    if (GenPart_pt[mcInd] >= Et_cut &&
		fabs(GenPart_eta[mcInd]) <= Eta_cut) {
	    

		if (parentIdx>-1) {	    
		    int motherPDGID = GenPart_pdgId[parentIdx];
		    maxPDGID = abs(motherPDGID);
		    while (parentIdx != -1){
			motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
			maxPDGID = std::max(maxPDGID,motherPDGID);
			parentIdx = GenPart_genPartIdxMother[parentIdx];
			//if photon is coming from a 
			if ( abs(motherPDGID)==6 ){
			    fromTopDecay = true;
			}
		    }
		}
		bool parentagePass = maxPDGID < 37;
		if(parentagePass && !fromTopDecay) {

		    minDR_Result= minGenDr(mcInd, extraPIDIgnore);
		    if(minDR_Result.at(0) > dR_cut) {
			haveOverlap = true;
			Overlaps = true;
		    }
		}
	    }
	    if (verbose){
		cout << " gen particle idx="<<mcInd << " pdgID="<<GenPart_pdgId[mcInd] << " status="<<GenPart_status[mcInd] << " pt="<<GenPart_pt[mcInd] << " eta=" << GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
	    }
	}
    }
    return haveOverlap;
}



bool OverlapRemove::overlapRemovalTT( bool verbose){
    const double Et_cut = 10;
    const double Eta_cut = 5.0;
    bool haveOverlap = false;
    vector<int> extraPIDIgnore={22};
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
        if(GenPart_pdgId[mcInd]==22){
	    
	    bool parentagePass=false;
	    vector<double> minDR_Result = {-1.,0.};
	    bool Overlaps = false;
	    int maxPDGID = 0;
	    if (GenPart_pt[mcInd] >= Et_cut &&
		fabs(GenPart_eta[mcInd]) <= Eta_cut){
	    
		Int_t parentIdx = mcInd;
		int motherPDGID = 0;
		while (parentIdx != -1){
		    motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
		    maxPDGID = std::max(maxPDGID,motherPDGID);
		    parentIdx = GenPart_genPartIdxMother[parentIdx];
		}

		bool parentagePass = maxPDGID < 37;
		if (parentagePass) {
		    minDR_Result= minGenDr(mcInd, extraPIDIgnore);

		    if(minDR_Result.at(0) > 0.1) {
			haveOverlap = true;
			Overlaps = true;
		    }
		}
	    }
	    if (verbose){
		cout << " gen particle idx="<<mcInd << " pdgID="<<GenPart_pdgId[mcInd] << " status="<<GenPart_status[mcInd] << " pt="<<GenPart_pt[mcInd] << " eta=" << GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
	    }
	}
    }
    return haveOverlap;
}



bool OverlapRemove::overlapRemovalWJets(bool verbose){
    const double Et_cut = 15;
    const double Eta_cut = 2.6;
    bool haveOverlap = false;
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
	bool Overlaps = false;
	vector<double> minDR_Result = {-1.,0.};
	int maxPDGID = 0;
        if(GenPart_pdgId[mcInd]==22 &&
           GenPart_pt[mcInd] >= Et_cut &&
           fabs(GenPart_eta[mcInd]) <= Eta_cut) {

	    Int_t parentIdx = mcInd;
	    int maxPDGID = 0;
	    int motherPDGID = 0;
	    while (parentIdx != -1){
		motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
		maxPDGID = std::max(maxPDGID,motherPDGID);
		parentIdx = GenPart_genPartIdxMother[parentIdx];
	    }

	    bool parentagePass = maxPDGID < 37;
	    
	    if (parentagePass) {
		minDR_Result= minGenDr(mcInd);
		if(minDR_Result.at(0) > 0.05) {
		    haveOverlap = true;
		    Overlaps = true;
		}
	    }
        }
	if (verbose){
	    cout << " gen particle idx="<<mcInd << " pdgID="<<GenPart_pdgId[mcInd] << " status="<<GenPart_status[mcInd] << " pt="<<GenPart_pt[mcInd] << " eta=" << GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
	}
    }
    return haveOverlap;
}


bool OverlapRemove::overlapRemovalZJets(bool verbose){
    const double Et_cut = 15;
    const double Eta_cut = 2.6;
    bool haveOverlap = false;
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
	bool Overlaps = false;
	int maxPDGID = 0;
	vector<double> minDR_Result = {-1.,0.};
        if(GenPart_pdgId[mcInd]==22 &&
           GenPart_pt[mcInd] >= Et_cut &&
           fabs(GenPart_eta[mcInd]) <= Eta_cut) {

	    Int_t parentIdx = mcInd;
	    int maxPDGID = 0;
	    int motherPDGID = 0;
	    while (parentIdx != -1){
		motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
		maxPDGID = std::max(maxPDGID,motherPDGID);
		parentIdx = GenPart_genPartIdxMother[parentIdx];
	    }

	    bool parentagePass = maxPDGID < 37;
	    
	    if (parentagePass) {
		minDR_Result= minGenDr(mcInd);
		if(minDR_Result.at(0) > 0.05) {
		    haveOverlap = true;
		    Overlaps = true;
		}
	    }
        }
	if (verbose){
	    cout << " gen particle idx="<<mcInd << " pdgID="<<GenPart_pdgId[mcInd] << " status="<<GenPart_status[mcInd] << " pt="<<GenPart_pt[mcInd] << " eta=" << GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
	}
    }
    return haveOverlap;
}

// bool overlapRemovalZJets(MyAnalysis* tree){
//     const double Et_cut = 15;
//     const double Eta_cut = 2.6;
//     bool haveOverlap = false;
//     for(int mcInd=0; mcInd<nGenPart_; ++mcInd){
//         if(GenPart_pdgId_[mcInd]==22 &&
//            GenPart_pt_[mcInd] > Et_cut &&
//            fabs(GenPart_eta_[mcInd]) < Eta_cut) {

// 	    Int_t parentIdx = mcInd;
// 	    int maxPDGID = 0;
// 	    int motherPDGID = 0;
// 	    while (parentIdx != -1){
// 		motherPDGID = std::abs(GenPart_pdgId_[parentIdx]);
// 		maxPDGID = std::max(maxPDGID,motherPDGID);
// 		parentIdx = GenPart_genPartIdxMother_[parentIdx];
// 	    }

// 	    bool parentagePass = maxPDGID < 37;
	    
// 	    if (parentagePass) {
// 		if(minGenDr(mcInd, tree).at(0) > 0.05) {
// 		    haveOverlap = true;
// 		}
// 	    }
//         }
//     }
//     return haveOverlap;
// }


bool OverlapRemove::overlapRemoval_Tchannel(){
    const double Et_cut = 10;
    const double Eta_cut = 2.6;
    bool haveOverlap = false;
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
	if(GenPart_pdgId[mcInd]==22 &&
	   GenPart_pt[mcInd] >= Et_cut &&
	   fabs(GenPart_eta[mcInd]) <= Eta_cut) {
	    
	    // TGJets doesn't include photons from top decay, so if gmom is top continue (don't remove)
	    
	    Int_t parentIdx = GenPart_genPartIdxMother[mcInd];
	    bool fromTopDecay = false;
	    int maxPDGID = 0;

	    if (parentIdx>-1) {	    
		int motherPDGID = GenPart_pdgId[parentIdx];
		maxPDGID = abs(motherPDGID);
		while (parentIdx != -1){
		    motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
		    maxPDGID = std::max(maxPDGID,motherPDGID);
		    parentIdx = GenPart_genPartIdxMother[parentIdx];
		    //if photon is coming from a 
		    if ( abs(motherPDGID)==6 ){
			fromTopDecay = true;
		    }
		}
	    }
	    bool parentagePass = maxPDGID < 37;
	    if(parentagePass && !fromTopDecay && minGenDr(mcInd).at(0) > 0.05) {
		haveOverlap = true;
	    }
	}
    }
    return haveOverlap;
}
