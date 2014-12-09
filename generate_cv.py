#!/usr/bin/python

import csv
import os
import shutil
import subprocess

def firstline(name,row):
	files=[]
	if row[0] == 'CVLANGUAGE':
		for language in row[1:]:
			files.append(open('temporal/CV_'+name+'_'+language+'.sty','w'))
	else:
		print 'First ROW of csv file must be CVLANGUAGE'
		raise SystemExit
	return files


if __name__ == "__main__":
	name='GRC'
	subprocess.call(['rm','-R','temporal'])
	subprocess.call(['rm','-R','output'])
	os.mkdir('temporal')
	os.mkdir('output')
	shutil.copy('base_CV.tex','temporal/base_CV.tex')
	shutil.copy('personal_photo.jpg','temporal/personal_photo.jpg')
	with open('CV_info.csv') as file:
		info = csv.reader(file,delimiter=';')
		files = []
		languages=[]
		for idx,row in enumerate(info):
			if idx==0:
				languages=row[1:]
				files=firstline(name,row)
			else:
				for idlan,lan in enumerate(languages):			
					files[idlan].write('\\newcommand{\\'+row[0]+'}{'+row[1+idlan]+'}\n')
		os.chdir('temporal')
		for idlan,lan in enumerate(languages):
			files[idlan].close()
			infoname = 'CV_'+name+'_'+lan+'.sty'
			cvlanname ='CV_'+name+'_'+lan+'.tex'
			pdfname =  'CV_'+name+'_'+lan+'.pdf' 
			shutil.copy(infoname,'../output/'+infoname)
			os.rename(infoname,'CV_INFO.sty')
			shutil.copy('base_CV.tex',cvlanname)
			shutil.copy(cvlanname,'../output/'+cvlanname)
			subprocess.call(['pdflatex','-interaction=batchmode','\\input{'+cvlanname+'}'])
			subprocess.call(['pdflatex','-interaction=batchmode','\\input{'+cvlanname+'}'])
			shutil.copy(pdfname,'../output/'+pdfname)
		os.chdir('..')
		subprocess.call(['rm','-R','temporal'])

