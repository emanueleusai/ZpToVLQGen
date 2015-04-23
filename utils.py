from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,THStack,TIter,kRed,kYellow,kGray,kBlack,TLatex
from os import system
from sys import argv
from os import mkdir
from os.path import exists

def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1):
  c=TCanvas(name,'',600,600)
  # c.SetLeftMargin(0.15)#
  # c.SetRightMargin(0.05)#
  # # c.SetTopMargin(0.05)#
  # c.SetBottomMargin(0.10)
  # # if not useOutfile:
  # # legend=TLegend(0.7,0.7,0.95,0.95)
  # # else:
  # c.SetTopMargin(0.15)
  # legend=TLegend(0.0,0.85,0.99,0.99)
  # #legend=TLegend(0.35,0.2,0.85,0.5)



  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.11)
  c.SetTopMargin(0.25)
  legend=TLegend(0.0,0.76,0.99,1.04)


  legend.SetHeader('')
  #legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  histo_list=[]
  # tfile_list=[]
  the_maxy=0
  for i in range(len(name_list)):
    # tfile_list.append(TFile(file_list[i],'READ'))
    histo_list.append(file_list[i].Get(name_list[i]))
    if normalize:
      histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001), "width")
    if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
      histo_list[-1].SetStats(0)
    histo_list[-1].SetLineWidth(3)
    histo_list[-1].SetLineColor(i+1)
    histo_list[-1].SetTitle('')
    legend.AddEntry(histo_list[-1],legend_list[i],'l')
    if rebin!=1:
      histo_list[-1].Rebin(rebin)
    the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
  for i in range(len(name_list)):
    if i==0:
      if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
        if miny!=0 or maxy!=0:
          histo_list[i].SetMaximum(maxy)
          histo_list[i].SetMinimum(miny)
        else:
          histo_list[i].SetMaximum(the_maxy)
          histo_list[i].SetMinimum(0.0001)
      else:
        histo_list[i].SetMaximum(1.05)
        histo_list[i].SetMinimum(0.0001)
      histo_list[i].Draw(drawoption)
      charsize=0.05*textsizefactor
      histo_list[i].GetYaxis().SetLabelSize(charsize)
      histo_list[i].GetYaxis().SetTitleSize(charsize)
      histo_list[i].GetYaxis().SetTitleOffset(1.6)
      histo_list[i].GetXaxis().SetLabelSize(charsize)
      histo_list[i].GetXaxis().SetTitleSize(charsize)
      histo_list[i].GetXaxis().SetTitleOffset(0.95)
      # if useOutfile:
      histo_list[i].GetXaxis().SetTitle(xtitle)
      histo_list[i].GetYaxis().SetTitle(ytitle)
      if maxx!=0 or minx!=0:
        histo_list[i].GetXaxis().SetRangeUser(minx,maxx)
      #   histo_list[i].GetYaxis().SetTitle('Efficiency')
    else:
      histo_list[i].Draw(drawoption+'SAME')
  legend.Draw()
  # outfile.cd()
  # c.Write(name)
  c.SaveAs('pdf/'+name+'.pdf')
  #c.SaveAs(folder+name+'.png')

def hadd(path_base,name_base,inputlist,outputname,force=True):
  command_list='hadd -f '+path_base+outputname+'.root'#-v 0
  if not force:
    command_list='hadd '+path_base+outputname+'.root'#-v 0
  for i in inputlist:
    command_list+=' '+path_base+name_base+i+'.root'
  system(command_list)
  return path_base+outputname+'.root'

def doeff(filename, histoname_den, histoname_num, histoname_out, outfile,rebin=1):
  numerator=filename.Get(histoname_num)
  denominator=filename.Get(histoname_den)
  if not rebin==1:
    numerator.Rebin(rebin)
    denominator.Rebin(rebin)
  n_num=numerator.Integral()
  n_den=denominator.Integral()
  error_bars=TGraphAsymmErrors()
  error_bars.Divide(numerator,denominator,"cl=0.683 b(1,1) mode")
  outfile.cd()
  error_bars.Write(histoname_out)
  return n_num/n_den

def slice_and_save(sample,histo,outfile):
  outfile.cd()
  histo_stack=THStack(histo,'x','Stack_'+histo.GetName(),'')
  histo_1d=histo_stack.GetHists()
  histo_stack.Write(histo_stack.GetName()+'_'+sample)
  nextinlist=TIter(histo_1d)
  obj=nextinlist()
  while obj:
    obj.Write(obj.GetName()+'_'+sample)
    obj=nextinlist()
  histo.Write(histo.GetName()+'_'+sample)

def domistag(infile,outfile,mistag_den,mistag_num,outname):
  den_histo=infile.Get(mistag_den).Clone('Denominator')
  num_histo=infile.Get(mistag_num).Clone('Numerator')
  mistag_histo=num_histo.Clone('Mistag')
  mistag_histo.Divide(num_histo,den_histo,1,1,'B')
  slice_and_save(outname,mistag_histo,outfile)
  slice_and_save(outname,num_histo,outfile)
  slice_and_save(outname,den_histo,outfile)


def make_plot(name, ttbar_file, qcd_file, signal_files, histo, histo_qcd='',rebin=1,minx=0,maxx=0,miny=0,maxy=0,logy=False):
  c=TCanvas(name,'',600,600)
  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.1)
  c.SetTopMargin(0.25)
  latex=TLatex(0.65,0.70,'13 TeV, 20 fb^{-1} ')
  latex.SetNDC(1)
  latex.SetTextFont(42)
  legend=TLegend(0.0,0.75,0.99,1.04)
  legend.SetHeader('')
  #legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  stack=THStack(name+'_stack','')
  ttbar_histo=ttbar_file.Get(histo)
  ttbar_histo.Rebin(rebin)
  if histo_qcd=='':
    qcd_histo=qcd_file.Get(histo)
  else:
    qcd_histo=qcd_file.Get(histo_qcd)
  qcd_histo.Rebin(rebin)
  signal_histos=[]
  colors=[28,9,8]
  for i in range(len(signal_files)):
    signal_histos.append(signal_files[i].Get(histo))
    signal_histos[i].SetLineWidth(3)
    signal_histos[i].SetLineStyle(1)
    signal_histos[i].SetLineColor(colors[i])
    signal_histos[i].Rebin(rebin)
  ttbar_histo.SetFillColor(kRed)
  qcd_histo.SetFillColor(kYellow)
  ttbar_histo.SetLineColor(kRed)
  qcd_histo.SetLineColor(kYellow)
  ttbar_histo.SetMarkerColor(kRed)
  qcd_histo.SetMarkerColor(kYellow)
  legend.AddEntry(ttbar_histo,'t#bar{t}','f')
  legend.AddEntry(qcd_histo,'QCD from background estimate','f')
  legend.AddEntry(signal_histos[0],"Z' 1 TeV 1pb",'l')
  legend.AddEntry(signal_histos[1],"Z' 2 TeV 1pb",'l')
  legend.AddEntry(signal_histos[2] ,"Z' 3 TeV 1pb",'l')
  stack.Add(ttbar_histo)
  stack.Add(qcd_histo)
  errors=ttbar_histo.Clone(histo+'tmp')
  errors.Add(qcd_histo)
  err=TGraphAsymmErrors(errors)
  stack.Draw('hist')
  stack.GetXaxis().SetRangeUser(0,4000)
  err.SetFillStyle(3145)
  err.SetFillColor(kGray)
  errors.SetLineColor(kBlack)
  errors.SetFillStyle(0)
  errors.Draw('samehist')
  err.Draw('2')
  #summc.Draw('samehist')
  #stack.SetMinimum(0.1)
  #stack.SetMaximum(stack.GetMaximum()*1.2)
  stack.GetXaxis().SetTitle("m_{t#bar{t}} [GeV]")
  stack.GetYaxis().SetTitle('Events')
  charsize=0.05
  stack.GetYaxis().SetLabelSize(charsize)
  stack.GetYaxis().SetTitleSize(charsize)
  stack.GetYaxis().SetTitleOffset(1.6)
  stack.GetXaxis().SetLabelSize(charsize)
  stack.GetXaxis().SetTitleSize(charsize)
  stack.GetXaxis().SetTitleOffset(0.95)
  #stack.SetMinimum(0.001)
  if logy:
    c.SetLogy()
  if maxx!=0 or minx!=0:
    stack.GetXaxis().SetRangeUser(minx,maxx)
  if maxy!=0 or miny!=0:
    stack.SetMinimum(miny)
    stack.SetMaximum(maxy)
  signal_histos[0].Draw('samehist')
  signal_histos[1].Draw('samehist')
  signal_histos[2].Draw('samehist')
  legend.Draw()
  latex.Draw()
  c.SaveAs('pdf/'+name+'.pdf')