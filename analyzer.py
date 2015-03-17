import ROOT
from DataFormats.FWLite import Events, Handle

# events = Events ('/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/gen.root')
def analyze_gen():
	events = Events ('/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/gen2.root')
	handle  = Handle ('LHEEventProduct')
	label = ("source")
	ROOT.gROOT.SetBatch()
	ROOT.gROOT.SetStyle('Plain') # white background
	zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)
	for event in events:
		event.getByLabel (label, handle)
		lhe = handle.product()
		hepeup=lhe.hepeup()
		pup= hepeup.PUP
		idup= hepeup.IDUP
		mothup= hepeup.MOTHUP
		for i in idup:
			print i

def analyze_sim():
	events = Events ('/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/sim3.root')
	handle  = Handle ('vector<reco::GenParticle>')
	label = ("genParticles")
	ROOT.gROOT.SetBatch()
	ROOT.gROOT.SetStyle('Plain') # white background
	zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)
	for event in events:
		event.getByLabel (label, handle)
		genparticles = handle.product()
		for genparticle in genparticles:
			print genparticle.pdgId(),genparticle.pt()

if __name__ == '__main__':
	#analyze_gen()
	analyze_sim()
