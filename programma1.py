# -*- coding: utf-8 -*- 

import sys
import codecs
import nltk

def CalcolaLunghezzaEToken(frasi):
	lunghezzaTOT=0.0
	lunghezzaCAR=0.0
	tokensTOT=[]
	tokensPOStot=[]
	n=0.0
	num=0.0
	for frase in frasi:
		#divido la frase in token
		tokens=nltk.word_tokenize(frase)
		tokensPOS=nltk.pos_tag(tokens)
		#calcolo il numero di frasi
		n=n+1
		#creo la lista che contiene tutti i token del testo
		tokensTOT=tokensTOT+tokens
		tokensPOStot=tokensPOStot+tokensPOS
	for tok in tokens:
		lunghezzaCAR=lunghezzaCAR+len(tok)
		num=num+1
	lunghezzaTOT=len(tokensTOT)
	#creo una lista dei primi 5000 token
	tokensCinquemila=tokensTOT[0:5001]
	#restituisco il risultato
	return lunghezzaTOT, lunghezzaTOT/n, lunghezzaCAR/num, tokensTOT, tokensCinquemila, tokensPOStot, n

def EstraiSequenzaPOS(TestoAnalizzatoPOS):
	listaPOS=[]
	for bigramma in TestoAnalizzatoPOS:
		#aggiungo alla listaPOS in pos del bigramma
		listaPOS.append(bigramma[1])
	return listaPOS

def CalcolaTotaleFrasi(frasi):
	totFRASI=0.0
	for frase in frasi:
		#calcolo totale frasi
		totFRASI=totFRASI+1
	#restituisco il risultato
	return totFRASI

def main(file1, file2):
	totaleVocabolario1=0.0 #lunghezza vocabolario corpus 1
	totaleVocabolario2=0.0 #lunghezza vocabolario corpus 2
	n=0.0 #contatore
	vtre1=0.0 #classe di frequenza 3 corpus 1
	vsei1=0.0 #classe di frequenza 6 corpus 1
	vnove1=0.0 #classe di frequenza 9 corpus 1
	vtre2=0.0 #classe di frequenza 3 corpus 2
	vsei2=0.0 #classe di frequenza 6 corpus 2
	vnove2=0.0 #classe di frequenza 9 corpus 2
	sostantivo1=0.0 #numero di sostantivi corpus 1
	aggettivo1=0.0 #numero di aggettivi corpus 1
	verbo1=0.0 #numero di verbi corpus 1
	avverbio1=0.0 #numero di avverbi corpus 1
	sostantivo2=0.0 #numero di sostantivi corpus 2
	aggettivo2=0.0 #numero di aggettivi corpus 2
	verbo2=0.0 #numero di verbi corpus 2
	avverbio2=0.0 #numero di avverbi corpus 2
	tok1=0.0 #numero di tok corpus1
	tok2=0.0 #numero di tok corpus2
	#leggo il file
	fileInput1 = codecs.open(file1, "r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	#carico uk tokenizzatore di NLTK
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	#divido I due file in frasi
	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)
	#chiamo la funzione "CalcolaLunghezzaEToken"
	corpus1, lunghezza1, lunghezzaCar1, listaToken1, listaCinquemila1, TestoAnalizzatoPOS1, num1 =CalcolaLunghezzaEToken(frasi1)
	corpus2, lunghezza2, lunghezzaCar2, listaToken2, listaCinquemila2, TestoAnalizzatoPOS2, num2 =CalcolaLunghezzaEToken(frasi2)
	#chiamo la funzione "CalcolaTotaleFrasi"	
	totFrasi1=CalcolaTotaleFrasi(frasi1)
	totFrasi2=CalcolaTotaleFrasi(frasi2)
	#calcolo il vocabolario del testo
	vocabolario1=set(listaToken1)
	vocabolario2=set(listaToken2)
	#calcolo il vocabolario dei primi 5000 token
	vocCinquemila1=set(listaCinquemila1)
	vocCinquemila2=set(listaCinquemila2)
	#calcolo lunghezza vocabolario
	totaleVocabolario1=len(vocabolario1)
	totaleVocabolario2=len(vocabolario2)
	#creo lista con i POS dei token
	SequenzaPOS1= EstraiSequenzaPOS(TestoAnalizzatoPOS1)
	SequenzaPOS2= EstraiSequenzaPOS(TestoAnalizzatoPOS2)
	#scorro il vocabolario dei primi 5000 token un token per volta
	for tok in vocCinquemila1:
		#calcolo la frequenza di ogni token
		freqToken1=listaToken1.count(tok)
		#controllo se la frequenza del token è uguale a tre e in quel caso incremento la sua classe
		if freqToken1==3:
			vtre1 = vtre1+1
		#controllo se la frequenza del token è uguale a sei e in quel caso incremento la sua classe
		elif freqToken1==6:
			vsei1 = vsei1+1
		#controllo se la frequenza del token è uguale a nove e in quel caso incremento la sua classe
		elif freqToken1==9:
			vnove1 = vnove1+1
	#scorro il vocabolario dei primi 5000 token un token per volta
	for tok in vocCinquemila2:
		#calcolo la frequenza di ogni token
		freqToken2=listaToken2.count(tok)
		#controllo se la frequenza del token è uguale a tre e in quel caso incremento la sua classe
		if freqToken2==3:
			vtre2 = vtre2+1
		#controllo se la frequenza del token è uguale a sei e in quel caso incremento la sua classe
		elif freqToken2==6:
			vsei2 = vsei2+1
		#controllo se la frequenza del token è uguale a nove e in quel caso incremento la sua classe
		elif freqToken2==9:
			vnove2 = vnove2+1
	for tok in SequenzaPOS1:
		#controllo che il tok non sia né un punto né una virgola
		if (tok!="," and tok!="."):
			tok1=tok1+1
		#controllo che il tok sia un sostantivo
		if (tok=="NN" or tok=="NNS" or tok=="NNP" or tok=="NNPS"):
			sostantivo1=sostantivo1+1
		#controllo che il tok sia un aggettivo
		if (tok=="JJ" or tok=="JJR" or tok=="JJS"):
			aggettivo1=aggettivo1+1
		#controllo che il tok sia un verbo
		if (tok=="VB" or tok=="VBD" or tok=="VBG" or tok=="VBN" or tok=="VBP" or tok=="VBZ"):
			verbo1=verbo1+1
		#controllo che il tok sia un avverbio
		if (tok=="RB" or tok=="RBR" or tok=="RBS"):
			avverbio1=avverbio1+1
	for tok in SequenzaPOS2:
		#controllo che il tok non sia né un punto né una virgola
		if (tok!="," and tok!="."):
			tok2=tok2+1
		#controllo che il tok sia un sostantivo
		if (tok=="NN" or tok=="NNS" or tok=="NNP" or tok=="NNPS"):
			sostantivo2=sostantivo2+1
		#controllo che il tok sia un aggettivo
		if (tok=="JJ" or tok=="JJR" or tok=="JJS"):
			aggettivo2=aggettivo2+1
		#controllo che il tok sia un verbo
		if (tok=="VB" or tok=="VBD" or tok=="VBG" or tok=="VBN" or tok=="VBP" or tok=="VBZ"):
			verbo2=verbo2+1
		#controllo che il tok sia un avverbio
		if (tok=="VB" or tok=="VBD" or tok=="VBG" or tok=="VBN" or tok=="VBP" or tok=="VBZ"):
			avverbio2=avverbio2+1
	#stampo I risultati:
	print
	print "PUNTO 1: il numero totale di frasi e di token"
	print "Il file", file1, "ha in totale", totFrasi1 , "frasi e", corpus1, "token"
	print "Il file", file2, "ha in totale", totFrasi2 , "frasi e", corpus2, "token"
	print
	print "PUNTO 2: la lunghezza media delle frasi in termini di token e la lunghezza media delle parole in termini di caratteri"	
	print "Lunghezza media delle frasi in termini di token del file", file1, "---",lunghezza1
	print "Lunghezza media delle parole in termini di caratteri del file", file1, "---", lunghezzaCar1
	print "Lunghezza media delle frasi in termini di token del file", file2,"---", lunghezza2
	print "Lunghezza media delle parole in termini di caratteri del file", file2,"---", lunghezzaCar2
	print	
	print "PUNTO 3: la grandezza del vocabolario e la Type Token Ratio (TTR) all'aumentare del corpus per porzioni incrementali di 1000 token (1000 token, 2000 token, 3000 token, etc.)"	
	print "File:", file1, "\tgrandezza vocabolario", totaleVocabolario1
	for tok in listaToken1:
		n=n+1
		if (n==1000):
			mille=len(set(listaToken1[0:1001])) 
			print "TTR a 1000 token:", mille/n #calcolo il TTR sui primi 1000 token
		if (n==2000):
			duemila=len(set(listaToken1[0:2001]))
			print "TTR a 2000 token:", duemila/n #calcolo il TTR sui primi 2000 token
		if (n==3000):
			tremila=len(set(listaToken1[0:3001]))
			print "TTR a 3000 token:", tremila/n #calcolo il TTR sui primi 3000 token
		if (n==4000):
			quattromila=len(set(listaToken1[0:4001]))
			print "TTR a 4000 token:", quattromila/n #calcolo il TTR sui primi 4000 token
		if (n==5000):
			cinquemila=len(set(listaToken1[0:5001])) 
			print "TTR a 5000 token:", cinquemila/n #calcolo il TTR sui primi 5000 token
	print "File:", file2, "\tgrandezza vocabolario", totaleVocabolario2
	for tok in listaToken2:
		n=n+1
		if (n==1000):
			mille=len(set(listaToken2[0:1001]))
			print "TTR a 1000 token:", mille/n #calcolo il TTR sui primi 1000 token
		if (n==2000):
			duemila=len(set(listaToken2[0:2001]))
			print "TTR a 2000 token:", duemila/n #calcolo il TTR sui primi 2000 token
		if (n==3000):
			tremila=len(set(listaToken2[0:3001]))
			print "TTR a 3000 token:", tremila/n #calcolo il TTR sui primi 3000 token
		if (n==4000):
			quattromila=len(set(listaToken2[0:4001]))
			print "TTR a 4000 token:", quattromila/n #calcolo il TTR sui primi 4000 token
		if (n==5000):
			cinquemila=len(set(listaToken2[0:5001]))
			print "TTR a 5000 token:", cinquemila/n #calcolo il TTR sui primi 5000 token
	print
	print "PUNTO 4: la grandezza delle classi di frequenza |v3|, |v6|, e |v9| sui primi 5000 token:"	
	print "File:", file1, "\t|v3|=", vtre1,"\t|v6|=", vsei1,"\t|v9|=", vnove1
	print "File:", file2, "\t|v3|=", vtre2,"\t|v3|=", vsei2,"\t|v3|=", vnove2
	print
	print "PUNTO 5: il numero medio di Sostantivi, Aggettivi e Verbi per frase:"	
	print "File: ", file1
	print "\tNumero medio di sostantivi per frase:", sostantivo1/num1
	print "\tNumero medio di aggettivi per frase:", aggettivo1/num1
	print "\tNumero medio di verbi per frase:", verbo1/num1
	print "File: ", file2
	print "\tNumero medio di sostantivi per frase:", sostantivo2/num2
	print "\tNumero medio di aggettivi per frase:", aggettivo2/num2
	print "\tNumero medio di verbi per frase:", verbo2/num2
	print
	print "PUNTO 6: la densità lessicale, calcolata come il rapporto tra il numero totale di occorrenze nel testo di Sostantivi, Verbi, Avverbi, Aggettivi e il numero totale di parole nel testo (ad esclusione dei segni di punteggiatura marcati con POS , e .):"	
	print "Densità lessicale del file: ", file1
	print "\t", (sostantivo1+verbo1+avverbio1+aggettivo1)/(tok1)
	print "Densità lessicale del file: ", file1
	print "\t", (sostantivo2+verbo2+avverbio2+aggettivo2)/(tok2)
	print

main(sys.argv[1], sys.argv[2]) 