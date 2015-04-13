import ROOT
from DataFormats.FWLite import Events, Handle

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
	analyze_gen()
	#analyze_sim()
