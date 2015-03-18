#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include <iomanip>
#include <iostream>
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "TH2.h"
#include "TH1.h"

using namespace std;
using namespace edm;
using namespace lhef;

class DummyLHEAnalyzer : public EDAnalyzer {
private: 
  bool dumpLHE_;
  bool checkPDG_;
public:
  explicit DummyLHEAnalyzer( const ParameterSet & cfg ) : 
    src_( cfg.getParameter<InputTag>( "src" ) )
  {
  }
private:
  std::map< std::string, TH1D* > histos1D_;

  int checkNof(int pdgid, const std::vector<int> idup_)
  {
    int n=0;
    for(auto id : idup_)
    {
      if (abs(id)==pdgid) n++;
    }
    return n;
  }

  bool checkDau(int mpdg, int d1pdg, int d2pdg, const std::vector<int> idup_, const std::vector< std::pair< int, int > > mothup_)
  {
    vector<int> dau;
    for(unsigned int i=0; i<idup_.size(); i++)
    {
      if ((abs(idup_[mothup_[i].first-1])==mpdg) || (abs(idup_[mothup_[i].second-1])==mpdg)) dau.push_back(idup_[i]);
    }
    if (dau.size()!=2) return false;
    if ((((abs(dau[0])==d1pdg) && (abs(dau[1])==d2pdg)) || ((abs(dau[0])==d2pdg) && (abs(dau[1])==d1pdg))) /*&& (dau[0]/abs(dau[0])*dau[1]/abs(dau[1])<0)*/ ) return true;
    return false;
  }

  void analyze( const Event & iEvent, const EventSetup & iSetup ) override {

    Handle<LHEEventProduct> evt;
    iEvent.getByLabel( src_, evt );

    int zprimepdg=9900113;
    int tprimepdg=8000001;

    const lhef::HEPEUP hepeup_ = evt->hepeup();

    const int nup_ = hepeup_.NUP; 
    const std::vector<int> idup_ = hepeup_.IDUP;
    const std::vector<lhef::HEPEUP::FiveVector> pup_ = hepeup_.PUP;
    const std::vector< std::pair< int, int > > mothup_ = hepeup_.MOTHUP;

    // std::cout << "Number of particles = " << nup_ << std::endl;

    // if ( evt->pdf() != NULL ) {
    //   std::cout << "PDF scale = " << std::setw(14) << std::fixed << evt->pdf()->scalePDF << std::endl;  
    //   std::cout << "PDF 1 : id = " << std::setw(14) << std::fixed << evt->pdf()->id.first 
    //             << " x = " << std::setw(14) << std::fixed << evt->pdf()->x.first 
    //             << " xPDF = " << std::setw(14) << std::fixed << evt->pdf()->xPDF.first << std::endl;  
    //   std::cout << "PDF 2 : id = " << std::setw(14) << std::fixed << evt->pdf()->id.second 
    //             << " x = " << std::setw(14) << std::fixed << evt->pdf()->x.second 
    //             << " xPDF = " << std::setw(14) << std::fixed << evt->pdf()->xPDF.second << std::endl;  
    // }

if(!(
    checkNof(6,idup_)==1 &&
    checkNof(zprimepdg,idup_)==1 &&
    checkNof(tprimepdg,idup_)==1 &&
    checkDau(zprimepdg,tprimepdg,6,idup_,mothup_) &&
    checkDau(tprimepdg,5,24,idup_,mothup_) &&
    (checkDau(6,5,24,idup_,mothup_) || checkDau(6,4,24,idup_,mothup_) ) )
    ){

std::cout<<"NO\n";
std::cout<<"checkNof(6,idup_)==1 " << checkNof(6,idup_) <<std::endl;
std::cout<<"checkNof(zprimepdg,idup_)==1 "<<checkNof(zprimepdg,idup_) <<std::endl;
std::cout<<"checkNof(tprimepdg,idup_)==1 "<<checkNof(tprimepdg,idup_) <<std::endl;
std::cout<<"checkDau(zprimepdg,tprimepdg,6,idup_,mothup_) "<<checkDau(zprimepdg,tprimepdg,6,idup_,mothup_) <<std::endl;
std::cout<<"checkDau(tprimepdg,5,24,idup_,mothup_) "<<checkDau(tprimepdg,5,24,idup_,mothup_) <<std::endl;
std::cout<<"checkDau(6,5,24,idup_,mothup_) "<<checkDau(6,5,24,idup_,mothup_) <<std::endl;
std::cout<<"checkDau(6,4,24,idup_,mothup_) "<<checkDau(6,4,24,idup_,mothup_) <<std::endl;
std::cout<<std::endl;
for ( unsigned int icount = 0 ; icount < (unsigned int)nup_; icount++ ) {
      std::cout << "# " << std::setw(14) << std::fixed << icount 
                << std::setw(14) << std::fixed << idup_[icount] 
                << std::setw(14) << std::fixed << (pup_[icount])[0] 
                << std::setw(14) << std::fixed << (pup_[icount])[1] 
                << std::setw(14) << std::fixed << (pup_[icount])[2] 
                << std::setw(14) << std::fixed << (pup_[icount])[3] 
                << std::setw(14) << std::fixed << (pup_[icount])[4]
                << std::setw(14) << std::fixed << mothup_[icount].first
                << std::setw(14) << std::fixed << mothup_[icount].second
                << std::endl;
              }

} 


    for ( unsigned int icount = 0 ; icount < (unsigned int)nup_; icount++ ) {

      // std::cout << "# " << std::setw(14) << std::fixed << icount 
      //           << std::setw(14) << std::fixed << idup_[icount] 
      //           << std::setw(14) << std::fixed << (pup_[icount])[0] 
      //           << std::setw(14) << std::fixed << (pup_[icount])[1] 
      //           << std::setw(14) << std::fixed << (pup_[icount])[2] 
      //           << std::setw(14) << std::fixed << (pup_[icount])[3] 
      //           << std::setw(14) << std::fixed << (pup_[icount])[4]
      //           << std::setw(14) << std::fixed << mothup_[icount].first
      //           << std::setw(14) << std::fixed << mothup_[icount].second
      //           << std::endl;

       if (abs(idup_[icount])==6) histos1D_[ "topPt" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)));
       if ((abs(idup_[mothup_[icount].first-1])==tprimepdg) && (abs(idup_[icount])==24)) histos1D_[ "wtpPt" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)));
       if ((abs(idup_[mothup_[icount].first-1])==tprimepdg) && (abs(idup_[icount])==5)) histos1D_[ "btpPt" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)));
       if (abs(idup_[icount])==tprimepdg) histos1D_[ "tprimePt" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)));

       if (abs(idup_[icount])==6) histos1D_[ "topP" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)+pow((pup_[icount])[2],2)));
       if ((abs(idup_[mothup_[icount].first-1])==tprimepdg) && (abs(idup_[icount])==24)) histos1D_[ "wtpP" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)+pow((pup_[icount])[2],2)));
       if ((abs(idup_[mothup_[icount].first-1])==tprimepdg) && (abs(idup_[icount])==5)) histos1D_[ "btpP" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)+pow((pup_[icount])[2],2)));
       if (abs(idup_[icount])==tprimepdg) histos1D_[ "tprimeP" ]->Fill(sqrt(pow((pup_[icount])[0],2)+pow((pup_[icount])[1],2)+pow((pup_[icount])[2],2)));

       if (abs(idup_[icount])==6) histos1D_[ "topM" ]->Fill((pup_[icount])[4]);
       if (abs(idup_[icount])==tprimepdg) histos1D_[ "tprimeM" ]->Fill((pup_[icount])[4]);
       if (abs(idup_[icount])==zprimepdg) histos1D_[ "zprimeM" ]->Fill((pup_[icount])[4]);
    }
    if( evt->weights().size() ) {
      //std::cout << "weights:" << std::endl;
      for ( size_t iwgt = 0; iwgt < evt->weights().size(); ++iwgt ) {
	const LHEEventProduct::WGT& wgt = evt->weights().at(iwgt);
	//std::cout << "\t" << wgt.id << ' ' 
		//  << std::scientific << wgt.wgt << std::endl;
      }
    }

  }

  
  void beginRun(edm::Run const& iRun, edm::EventSetup const& es) override {
edm::Service< TFileService > fileService;
  histos1D_[ "topPt" ] = fileService->make< TH1D >( "topPt", ";top p_{T} [GeV];Events", 200, 0., 2000);
  histos1D_[ "tprimePt" ] = fileService->make< TH1D >( "tprimePt", ";T' p_{T} [GeV];Events", 200, 0., 2000);
  histos1D_[ "wtpPt" ] = fileService->make< TH1D >( "wtpPt", ";W from T' p_{T} [GeV];Events", 200, 0., 2000);
  histos1D_[ "btpPt" ] = fileService->make< TH1D >( "btpPt", ";b from T' p_{T} [GeV];Events", 200, 0., 2000);

  histos1D_[ "topP" ] = fileService->make< TH1D >( "topP", ";top p [GeV];Events", 200, 0., 2000);
  histos1D_[ "tprimeP" ] = fileService->make< TH1D >( "tprimeP", ";T' p [GeV];Events", 200, 0., 2000);
  histos1D_[ "wtpP" ] = fileService->make< TH1D >( "wtpP", ";W from T' p [GeV];Events", 200, 0., 2000);
  histos1D_[ "btpP" ] = fileService->make< TH1D >( "btpP", ";b from T' p [GeV];Events", 200, 0., 2000);

  histos1D_[ "topM" ] = fileService->make< TH1D >( "topM", ";top mass [GeV];Events", 100, 100, 200);
  histos1D_[ "tprimeM" ] = fileService->make< TH1D >( "tprimeM", ";T' mass [GeV];Events", 200, 0, 2000);
  histos1D_[ "zprimeM" ] = fileService->make< TH1D >( "zprimeM", ";Z' mass [GeV];Events", 300, 0, 3000);

    // Handle<LHERunInfoProduct> run;
    // iRun.getByLabel( src_, run );
    
    // const lhef::HEPRUP thisHeprup_ = run->heprup();

    // std::cout << "HEPRUP \n" << std::endl;
    // std::cout << "IDBMUP " << std::setw(14) << std::fixed << thisHeprup_.IDBMUP.first 
    //           << std::setw(14) << std::fixed << thisHeprup_.IDBMUP.second << std::endl; 
    // std::cout << "EBMUP  " << std::setw(14) << std::fixed << thisHeprup_.EBMUP.first 
    //           << std::setw(14) << std::fixed << thisHeprup_.EBMUP.second << std::endl; 
    // std::cout << "PDFGUP " << std::setw(14) << std::fixed << thisHeprup_.PDFGUP.first 
    //           << std::setw(14) << std::fixed << thisHeprup_.PDFGUP.second << std::endl; 
    // std::cout << "PDFSUP " << std::setw(14) << std::fixed << thisHeprup_.PDFSUP.first 
    //           << std::setw(14) << std::fixed << thisHeprup_.PDFSUP.second << std::endl; 
    // std::cout << "IDWTUP " << std::setw(14) << std::fixed << thisHeprup_.IDWTUP << std::endl; 
    // std::cout << "NPRUP  " << std::setw(14) << std::fixed << thisHeprup_.NPRUP << std::endl; 
    // std::cout << "        XSECUP " << std::setw(14) << std::fixed 
    //           << "        XERRUP " << std::setw(14) << std::fixed 
    //           << "        XMAXUP " << std::setw(14) << std::fixed 
    //           << "        LPRUP  " << std::setw(14) << std::fixed << std::endl;
    // for ( unsigned int iSize = 0 ; iSize < thisHeprup_.XSECUP.size() ; iSize++ ) {
    //   std::cout  << std::setw(14) << std::fixed << thisHeprup_.XSECUP[iSize]
    //              << std::setw(14) << std::fixed << thisHeprup_.XERRUP[iSize]
    //              << std::setw(14) << std::fixed << thisHeprup_.XMAXUP[iSize]
    //              << std::setw(14) << std::fixed << thisHeprup_.LPRUP[iSize] 
    //              << std::endl;
    // }
    // std::cout << " " << std::endl;

  }
  

  InputTag src_;
};

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE( DummyLHEAnalyzer );


