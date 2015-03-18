from math import log10,floor,ceil
from shutil import copy
from subprocess import call,Popen
import gzip
from utils import compare,hadd,doeff,make_plot
from ROOT import TFile,gROOT
gROOT.SetBatch()
#process name
process_name='testscan3'
print 'process name',process_name
#list of zprime mass points
zprime_mass_points=[1500.0,2000.0,2500.0]
print 'list of zprime mass points',zprime_mass_points
#list of tprime mass points
#tprime mass fractions
tprime_mass_fractions=[0.50,0.65,0.80]#[1.0/2.0,2.0/3.0,3.0/4.0]
#calculate mass points
tprime_mass_points=[]
raw_tprime_mass_points=[]
mtop=173.34
for i in range(len(zprime_mass_points)):
  	tmp_mass_list=[]
  	raw_tmp_mass_list=[]
  	for j in range(len(tprime_mass_fractions)):
		raw_value=(zprime_mass_points[i]-mtop)*tprime_mass_fractions[j]
		rounding_factor=100#pow(10.0,floor(log10(raw_value))-1)
		tmp_mass_list.append(round(raw_value/rounding_factor)*rounding_factor)
		raw_tmp_mass_list.append(raw_value)
	tprime_mass_points.append(tmp_mass_list)
	raw_tprime_mass_points.append(raw_tmp_mass_list)
print 'list of tprime mass points',tprime_mass_points
print 'list of raw tprime mass points',raw_tprime_mass_points
#list of zprime widths
zprime_width_fractions=[0.01,0.1]
zprime_widths=[]
for i in range(len(zprime_mass_points)):
	tmp_width_list=[]
	for j in range(len(zprime_width_fractions)):
		tmp_width_list.append(zprime_mass_points[i]*zprime_width_fractions[j])
	zprime_widths.append(tmp_width_list)
print 'list of zprime widths',zprime_widths
#number of events for each point
nevts=10000
print 'number of events for each point', nevts
nsamples=len(zprime_mass_points)*len(tprime_mass_points[0])*len(zprime_widths[0])
print 'number of samples',nsamples
total_nevts=nsamples*nevts
print 'total number of events',total_nevts
prototype_card_folder='/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/carte/'
# destination_card_folder='/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/syscal/sys_Cal/CMSSW_7_4_0_pre5/src/ZpToVLQGen/carte2/'
destination_folder='/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/test/Zp_Tt/'
destination_card_folder=destination_folder+'Cards/'
prototype_prefix='zpvlq_'
run_card_name='run_card.dat'
param_card_name='param_card.dat'
u='_'
# proc_card_name='zpvlq_proc_card.dat'

def main():
	#copy(prototype_card_folder+run_card_name,destination_card_folder+run_card_name)
	#moving the run card (only once!)
	print 'moving the run card'
	run_prototype_file=open(prototype_card_folder+prototype_prefix+run_card_name,'r')
	run_destination_file=open(destination_card_folder+run_card_name,'w')
	for line in run_prototype_file.readlines():
		if 'nevents' in line:
			run_destination_file.write('  '+str(nevts)+' = nevents ! Number of unweighted events requested \n')
		else:
			run_destination_file.write(line)
	run_prototype_file.close()
	run_destination_file.close()
	#entering scan loop
	print 'entering scan loop'
	for zprime_mass in zprime_mass_points:
		zprime_index=zprime_mass_points.index(zprime_mass)
		for tprime_mass in tprime_mass_points[zprime_index]:
			for zprime_width in zprime_widths[zprime_index]:
				print 'working on m_zp=',zprime_mass,'m_tp=',tprime_mass,'w_zp=',zprime_width, 'w_tp', tprime_mass/100.0
				#moving the param card
				print 'moving the param card'
				param_prototype_file=open(prototype_card_folder+prototype_prefix+param_card_name,'r')
				param_destination_file=open(destination_card_folder+param_card_name,'w')
				for line in param_prototype_file.readlines():
					if 'DECAY 9900113' in line:
						param_destination_file.write('DECAY 9900113 '+format(zprime_width,'e')+' # wrho0 \n')
					elif 'DECAY 8000001' in line:
						param_destination_file.write('DECAY 8000001 '+format(tprime_mass/100.0,'e')+' # WT23 \n')
					elif '9900113' in line and 'mrho0' in line:
						param_destination_file.write('  9900113 '+format(zprime_mass,'e')+' # mrho0 \n')
					elif '8000001' in line and 'MT23' in line:
						param_destination_file.write('  8000001 '+format(tprime_mass,'e')+' # MT23 \n')
					else:
						param_destination_file.write(line)
				param_prototype_file.close()
				param_destination_file.close()
				#running
				print 'run madgraph for this configuration'
				call(['/afs/desy.de/user/u/usaiem/xxl-af-cms/gen2/test/Zp_Tt/bin/generate_events',process_name+u+str(int(zprime_mass))+u+str(int(tprime_mass))+u+str(int(zprime_width)),'-f'])


def unzip():
	print 'unzipping unweighted events'
	for zprime_mass in zprime_mass_points:
		zprime_index=zprime_mass_points.index(zprime_mass)
		for tprime_mass in tprime_mass_points[zprime_index]:
			for zprime_width in zprime_widths[zprime_index]:
				print 'working on m_zp=',zprime_mass,'m_tp=',tprime_mass,'w_zp=',zprime_width	
				tmpunzipped=gzip.open(destination_folder+'Events/'+process_name+u+str(int(zprime_mass))+u+str(int(tprime_mass))+u+str(int(zprime_width))+'/unweighted_events.lhe.gz','r')
				tmpread=tmpunzipped.read()
				tmpout=open(destination_folder+'Events/'+process_name+u+str(int(zprime_mass))+u+str(int(tprime_mass))+u+str(int(zprime_width))+'/unweighted_events.lhe','w')
				tmpout.write(tmpread)
				tmpunzipped.close()
				tmpout.close()

def analyze():
	print 'running the analysis'
	for zprime_mass in zprime_mass_points:
		zprime_index=zprime_mass_points.index(zprime_mass)
		for tprime_mass in tprime_mass_points[zprime_index]:
			for zprime_width in zprime_widths[zprime_index]:
				print 'working on m_zp=',zprime_mass,'m_tp=',tprime_mass,'w_zp=',zprime_width	
				Popen(['cmsRun','ZpToVLQGenAnalyzer/python/testReader2_cfg.py',process_name+u+str(int(zprime_mass))+u+str(int(tprime_mass))+u+str(int(zprime_width))])

def plot():
	compare(
		name='comp1500topPt',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_900_15.root'),TFile(process_name+'_1500_1100_15.root')],
		name_list=['lhedump/topPt']*3,
		legend_list=['m_zp=1500 m_tp=700GeV','m_zp=1500 m_tp=900GeV','m_zp=1500 m_tp=1100GeV'],
		normalize=False,drawoption='hE',xtitle='top pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2000topPt',
		file_list=[TFile(process_name+'_2000_900_20.root'),TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1500_20.root')],
		name_list=['lhedump/topPt']*3,
		legend_list=['m_zp=2000 m_tp=900GeV','m_zp=2000 m_tp=1200GeV','m_zp=2000 m_tp=1500GeV'],
		normalize=False,drawoption='hE',xtitle='top pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2500topPt',
		file_list=[TFile(process_name+'_2500_1200_25.root'),TFile(process_name+'_2500_1500_25.root'),TFile(process_name+'_2500_1900_25.root')],
		name_list=['lhedump/topPt']*3,
		legend_list=['m_zp=2500 m_tp=1200GeV','m_zp=2500 m_tp=1500GeV','m_zp=2500 m_tp=1900GeV'],
		normalize=False,drawoption='hE',xtitle='top pt',ytitle='',minx=0,maxx=2000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)

	compare(
		name='comp1500wtpPt',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_900_15.root'),TFile(process_name+'_1500_1100_15.root')],
		name_list=['lhedump/wtpPt']*3,
		legend_list=['m_zp=1500 m_tp=700GeV','m_zp=1500 m_tp=900GeV','m_zp=1500 m_tp=1100GeV'],
		normalize=False,drawoption='hE',xtitle='w from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2000wtpPt',
		file_list=[TFile(process_name+'_2000_900_20.root'),TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1500_20.root')],
		name_list=['lhedump/wtpPt']*3,
		legend_list=['m_zp=2000 m_tp=900GeV','m_zp=2000 m_tp=1200GeV','m_zp=2000 m_tp=1500GeV'],
		normalize=False,drawoption='hE',xtitle='w from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2500wtpPt',
		file_list=[TFile(process_name+'_2500_1200_25.root'),TFile(process_name+'_2500_1500_25.root'),TFile(process_name+'_2500_1900_25.root')],
		name_list=['lhedump/wtpPt']*3,
		legend_list=['m_zp=2500 m_tp=1200GeV','m_zp=2500 m_tp=1500GeV','m_zp=2500 m_tp=1900GeV'],
		normalize=False,drawoption='hE',xtitle='w from tprime pt',ytitle='',minx=0,maxx=2000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)

	compare(
		name='comp1500btpPt',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_900_15.root'),TFile(process_name+'_1500_1100_15.root')],
		name_list=['lhedump/btpPt']*3,
		legend_list=['m_zp=1500 m_tp=700GeV','m_zp=1500 m_tp=900GeV','m_zp=1500 m_tp=1100GeV'],
		normalize=False,drawoption='hE',xtitle='b from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2000btpPt',
		file_list=[TFile(process_name+'_2000_900_20.root'),TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1500_20.root')],
		name_list=['lhedump/btpPt']*3,
		legend_list=['m_zp=2000 m_tp=900GeV','m_zp=2000 m_tp=1200GeV','m_zp=2000 m_tp=1500GeV'],
		normalize=False,drawoption='hE',xtitle='b from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2500btpPt',
		file_list=[TFile(process_name+'_2500_1200_25.root'),TFile(process_name+'_2500_1500_25.root'),TFile(process_name+'_2500_1900_25.root')],
		name_list=['lhedump/btpPt']*3,
		legend_list=['m_zp=2500 m_tp=1200GeV','m_zp=2500 m_tp=1500GeV','m_zp=2500 m_tp=1900GeV'],
		normalize=False,drawoption='hE',xtitle='b from tprime pt',ytitle='',minx=0,maxx=2000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)

	compare(
		name='comp1500tprimeM',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_900_15.root'),TFile(process_name+'_1500_1100_15.root')],
		name_list=['lhedump/tprimeM']*3,
		legend_list=['m_zp=1500 m_tp=700GeV','m_zp=1500 m_tp=900GeV','m_zp=1500 m_tp=1100GeV'],
		normalize=False,drawoption='hE',xtitle='tprime m',ytitle='',minx=0,maxx=2000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2000tprimeM',
		file_list=[TFile(process_name+'_2000_900_20.root'),TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1500_20.root')],
		name_list=['lhedump/tprimeM']*3,
		legend_list=['m_zp=2000 m_tp=900GeV','m_zp=2000 m_tp=1200GeV','m_zp=2000 m_tp=1500GeV'],
		normalize=False,drawoption='hE',xtitle='tprime m',ytitle='',minx=0,maxx=2000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='comp2500tprimeM',
		file_list=[TFile(process_name+'_2500_1200_25.root'),TFile(process_name+'_2500_1500_25.root'),TFile(process_name+'_2500_1900_25.root')],
		name_list=['lhedump/tprimeM']*3,
		legend_list=['m_zp=2500 m_tp=1200GeV','m_zp=2500 m_tp=1500GeV','m_zp=2500 m_tp=1900GeV'],
		normalize=False,drawoption='hE',xtitle='tprime m',ytitle='',minx=0,maxx=3000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)


	compare(
		name='compW1500topPt',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_700_150.root')],
		name_list=['lhedump/topPt']*2,
		legend_list=['w_zp=15GeV','w_zp=150GeV'],
		normalize=False,drawoption='hE',xtitle='top pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='compW1500wtpPt',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_700_150.root')],
		name_list=['lhedump/wtpPt']*2,
		legend_list=['w_zp=15GeV','w_zp=150GeV'],
		normalize=False,drawoption='hE',xtitle='w from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='compW1500btpPt',
		file_list=[TFile(process_name+'_1500_700_15.root'),TFile(process_name+'_1500_700_150.root')],
		name_list=['lhedump/btpPt']*2,
		legend_list=['w_zp=15GeV','w_zp=150GeV'],
		normalize=False,drawoption='hE',xtitle='b from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)


	compare(
		name='compW2000topPt',
		file_list=[TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1200_200.root')],
		name_list=['lhedump/topPt']*2,
		legend_list=['w_zp=20GeV','w_zp=200GeV'],
		normalize=False,drawoption='hE',xtitle='top pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='compW2000wtpPt',
		file_list=[TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1200_200.root')],
		name_list=['lhedump/wtpPt']*2,
		legend_list=['w_zp=20GeV','w_zp=200GeV'],
		normalize=False,drawoption='hE',xtitle='w from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='compW2000btpPt',
		file_list=[TFile(process_name+'_2000_1200_20.root'),TFile(process_name+'_2000_1200_200.root')],
		name_list=['lhedump/btpPt']*2,
		legend_list=['w_zp=20GeV','w_zp=200GeV'],
		normalize=False,drawoption='hE',xtitle='b from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)


	compare(
		name='compW2500topPt',
		file_list=[TFile(process_name+'_2500_1900_25.root'),TFile(process_name+'_2500_1900_250.root')],
		name_list=['lhedump/topPt']*2,
		legend_list=['w_zp=25GeV','w_zp=250GeV'],
		normalize=False,drawoption='hE',xtitle='top pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='compW2500wtpPt',
		file_list=[TFile(process_name+'_2500_1900_25.root'),TFile(process_name+'_2500_1900_250.root')],
		name_list=['lhedump/wtpPt']*2,
		legend_list=['w_zp=25GeV','w_zp=250GeV'],
		normalize=False,drawoption='hE',xtitle='w from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	compare(
		name='compW2500btpPt',
		file_list=[TFile(process_name+'_2500_1900_25.root'),TFile(process_name+'_2500_1900_250.root')],
		name_list=['lhedump/btpPt']*2,
		legend_list=['w_zp=25GeV','w_zp=250GeV'],
		normalize=False,drawoption='hE',xtitle='b from tprime pt',ytitle='',minx=0,maxx=1000,rebin=2,miny=0,maxy=0,textsizefactor=0.7
		)
	


if __name__ == '__main__':
	#main()
	#unzip()
	#analyze()
	plot()
