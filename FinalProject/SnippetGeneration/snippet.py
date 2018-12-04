import dominate
from dominate.tags import *
import shutil
import os
import re
from bs4 import BeautifulSoup
SNIPPET = 'snippets/'
RAW_HTML_PATH = 'source/cacm/'
BM25_RES = 'baselines_phase1_task1/bm25.txt'
QUERY_PATH = 'source/cacm.query.txt'
WINDOW = 40
def createSnippet(query, docList, queryID):
	
	cleanedQuery = clean(query)
	newHtml = dominate.document(title=cleanedQuery)
	with newHtml.body:
		h1(cleanedQuery)

	for docID in docList:

		filename = docID+'.html'
		path_ = 'file:///'+RAW_HTML_PATH+filename
		raw_html = open(RAW_HTML_PATH+filename)
		raw_html = BeautifulSoup(raw_html,'lxml')
		text = raw_html.text.strip()
		text = text.replace('\t',' ')
		text = re.sub(' +',' ',text)

		
		lines = text.split('\n')


		title = boldify(lines[0],cleanedQuery)

		originalBody = BeautifulSoup(' '.join(lines[1:]),'lxml').text.strip()
		bodyyContent = originalBody.lower().split(' ')
		queryTerms = query.lower().split(' ')
		

		start = 0
		termsInSnippet = 0
		startIndex = 0
		termsCount = len(bodyyContent)
		while start < termsCount-WINDOW:
			subArr = bodyyContent[start:start+WINDOW]
			temp = 0
			for q in queryTerms:
				temp+=subArr.count(q)

			if temp>termsInSnippet:
				termsInSnippet = temp
				startIndex = start
			start +=1


		finalSnippet = boldify(' '.join(bodyyContent[startIndex:startIndex+WINDOW]+['...']),query)
		#print finalSnippet




		with newHtml.body:
			d = div()
			with d:
				a(title,href = path_,style='text-decoration:none;font-size:22px')
				pre(path_,style = 'font-size:12px;color:green;margin:0;padding:0')
				pre(finalSnippet,style = 'font-size:12px;color:black;margin:0;padding:0')
				br()
				br()
			


		#print newHtml

	file_ = open(SNIPPET + str(queryID) + '.html','w+')
	file_.write(str(newHtml))
	file_.close()

def clean(s):
	s = s.replace('\t',' ')
	s = re.sub(' +',' ',s)
	s.replace('\n',' ')
	return s

def boldify(title,query):


	titleTerms = title.split(' ')
	queryTerms = query.lower().split(' ')
	boldedTerms = []
	for t in titleTerms:
		if t.lower() in queryTerms:
			boldedTerms.append(b(t))
		else:
			boldedTerms.append(t)

	

	pr = pre(style='margin:0;padding:0')
	count = 0
	for bo in boldedTerms:	
		count += 1

		pr.add(bo)
		pr.add(' ')
		if count % 15 ==0:
			pr.add(br())
	return pr


def getQueryMap():
	dict_ = {}
	f_ = open(QUERY_PATH)
	html = BeautifulSoup(f_.read(),'lxml')

	for doc in html.findAll('doc'):
		docno = doc.find('docno')
		queryID = int(docno.text)
		docno.decompose()
		text = doc.text.strip()
		dict_[queryID] = text
		#ctext = text.replace('\n',' ')
	return dict_

def getQRMap():
	dict_ = {}
	f = open(BM25_RES,'r')
	lines = f.readlines()
	for l in lines:
		items = l.split(' ')
		queryID = int(items[0])
		#print str(queryID)
		if queryID in dict_:
			dict_[queryID].append(items[2])
		else:
			dict_[queryID] = [items[2]] # items[2] contains docID

	return dict_


def createSnippetMain(queryResultMap,queryMap):
	shutil.rmtree(SNIPPET,ignore_errors=True)
	os.mkdir(SNIPPET)
	for i in range(1,65):
		createSnippet(queryMap[i],queryResultMap[i],i)



def main():
	queryResultMap = getQRMap()
	queryMap = getQueryMap()

	print '\n\nGenerating displayable results (html) for each query inside snippets folder...'
	createSnippetMain(queryResultMap,queryMap)
	print 'html files created!'

if __name__ == "__main__":
	main()	




