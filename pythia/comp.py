from utils import compare
from ROOT import TFile,gROOT

gROOT.SetBatch()

compare(
name='LH_MGPvsPYTHIA',
file_list=[TFile('outLmu.root'),TFile('outL2.root')],
legend_list=["LH MG+PYTHIA", "LH PYTHIA"],
name_list=['muPt']*2,
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='RH_MGPvsPYTHIA',
file_list=[TFile('outRmu.root'),TFile('outR2.root')],
legend_list=["RH MG+PYTHIA", "RH PYTHIA"],
name_list=['muPt']*2,
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='PYTHIA_LHvsRH',
file_list=[TFile('outL2.root'),TFile('outR2.root')],
legend_list=["LH PYTHIA", "RH PYTHIA"],
name_list=['muPt']*2,
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='MGP_LHvsRH',
file_list=[TFile('outLmu.root'),TFile('outRmu.root')],
legend_list=["LH MG+PYTHIA", "RH MG+PYTHIA"],
name_list=['muPt']*2,
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='MG_LHvsRH',
file_list=[TFile('Ht_lept_L.root'),TFile('Ht_lept_R.root')],
legend_list=["LH MG", "RH MG"],
name_list=['lhedump/muPt']*2,
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='LH_MGvsMGP',
file_list=[TFile('Ht_lept_L.root'),TFile('outLmu.root')],
legend_list=["LH MG+PYTHIA", "LH MG"],
name_list=['lhedump/muPt','muPt'],
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='RH_MGvsMGP',
file_list=[TFile('Ht_lept_R.root'),TFile('outRmu.root')],
legend_list=["RH MG+PYTHIA", "RH MG"],
name_list=['lhedump/muPt','muPt'],
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='LH_MGvsMGPvsPYTHIA',
file_list=[TFile('Ht_lept_L.root'),TFile('outLmu.root'),TFile('outL2.root')],
legend_list=["LH MG+PYTHIA", "LH MG","LH PYTHIA"],
name_list=['lhedump/muPt','muPt','muPt'],
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='RH_MGvsMGPvsPYTHIA',
file_list=[TFile('Ht_lept_R.root'),TFile('outRmu.root'),TFile('outR2.root')],
legend_list=["RH MG+PYTHIA", "RH MG","RH PYTHIA"],
name_list=['lhedump/muPt','muPt','muPt'],
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)

compare(
name='all',
file_list=[TFile('Ht_lept_L.root'),TFile('outLmu.root'),TFile('outL2.root'),TFile('Ht_lept_R.root'),TFile('outRmu.root'),TFile('outR2.root')],
legend_list=["LH MG+PYTHIA", "LH MG","LH PYTHIA","RH MG+PYTHIA", "RH MG","RH PYTHIA"],
name_list=['lhedump/muPt','muPt','muPt','lhedump/muPt','muPt','muPt'],
normalize=True,drawoption='h',xtitle="p_{T} of #mu from T'",ytitle='',minx=0,maxx=1000,rebin=4,miny=0,maxy=0,textsizefactor=0.7
)