import re
import os
import pdftotext
import pickle
from tqdm import tqdm
import nltk

def pdf_footer_stripper(pdf):

	cleaned_text = ""

	for pdf_page in pdf:
		lines = pdf_page.strip().split("\n")
		last_line = lines[-1]

		if "ª" in last_line and "S" in last_line and "-" in last_line:
			del lines[-1]

		if len(lines)>3:
			if re.search("Disponibilizado pela Equipe de Documentação do Legislativo",lines[-1]) and re.search("Secretaria de Documentação", lines[-2]) and re.search("Câmara Municipal de São Paulo", lines[-3]):
				del lines[-3:]

		cleaned_lines = [l.strip() for l in lines]

		cleaned_text += " ".join(cleaned_lines)

	return cleaned_text
	

def remove_expediente_and_other_stuff(pdf_string):

	s1 = re.search("EXPEDIENTE - [0-9]*ª.*", pdf_string)
	if s1:

		return pdf_string[0:s1.span()[0]]

	s2 = re.search("EXPEDIENTE DESPACHADO PELA PRESIDÊNCIA", pdf_string)

	if s2:
		return pdf_string[0:s2.span()[0]]

	s3 =  re.search("Expediente - [0-9]*ª.*", pdf_string)

	if s3:
		return pdf_string[0:s3.span()[0]]
	
	else:
		return pdf_string


def detect_speaker(speaker):

	if "PRESIDENTE" in speaker or "PRESIDETNE" in speaker or "PRESIENTE" in speaker:

		p_match = re.search("\(.*\)", speaker)
		speaker_inner_string  = speaker[p_match.span()[0]: p_match.span()[1]]

		president_name = re.sub("\)|\(","", speaker_inner_string).split("-")[0].split("–")[0].strip().upper()

		return president_name.replace("-", "").replace("–", "").strip()

	else:

		return re.sub("\(.*\)|-|–|O SR\.|A SRA\.","", speaker).strip().upper().replace("-", "").replace("–", "").strip()




def extract_quotes(pdf_text, sent_tokenizer):

	text_len = len(pdf_text)
	speaker_pattern = "O SR\..*\(.*\) (-|–) |A SRA\..*\(.*\) (-|–) "

	spanz = []
	i =0
	while(i<text_len-1):

		for j in range(i+1, min(text_len, i+100)):

			t = pdf_text[i:j]

			if "A"==t[0] or "O"==t[0]:
				s = re.match(speaker_pattern, t)
				if s:
					spanz.append((i,j))
					break
			else:
				break

		i+=1

	quotes = []
	
	if not spanz:
		return []
		
	quotes.append({
		"speaker": "Intro", 
		"quote":  pdf_text[0:spanz[0][0]]
		})

	spanz_len = len(spanz)

	for idx, span in enumerate(spanz):

		speaker = pdf_text[span[0]: span[1]]
		quote = ""
		if idx != spanz_len-1:
			
			quote = pdf_text[span[1]: spanz[idx+1][0]].strip()
		else:
			quote = pdf_text[span[1]:].strip()

		detected_speaker = detect_speaker(speaker)		

		quote = re.sub("sr\.", "senhor",quote, flags = re.IGNORECASE)
		quote = re.sub("sra\.", "senhora",quote, flags = re.IGNORECASE)
		quote = re.sub("srs\.", "senhores",quote, flags = re.IGNORECASE)
		quote = re.sub("sras\.", "senhoras",quote, flags = re.IGNORECASE)
		quote = re.sub("art\.", "artigo", quote, flags = re.IGNORECASE)
		quote = re.sub("Exa.", "excelência", quote, flags = re.IGNORECASE)
		quote = re.sub("Exo.", "excelêncio", quote, flags = re.IGNORECASE)
		quote = re.sub("[0-9]+\.", "#", quote)
		quote = re.sub("[0-9]+º\.", "#", quote)
		quote = re.sub("[0-9]+ª\.", "#", quote)
		
		quote = re.sub("no\.", "número", quote)

		for sentence in sent_tokenizer.tokenize(quote):	

			quotes.append({
				"speaker": detected_speaker,
				"quote": sentence
				})		

	
	return quotes


if __name__ == '__main__':
	
	quotes_dir = "./parsed_quotes/"

	if not os.path.isdir(quotes_dir):

		os.mkdir(quotes_dir)

	pdf_dir = "./camara_vereadores_sp/"

	for d in os.listdir(pdf_dir):

		print(f"DIR : {d}")
		t_quote_dir = os.path.join(quotes_dir, d)
		if not os.path.isdir(t_quote_dir):

			os.mkdir(t_quote_dir)

		for f in tqdm(os.listdir(os.path.join(pdf_dir, d))):

			with open(os.path.join(pdf_dir, d,f), "rb") as file:
				pdf = pdftotext.PDF(file)


			tt = remove_expediente_and_other_stuff(pdf_footer_stripper(pdf))
			sent_tokenizer=nltk.data.load('tokenizers/punkt/portuguese.pickle')
			quotes = extract_quotes(tt, sent_tokenizer)

			pickle.dump(quotes,open(os.path.join(t_quote_dir, f.replace(".pdf", ".pkl")), "wb"))
