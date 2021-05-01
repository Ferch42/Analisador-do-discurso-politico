import os
import requests

def save_pdf_file(base_url, file_name):
	
	print(f"Requesting file {file_name}")
	file_url = os.path.join(base_url, file_name)

	r = requests.get(file_url)
	if r.status_code ==200:
		
		print("VALID FILE")
		### IT IS A VALID FILE
		with open(os.path.join(l_folder_path, file_name), "wb") as f:
			f.write(r.content)



ordinary_base_url = "https://www.saopaulo.sp.leg.br/static/atas_anais_cmsp/anadig/Sessoes/Ordinarias/"
extraordinary_base_url = "https://www.saopaulo.sp.leg.br/static/atas_anais_cmsp/anadig/Sessoes/Extraordinarias/"
solene_base_url = "https://www.saopaulo.sp.leg.br/static/atas_anais_cmsp/anadig/Sessoes/Solenes/"

base_dir = "./camara_vereadores_sp/"
legistraturas = range(13,19)


for l in legistraturas:

	l_folder = f"L{l}"

	l_folder_path = os.path.join(base_dir, l_folder)

	if not os.path.isdir(l_folder_path):
		os.mkdir(l_folder_path)

	for i in range(1,1000):

		save_pdf_file(base_url = ordinary_base_url, file_name = f"{i:03}SO{l:02}.pdf")
		save_pdf_file(base_url = extraordinary_base_url , file_name = f"{i:03}SE{l:02}.pdf")
		save_pdf_file(base_url = solene_base_url, file_name = f"{i:03}SS{l:02}.pdf")



