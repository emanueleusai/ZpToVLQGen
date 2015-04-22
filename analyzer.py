import ROOT
from DataFormats.FWLite import Events, Handle
from utils import compare,hadd,doeff,make_plot
from ROOT import TFile
import sys

# events = Events ('/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/gen.root')
def analyze_gen():
	events = Events ('/nfs/dust/cms/user/usaiem/gen/genall.root')
	handle  = Handle ('LHEEventProduct')
	label = ("source")
	ROOT.gROOT.SetBatch()
	ROOT.gROOT.SetStyle('Plain') # white background
	zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)
	zevts=0
	wevts=0
	hevts=0
	for event in events:
		event.getByLabel (label, handle)
		lhe = handle.product()
		hepeup=lhe.hepeup()
		pup= hepeup.PUP
		idup= hepeup.IDUP
		mothup= hepeup.MOTHUP
		for i in idup:
			if abs(i)==23:
				zevts+=1
				break
			elif abs(i)==24:
				wevts+=1
				break
			elif abs(i)==25:
				hevts+=1
				break
	print 'zevts',zevts
	print 'wevts',wevts
	print 'hevts',hevts

def findau(mother,motherid,daughterid):
	for i in range(mother.numberOfDaughters()):
		if abs(mother.pdgId())==motherid and abs(mother.daughter(i).pdgId()) in daughterid:
			return mother.daughter(i)
		elif abs(mother.pdgId())==motherid and abs(mother.daughter(i).pdgId())==motherid:
			return findau(mother.daughter(i),motherid,daughterid)
		else:
			return 0


def analyze_sim():
	filenames=[]
	print sys.argv
	postfix=''
	if sys.argv[1]=='2':
		postfix='2'
	therange=range(50)
	if sys.argv[2]=='right':
		therange=range(50,100)
	for i in therange:
		filenames.append('/nfs/dust/cms/user/usaiem/gc-output/ZpToVLQ/ZpSIMLR'+postfix+'/'+sys.argv[2]+'_'+str(i)+'_simhtlr.root')
	#events = Events (['/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/simht2.root'])
	events = Events (filenames)
	handle  = Handle ('vector<reco::GenParticle>')
	label = ("genParticles")
	ROOT.gROOT.SetBatch()
	ROOT.gROOT.SetStyle('Plain') # white background
	print 'Ht_'+postfix+'_'+sys.argv[2]+'_hist.root'
	outfile=TFile('Ht_'+postfix+'_'+sys.argv[2]+'_hist.root','RECREATE')
	Hist = ROOT.TH1F ("mupt", ";#mu p_{T}", 100, 0, 1000)
	num=0
	for event in events:
		num=num+1
		if num%100==0:
			print 'event',num
		event.getByLabel (label, handle)
		genparticles = handle.product()
		for genparticle in genparticles:
			# if abs(genparticle.pdgId()) in [25]:
			# 	print 'ecco un higgs'
			# 	for i in range(genparticle.numberOfDaughters()):
			# 		print genparticle.daughter(i).pdgId()
			if abs(genparticle.pdgId()) in [8000001]:
				the_top=findau(genparticle,8000001,[6])
				if the_top!=0:
					the_w=findau(the_top,6,[24])
					if the_w!=0:
						the_lepton=findau(the_w,24,[13])
						if the_lepton!=0:
							Hist.Fill(the_lepton.pt())
							break
				# for i in range(genparticle.numberOfDaughters()):
				# 	if abs(genparticle.daughter(i).pdgId()) in [6]:
				# 		for j in range(genparticle.daughter(i).numberOfDaughters()):
				# 			if abs(genparticle.daughter(i).daughter(j).pdgId()) in [11,13,15]:
				# 				print genparticle.daughter(i).daughter(j).pt()
	outfile.cd()
	Hist.Write()
	#Hist.SaveAs('Ht_'+sys.argv[2]+'.pdf')
	outfile.Close()

def plotting():
	#additional jets
	ROOT.gROOT.SetBatch()
	compare(
name='additional_jets',
file_list=[TFile('Wb_jj_correct.root'),TFile('Wb_jj_ickkw.root'),TFile('Wb_jj_ickkw_xqcut.root'),TFile('Wb_jj_kin.root'),TFile('Wb_jj_kin_ickkw.root'),TFile('Wb_jj_kin_xqcut.root'),TFile('Wb_jj_wrong.root'),TFile('Wb_jj_xqcut.root')],
legend_list=['ickkw+kin+xqcut','ickkw','ickkw+xqcut','kin','kin+ickkw','kin+xqcut','nothing','xqcut'],
name_list=['lhedump/topzprimePt']*8,
normalize=False,drawoption='hE',xtitle="p_{T} of top from Z'",ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
)
	#bW
	compare(
name='bW_LR',
file_list=[TFile('Wb_lept_L.root'),TFile('Wb_lept_R.root')],
legend_list=["T' left #rightarrow bW", "T' right #rightarrow bW"],
name_list=['lhedump/muPt']*2,
normalize=False,drawoption='hE',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)
	#tZ
	compare(
name='tZ_LR',
file_list=[TFile('Zt_lept_L.root'),TFile('Zt_lept_R.root')],
legend_list=["T' left #rightarrow tZ", "T' right #rightarrow tZ"],
name_list=['lhedump/muPt']*2,
normalize=False,drawoption='hE',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
)
	#tH
	compare(
name='tH_LR',
file_list=[TFile('Ht_lept_L.root'),TFile('Ht_lept_R.root')],
legend_list=["T' left #rightarrow tH", "T' right #rightarrow tH"],
name_list=['lhedump/muPt']*2,
normalize=False,drawoption='hE',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
)
	#pythia tH
	#pythia bW


if __name__ == '__main__':
	#analyze_gen()
	analyze_sim()
	#plotting()
