# -*- coding: utf-8 -*- 

import sys
import codecs
import nltk
from nltk import bigrams
from nltk import trigrams
import math

def EstraiTestoTokenizzato(frasi):
	tokensTOT=[]
	tokensPOStot=[]
	for frase in frasi:
		#divido la frase in token
		tokens=nltk.word_tokenize(frase)
		#creo la lista che contiene tutti i token del testo
		tokensTOT=tokensTOT+tokens
		tokensPOS=nltk.pos_tag(tokens)
		#creo la lista che contiene tutti i bigramma (token, pos) del testo
		tokensPOStot=tokensPOStot+tokensPOS
	return tokensTOT, tokensPOStot 

def EstraiSequenzaPOS(TestoAnalizzatoPOS):
	sostantivi=[] #creo lista di sostantivi
	aggettivi=[] #creo lista di aggettivi
	POS=[] #creo lista di POS
	freqMAX=0.0
	for bigramma in TestoAnalizzatoPOS:
		#cerco i sostantivi
		if (bigramma[1]=="NN" or bigramma[1]=="NNS" or bigramma[1]=="NNP" or bigramma[1]=="NNPS"):
			#aggiungo il token alla lista di sostantivi		
			sostantivi.append(bigramma[0])
		if (bigramma[1]=="JJ" or bigramma[1]=="JJR" or bigramma[1]=="JJS"):		
			aggettivi.append(bigramma[0])
		POS.append(bigramma[1])
	return sostantivi, aggettivi, POS

def CalcoloProbabilitaCongiunta(TestoTokenizzato, LunghezzaCorpus, Token1, Token2):
	DistribuzioneDiFrequenzaToken=nltk.FreqDist(TestoTokenizzato)
	probabilitaToken1=(DistribuzioneDiFrequenzaToken[Token1]*1.0/LunghezzaCorpus*1.0) 
	#calcolo la probabilità del token
	probabilitaToken2=(DistribuzioneDiFrequenzaToken[Token2]*1.0/LunghezzaCorpus*1.0)
	#calcolo la probabilità condizionata	
	probCondizionata = (probabilitaToken1 * probabilitaToken2) / probabilitaToken2
	#calcolo la probabilità congiunta
	probCongiunta = probabilitaToken2 * probCondizionata
	return probCongiunta		

def LocalMutualInformation(TestoTokenizzato, LunghezzaCorpus, Token1, Token2, FreqBigramma):
	DistribuzioneDiFrequenzaToken=nltk.FreqDist(TestoTokenizzato)
	probabilitaToken1=(DistribuzioneDiFrequenzaToken[Token1]*1.0/LunghezzaCorpus*1.0) 
	#calcolo la probabilità del token
	probabilitaToken2=(DistribuzioneDiFrequenzaToken[Token2]*1.0/LunghezzaCorpus*1.0)
	#calcolo la probabilità del bigramma
	probabilitaBigramma= (FreqBigramma*0.1 / LunghezzaCorpus*1.0)
	probCondizionata = (probabilitaToken1 * probabilitaToken2) / probabilitaToken2
	#calcolo la probabilità congiunta
	probCongiunta = probabilitaToken2 * probCondizionata	
	#calcolo la local mutual information
	lmi = probabilitaBigramma * (math.log((probabilitaBigramma / (probabilitaToken1*probabilitaToken2)),2))
	return lmi

def FrequenzaMaggioreDi2(frase, FrequenzaToken):
	lunghezza=len(frase)
	n=0
	#controllo se la frequenza è maggiore di 2 per ogni token della frase
	for tok in frase:
		if(FrequenzaToken[tok]>2):
			n=n+1
	if(n==lunghezza):
		return "true"
	else:
		return "false"

def MarkovOrdine0(testoTokenizzato, frasi):
    lunghezzaCorpus=len(testoTokenizzato) 
    listaFrasiTokenizzate=[]
    freqToken={}
    #Calcolo la distribuzione dei bigrammi
    DistribuzioneDiFrequenza=nltk.FreqDist(testoTokenizzato) 
    #tokenizzo frase per frase
    for frase in frasi:
        fraseTokenizzata=nltk.word_tokenize(frase)
        listaFrasiTokenizzate.append(fraseTokenizzata)
    #calcolo la freqenza di ciascun token 
    for tok in testoTokenizzato:
	freq=testoTokenizzato.count(tok)
	freqToken[tok]=freq
    prob=1.0
    probMassima=0.0
    for tok in frase:
	#controllo se la frase è minore di 8 token 
	if(len(frase)<=8):
		#controllo che ogni token abbia frequenza maggiore di 2
		if(FrequenzaMaggioreDi2(frase, freqToken)=="true"):
			probToken=DistribuzioneDiFrequenza[tok]*1.0/lunghezzaCorpus*1.0
			#nel modello di ordine 0 la probabilita' della frase equivale al prodotto delle probabilita' dei singoli token
			prob=prob*probToken
			#estraggo la probabilita' massima
			if prob > probMassima:
			   probMassima=prob
    print "Markov di ordine 0"
    print "\tLa frase con probabilità più alta:", fraseTokenizzata
    print "\tprobabilità:", probMassima

def MarkovOrdine1(testoTokenizzato, frasi):
	lung=len(testoTokenizzato)
	ProbMassima=0.0
	Prob=0.0
	FraseMassima=""
	freqToken={}
	#calcolo lunghezza corpus
	lunghezzaCorpus=len(testoTokenizzato)
	#calcolo la freqenza di ciascun token 
	for tok in testoTokenizzato:
		freq=testoTokenizzato.count(tok)
		freqToken[tok]=freq
	#trovo i token
	for i in frasi:
		frase=nltk.word_tokenize(i)
		bigra= list(nltk.bigrams(frase))
		#controllo se la frase è minore di 8 token 
		if(len(frase)<=8):
			#controllo che ogni token abbia frequenza maggiore di 2
			if(FrequenzaMaggioreDi2(frase, freqToken)=="true"):
				#calcolo la probabilità del primo token
				Prob=freqToken[frase[0]]*1.0/lung*1.0
				for x in bigra:
					probToken=bigra.count(x)*1.0/freqToken[x[0]]*1.0
					Prob=Prob*probToken
		#probabilità massima
		if(ProbMassima<Prob):
			FraseMassima = i
			ProbMassima = Prob
        print "Markov di ordine 1"
        print "\tLa frase con probabilità più alta:", FraseMassima
        print "\tprobabilità:", ProbMassima

def main(file1, file2):
	ventiToken1={} 
	ventiToken2={} 
	sost1={}
	sost2={}
	agg1={}
	agg2={}
	lista1={}
	lista2={}
	tipoPOS1={}
	tipoPOS2={}
	listaPOS1={}
	listaPOS2={}
	listaTriPOS1={}
	listaTriPOS2={}
	listaBig1={}
	listaBig2={}
	listaPC1={}
	listaPC1={}
	frequenzaToken1={}
	frequenzaBigramma1={}
	frequenzaToken2={}
	frequenzaBigramma2={}
	congiunta1={}
	congiunta2={}
	LMIBigramma1={}
	LMIBigramma2={}
	freqMAX=0.0
	n1=0.0
	n2=0.0
	n1_2=0.0
	n2_2=0.0
	n1_3=0.0
	n2_3=0.0	
	n1_4=0.0
	n2_4=0.0
	n1_5=0.0
	n2_5=0.0
	n1_6=0.0
	n2_6=0.0
	n1_7=0.0
	n2_7=0.0
	n1_8=0.0
	n2_8=0.0
	n1_9=0.0
	n2_9=0.0
	n1_10=0.0
	n2_10=0.0
	#leggo i file
	fileInput1 = codecs.open(file1, "r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	#carico il tokenizzatore di NLTK
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	#divido I due file in frasi:
	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)
	#chiamo la funzione "EstraiTestoTokenizzato" sul testo diviso in frasi
	TestoTokenizzato1, TestoAnalizzatoPOS1 = EstraiTestoTokenizzato(frasi1)
	TestoTokenizzato2, TestoAnalizzatoPOS2 =EstraiTestoTokenizzato(frasi2)
	#chiamo la funzione "EstraiSequenzaPOS" sul testo analizzato
	paroleSostantivi1, paroleAggettivi1, POS1 = EstraiSequenzaPOS(TestoAnalizzatoPOS1)	
	paroleSostantivi2, paroleAggettivi2, POS2 = EstraiSequenzaPOS(TestoAnalizzatoPOS2)	
	#Calcolo tutti i bigrammi del file1
	bigrammi1=bigrams(TestoTokenizzato1)
	#Calcolo tutti i bigrammi del file2
	bigrammi2=bigrams(TestoTokenizzato2) 
	#Calcolo la distribuzione dei bigrammi
	DistribuzioneDiFrequenzaBigrammi1=nltk.FreqDist(bigrammi1) 
	DistribuzioneDiFrequenzaBigrammi2=nltk.FreqDist(bigrammi2) 
	#Calcolo tutti i bigrammi della lista di POS1
	bigrammiPOS1=bigrams(POS1) 
	#Calcolo tutti i bigrammi della lista di POS2
	bigrammiPOS2=bigrams(POS2) 
	 #Calcolo la distribuzione dei bigrammi
	DistribuzioneDiFrequenzaBigrammiPOS1=nltk.FreqDist(bigrammiPOS1)
	DistribuzioneDiFrequenzaBigrammiPOS2=nltk.FreqDist(bigrammiPOS2) 
	#Calcolo tutti i trigrammi della lista di POS1
	trigrammiPOS1=trigrams(POS1)
	#Calcolo tutti i trigrammi della lista di POS2 
	trigrammiPOS2=trigrams(POS2)
	#Calcolo la distribuzione dei trigrammi
	DistribuzioneDiFrequenzaTrigrammiPOS1=nltk.FreqDist(trigrammiPOS1) 
	DistribuzioneDiFrequenzaTrigrammiPOS2=nltk.FreqDist(trigrammiPOS2) 	
	#file1
	for tok in TestoTokenizzato1:
		#calcolo la frequenza di ogni token
		freqToken1=TestoTokenizzato1.count(tok)
		#associo il token alla sua frequenza
		ventiToken1[tok] = freqToken1
	for k in list(ventiToken1):
		#controllo se è presente la punteggiatura
		if (k=="!" or k=="." or k=="," or k=="-" or k==":" or k=="(" or k==")" or k==";" or k=="'" or k=="''" or k=="..." or k=="<<" or k==">>"):
			#elimiino la punteggiatura dal dizionario ventiToken1
			del ventiToken1[k]
	print "PUNTO 1: estraete ed ordinate in ordine di frequenza decrescente, indicando anche la relativa frequenza"
	#stampo i risultati file1
	print "i 20 token più frequenti escludendo la punteggiatura del file", file1, ": "
	#ordino in maniera decrescente in base alla frequenza
	for w in sorted(ventiToken1, key=ventiToken1.get, reverse=True):
		#controllo che i token stampati non siano maggiori di 20
		if(n1<=20):
			#stampo il token e la sua occorrenza
			print w, "\toccorrenza", ventiToken1[w]
			n1=n1+1
	#file 2
	for tok in TestoTokenizzato2:
		#calcolo la frequenza di ogni token
		freqToken2=TestoTokenizzato2.count(tok)
		#associo il token alla sua frequenza
		ventiToken2[tok] = freqToken2
	for i in list(ventiToken2):
		#controllo se è presente la punteggiatura
		if (i=="!" or i=="." or i=="," or i=="-" or i==":" or i=="(" or i==")" or i==";" or i=="'" or i=="''" or i=="..." or i=="<<" or i==">>"):
			#elimiino la punteggiatura dal dizionario ventiToken2			
			del ventiToken2[i]
	#stampo i risultati file2
	print
	print "i 20 token più frequenti escludendo la punteggiatura del file", file2, ": "
	#ordino in maniera decrescente in base alla frequenza
	for y in sorted(ventiToken2, key=ventiToken2.get, reverse=True):
		#controllo che i token stampati non siano maggiori di 20
		if(n2<=20):
			#stampo il token e la sua occorrenza
			print y, "\toccorrenza", ventiToken2[y]
			n2=n2+1
	print
	print
	print
	for tok in paroleSostantivi1:
		#calcolo la frequenza di ogni token
		freqToken1=TestoTokenizzato1.count(tok)
		#associo a ogni sostantivo la sua frequenza 
		sost1[tok] = freqToken1
	print "i 20 sostantivi più frequenti del file",file1,": "
	#ordino in maniera decrescente in base alla frequenza
	for w in sorted(sost1, key=sost1.get, reverse=True):
		#controllo che i token stampati non siano maggiori di 20
		if(n1_2<=20):
			#stampo il token e la sua occorrenza
			print w, "\toccorrenza", sost1[w]
			n1_2=n1_2+1
	print
	for tok in paroleSostantivi2:
		#calcolo la frequenza di ogni token
		freqToken2=TestoTokenizzato2.count(tok)
		#associo a ogni sostantivo la sua frequenza 
		sost2[tok] = freqToken2
	print "i 20 sostantivi più frequenti del file",file2,": "
	#ordino in maniera decrescente in base alla frequenza
	for w in sorted(sost2, key=sost2.get, reverse=True):
		#controllo che i token stampati non siano maggiori di 20
		if(n2_2<=20):
			#stampo il token e la sua occorrenza
			print w, "\toccorrenza", sost2[w]
			n2_2=n2_2+1
	print
	print
	print
	#file 1
	for tok in paroleAggettivi1:
		#calcolo la frequenza di ogni token
		freqToken1=TestoTokenizzato1.count(tok)
		#associo a ogni sostantivo la sua frequenza 
		agg1[tok] = freqToken1
	print "i 20 aggettivi più frequenti del file",file1,": "
	#ordino in maniera decrescente in base alla frequenza
	for w in sorted(agg1, key=agg1.get, reverse=True):
		#controllo che i token stampati non siano maggiori di 20
		if(n1_3<=20):
			#stampo il token e la sua occorrenza
			print w, "\toccorrenza", agg1[w]
			n1_3=n1_3+1
	for tok in paroleAggettivi2:
		#calcolo la frequenza di ogni token
		freqToken2=TestoTokenizzato2.count(tok)
		agg2[tok] = freqToken2
	#file 2
	print
	print "i 20 aggettivi più frequenti del file",file2,": "
	#ordino in maniera decrescente in base alla frequenza
	for w in sorted(agg2, key=agg2.get, reverse=True):
		#controllo che i token stampati non siano maggiori di 20
		if(n2_3<20):
			#stampo il token e la sua occorrenza
			print w, "\toccorrenza", agg2[w]
			n2_3=n2_3+1
	print
	print
	print
	#file 1
	print "I 20 bigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni nel file: ", file1
	for elem in DistribuzioneDiFrequenzaBigrammi1:
		#associo a x la prima parola del bigramma e a y la seconda parola del bigramma
		x, y=nltk.pos_tag(elem)
		#controllo che i token non contengano punteggiatura 
		if(x[1]!="." and y[1]!="." and x[1]!="," and y[1]!="," and x[1]!="?" and y[1]!="?" and x[1]!="!" and y[1]!="!" and x[1]!="CC" and y[1]!="CC" and x[1]!="IN" and y[1]!="IN" and x[1]!="DT" and y[1]!="DT"):
			lista1[elem]= DistribuzioneDiFrequenzaBigrammi1[elem]
	#ordino in maniera decrescente in base alla frequenza	
	for w in sorted(lista1, key=lista1.get, reverse=True):
		#controllo che i bigrammi stampati non siano maggiori di 20
		if(n1_4<=20):
			#stampo il bigramma e la sua occorrenza
			print w, "\toccorrenza", lista1[w]
			n1_4=n1_4+1
	print
	#file2
	print "I 20 bigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni nel file: ", file2
	for elem in DistribuzioneDiFrequenzaBigrammi2:
		#associo a z la prima parola del bigramma e a j la seconda parola del bigramma
		z, j=nltk.pos_tag(elem)
		#controllo che i token non contengano punteggiatura 
		if(z[1]!="." and j[1]!="." and z[1]!="," and j[1]!="," and z[1]!="?" and j[1]!="?" and z[1]!="!" and j[1]!="!" and z[1]!="CC" and j[1]!="CC" and z[1]!="IN" and j[1]!="IN" and z[1]!="DT" and j[1]!="DT"):
			lista2[elem]= DistribuzioneDiFrequenzaBigrammi2[elem]	
	#ordino in maniera decrescente in base alla frequenza	
	for w in sorted(lista2, key=lista2.get, reverse=True):
		#controllo che i bigramma stampati non siano maggiori di 20
		if(n2_4<=20):
			#stampo il bigramma e la sua occorrenza
			print w, "\toccorrenza:", lista2[w]
			n2_4=n2_4+1
	print
	print
	print
	#file1
	for bigramma in TestoAnalizzatoPOS1:
		#calcolo la freqeunza di ogni POS
		freqPOS1=POS1.count(bigramma[1])
		#creo un dizionario che contiente come chiave il POS e come valore il numero di occorrenza
		tipoPOS1[bigramma[1]]=freqPOS1
	print "I 10 Pos (Part-of-Speech) più frequenti del file", file1, ":"
	for w in sorted(tipoPOS1, key=tipoPOS1.get, reverse=True):
		#controllo che i POS stampati non siano maggiori di 10
		if(n1_5<=10):
			#stampo il POS e la sua occorrenza
			print w, "\toccorrenza", tipoPOS1[w]
			n1_5=n1_5+1
	#file 2
	for bigramma in TestoAnalizzatoPOS2:
		freqPOS2=POS2.count(bigramma[1])
		tipoPOS2[bigramma[1]]=freqPOS2
	print
	print "I 10 Pos (Part-of-Speech) più frequenti del file", file2, ":"
	for y in sorted(tipoPOS2, key=tipoPOS2.get, reverse=True):
		#controllo che i POS stampati non siano maggiori di 10
		if(n2_5<=10):
			#stampo il POS e la sua occorrenza
			print y, "\toccorrenza", tipoPOS2[y]
			n2_5=n2_5+1
	print
	print
	print
	#file 1
	print "I 10 bigrammi di POS (Part-of-Speech) più frequenti del file:", file1
	for elem in DistribuzioneDiFrequenzaBigrammiPOS1:
		#associo a ogni bigramma la sua frequenza
		listaPOS1[elem]= DistribuzioneDiFrequenzaBigrammiPOS1[elem]
	for w in sorted(listaPOS1, key=listaPOS1.get, reverse=True):
		#controllo che i bigrammi stampati non siano maggiori di 10
		if(n1_6<=10):
			#stampo il bigramma e la sua occorrenza
			print w, "\toccorrenza", listaPOS1[w]
			n1_6=n1_6+1
	print 
	#file2
	print "I 10 bigrammi di POS (Part-of-Speech) più frequenti del file:", file2
	for elem in DistribuzioneDiFrequenzaBigrammiPOS2:
		#associo a ogni bigramma la sua frequenza
		listaPOS2[elem]= DistribuzioneDiFrequenzaBigrammiPOS2[elem]
	for w in sorted(listaPOS2, key=listaPOS2.get, reverse=True):
		#controllo che i bigrammi stampati non siano maggiori di 10
		if(n2_6<=10):
			#stampo il bigramma e la sua occorrenza
			print w, "\toccorrenza", listaPOS2[w]
			n2_6=n2_6+1
	print
	print
	print
	#file1
	print "I 10 trigrammi di POS (Part-of-Speech) più frequenti del file:", file1
	for elem in DistribuzioneDiFrequenzaTrigrammiPOS1:
		#associo a ogni trigramma la sua frequenza
		listaTriPOS1[elem]= DistribuzioneDiFrequenzaTrigrammiPOS1[elem]
	for w in sorted(listaTriPOS1, key=listaTriPOS1.get, reverse=True):
		#controllo che i trigrammi stampati non siano maggiori di 10
		if(n1_7<=10):
			#stampo il trigramma e la sua occorrenza
			print w, "\toccorrenza", listaTriPOS1[w]
			n1_7=n1_7+1
	print
	#file2
	print "I 10 trigrammi di POS (Part-of-Speech) più frequenti del file:", file2
	for elem in DistribuzioneDiFrequenzaTrigrammiPOS2:
		#associo a ogni trigramma la sua frequenza
		listaTriPOS2[elem]= DistribuzioneDiFrequenzaTrigrammiPOS2[elem]
	for w in sorted(listaTriPOS2, key=listaTriPOS2.get, reverse=True):
		#controllo che i trigrammi stampati non siano maggiori di 10
		if(n2_7<=10):
			#stampo il trigramma e la sua occorrenza
			print w, "\toccorrenza", listaTriPOS2[w]
			n2_7=n2_7+1
	print
	print
	print
	print "PUNTO 2: Estraete ed ordinate in ordine decrescente i 20 bigrammi composti da aggettivo e sostantivo (dove ogni token deve avere una frequenza maggiore di 2):"
	print	
	#file1
	print "File:", file1	
	for tok in TestoTokenizzato1:
		#calcolo la frequenza di ogni token
		freq=TestoTokenizzato1.count(tok)
		#associo ogni token alla sua frequenza
		frequenzaToken1[tok]=freq
	#calcolo la lunghezza del corpus1
	LunghezzaCorpus1=len(TestoTokenizzato1)
	for elem in DistribuzioneDiFrequenzaBigrammi1:
		#associo a x la prima parola del bigramma e a y la seconda parola del bigramma
		x, y=nltk.pos_tag(elem)
		#verifico che la prima parola sia un aggettivo
		if(x[1]=="JJ" or x[1]=="JJR" or x[1]=="JJS"):
			#verifico che la prima parola sia un sostantivo
			if(y[1]=="NN" or y[1]=="NNS" or y[1]=="NNP" or y[1]=="NNPS"):
				#verifico che ogni token abbia frequenza maggiore di 2
				if (frequenzaToken1[x[0]]>2 and frequenzaToken1[y[0]]>2):
					#associo ogni bigramma alla sua frequenza
					frequenzaBigramma1[elem]=DistribuzioneDiFrequenzaBigrammi1[elem]
					#calcolo la probabilita congiunta del bigramma
					probCongiunta = CalcoloProbabilitaCongiunta(TestoTokenizzato1, LunghezzaCorpus1, x[0], y[0]) 
					#associo ogni bigramma alla sua probabilità congiunta
					congiunta1[elem]=probCongiunta
	freqBigra1={}
	LMIBigra1={}
	for elem in DistribuzioneDiFrequenzaBigrammi1:	
		x, y=nltk.pos_tag(elem)
		if(x[1]=="JJ" or x[1]=="JJR" or x[1]=="JJS"):
			if(y[1]=="NN" or y[1]=="NNS" or y[1]=="NNP" or y[1]=="NNPS"):
				if (frequenzaToken1[x[0]]>2 or frequenzaToken1[y[0]]>2):
					#associo ogni bigramma alla sua frequenza
					freqBigra1[elem]=DistribuzioneDiFrequenzaBigrammi1[elem]
					#calcolo la Local Mutual Information
					LMI = LocalMutualInformation(TestoTokenizzato1, LunghezzaCorpus1, x[0], y[0], freqBigra1[elem])
					#associo ogni bigramma alla sua local mutual information					
					LMIBigra1[elem] = LMI
	for tok in TestoTokenizzato2:
		#calcolo la frequenza di ogni token
		freq=TestoTokenizzato2.count(tok)
		#associo ogni token alla sua frequenza
		frequenzaToken2[tok]=freq
	#calcolo la lunghezza del corpus2
	LunghezzaCorpus2=len(TestoTokenizzato2)
	for elem in DistribuzioneDiFrequenzaBigrammi2:
		#associo a x la prima parola del bigramma e a y la seconda parola del bigramma
		x, y=nltk.pos_tag(elem)
		#verifico che la prima parola sia un aggettivo
		if(x[1]=="JJ" or x[1]=="JJR" or x[1]=="JJS"):
			#verifico che la prima parola sia un sostantivo
			if(y[1]=="NN" or y[1]=="NNS" or y[1]=="NNP" or y[1]=="NNPS"):
				#verifico che ogni token abbia frequenza maggiore di 2
				if (frequenzaToken2[x[0]]>2 and frequenzaToken2[y[0]]>2):
					#associo ogni bigramma alla sua frequenza
					frequenzaBigramma2[elem]=DistribuzioneDiFrequenzaBigrammi2[elem]
					#calcolo la probabilita congiunta del bigramma
					probCongiunta = CalcoloProbabilitaCongiunta(TestoTokenizzato2, LunghezzaCorpus2, x[0], y[0]) 
					#associo ogni bigramma alla sua probabilità congiunta
					congiunta2[elem]=probCongiunta
	freqBigra2={}
	LMIBigra2={}
	for elem in DistribuzioneDiFrequenzaBigrammi2:	
		x, y=nltk.pos_tag(elem)
		if(x[1]=="JJ" or x[1]=="JJR" or x[1]=="JJS"):
			if(y[1]=="NN" or y[1]=="NNS" or y[1]=="NNP" or y[1]=="NNPS"):
				if (frequenzaToken2[x[0]]>2 or frequenzaToken2[y[0]]>2):
					#associo ogni bigramma alla sua frequenza
					freqBigra2[elem]=DistribuzioneDiFrequenzaBigrammi2[elem]
					#calcolo la Local Mutual Information
					LM = LocalMutualInformation(TestoTokenizzato2, LunghezzaCorpus2, x[0], y[0], freqBigra2[elem])
					#associo ogni bigramma alla sua local mutual information					
					LMIBigra2[elem] = LMI

	print "---con frequenza massima, indicando anche la frequenza di ogni parola che compone il bigramma:"			
	print "File:", file1	
	for w in sorted(frequenzaBigramma1, key=frequenzaBigramma1.get, reverse=True):
	#controllo che i bigrammi stampati non sono maggiori di 20
		if(n1_8<=20):
			print w, "\toccorrenza", frequenzaBigramma1[w] #stampo il bigramma e la sua frequenza 	
			print w[0], "\toccorrenza", frequenzaToken1[w[0]] #stampo la prima parola del bigramma e la sua frequenza
			print w[1], "\toccorrenza", frequenzaToken1[w[1]] #stampo la seconda parola del bigramma e la sua frequenza
			print			
			n1_8=n1_8+1
	print "File:", file1	
	for w in sorted(frequenzaBigramma2, key=frequenzaBigramma2.get, reverse=True):
	#controllo che i bigrammi stampati non sono maggiori di 20
		if(n2_8<=20):
			print w, "\toccorrenza", frequenzaBigramma2[w] #stampo il bigramma e la sua frequenza 	
			print w[0], "\toccorrenza", frequenzaToken2[w[0]] #stampo la prima parola del bigramma e la sua frequenza
			print w[1], "\toccorrenza", frequenzaToken2[w[1]] #stampo la seconda parola del bigramma e la sua frequenza
			print			
			n2_8=n2_8+1
	print
	print
	print "---con probabilità congiunta massima, indicando anche la relativa frequenza:"	
	print "File:", file1	
	for w in sorted(congiunta1, key=congiunta1.get, reverse=True):
		if(n1_9<=20):
			n1_9=n1_9+1
			print w, "\tprobabilita congiunta:", probCongiunta #stampo il bigramma e la sua probabilità congiunta
			probabilitaToken1=(frequenzaToken1[w[0]]*1.0/LunghezzaCorpus1*1.0) #calcolo la probabilità del token
			probabilitaToken2=(frequenzaToken1[w[1]]*1.0/LunghezzaCorpus1*1.0) #calcolo la probabilità del token
			print w[0], "\tprobabilità:", probabilitaToken1 #stampo la prima parola del bigramma con la relativa probabilità
			print w[1], "\tprobabilità:", probabilitaToken2 #stampo la seconda parola del bigramma con la relativa probabilità
			print		
	print "File:", file2	
	for w in sorted(congiunta2, key=congiunta2.get, reverse=True):
		if(n2_9<=20):
			n2_9=n2_9+1
			print w, "\tprobabilita congiunta:", probCongiunta #stampo il bigramma e la sua probabilità congiunta
			probabilitaToken1=(frequenzaToken2[w[0]]*1.0/LunghezzaCorpus1*1.0) #calcolo la probabilità del token
			probabilitaToken2=(frequenzaToken2[w[1]]*1.0/LunghezzaCorpus1*1.0) #calcolo la probabilità del token
			print w[0], "\tprobabilità:", probabilitaToken1 #stampo la prima parola del bigramma con la relativa probabilità
			print w[1], "\tprobabilità:", probabilitaToken2 #stampo la seconda parola del bigramma con la relativa probabilità	
	print
	print
	print "---con local mutual information:"	
	print "File:", file1
	for w in sorted(LMIBigra1, key=LMIBigra1.get, reverse=True):
		if(n1_10<=20):
			print w, "\tlocal mutual information:", LMI #stampo il bigramma e la sua Local Mutual Information
			n1_10=n1_10+1
	print
	print "File:", file2
	for w in sorted(LMIBigra2, key=LMIBigra2.get, reverse=True):
		if(n2_10<=20):
			print w, "\tlocal mutual information:", LMI #stampo il bigramma e la sua Local Mutual Information
			n2_10=n2_10+1
	print
	print
	print
	print "PUNTO 3:"
	#file1
	print "File", file1
	#la frase con probabilita' piu' alta calcolate con modello di ordine 0
	probFrase1_0=MarkovOrdine0(TestoTokenizzato1, frasi1)
	print
	#la frase con probabilita' piu' alta calcolate con modello di ordine 1
	probFrase1_1=MarkovOrdine1(TestoTokenizzato1, frasi1)
	#file2
	print
	print
	print "File", file2
	#la frase con probabilita' piu' alta calcolate con modello di ordine 0
	probFrase2_0=MarkovOrdine0(TestoTokenizzato2, frasi2)
	print
	#la frase con probabilita' piu' alta calcolate con modello di ordine 1
	probFrase2_1=MarkovOrdine1(TestoTokenizzato2, frasi2)

main(sys.argv[1], sys.argv[2]) 