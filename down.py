## read PDF
import PyPDF2
import re

def read_pdf(pdfFile):
	"Read the pdf file and return a dic with all the Books data for the fields: numbers, titles, authors. edition years and urls."

	#pdfFile = "0Springer Ebooks list.pdf"
	pdfRead = PyPDF2.PdfFileReader(pdfFile)

	for i_page in range(pdfRead.getNumPages()):
		page = pdfRead.getPage(i_page)
		#print("=============================================")
		#print(" Read page Number: " + str(1+ pdfRead.getPageNumber(page)))
		pageContent = page.extractText()
		#print(pageContent)
		all_lines = re.split("\n",pageContent)
		if i_page == 0:
			all_lines = all_lines[0:-4]
			Book_nums =  []
			Book_titles = []
			Book_authors = []
			Book_editions = []
			Book_urls = []

		if i_page == pdfRead.getNumPages(): all_lines = all_lines ## need to check if any problem with last page

		## Remove extra elements regarding Edition that we dont want and cant control
		indx_ed = [ jj for jj, elem in enumerate(all_lines) if "ed." in elem ]
		indx_ed.reverse() ## reverse the list to start by the end, so the indexs are valid
		#print('Lenght all Lines: '+ str(len(all_lines)))
		#print(all_lines)
		for jk in range(len(indx_ed)): del all_lines[indx_ed[jk]] ## delete positions wity "ed." chain that we dont want

		## Remove blank spaces but not necesary. For some reason, program does not read well all ahuthors and
		## leaves a '' space on them that is better to keep.
		#try:
		#	all_lines.remove('') ## we remove all blank fields
		#	all_lines.remove('')
		#except ValueError:
		#	pass  # do nothing!

		#print("Read fields corrected: Ed. and blank fields deleted")
		#print('Lenght all Lines: '+ str(len(all_lines)))
		#print(all_lines)
		#print("-------------------------")

		## For each page:
		for i_line in range(0,len(all_lines),5): ## we check each line and assign it to its corresp. list

			if i_line == 0: ## at the first line, we create the lists used at each page. Temporal.
				k= 0  # counter for the number for the number of books. vector index
				k_extra = 0 ## parameter to control extra lines in author field
				Book_num =  []
				Book_title = []
				Book_author = []
				Book_edition = []
				Book_url = []

			if (i_line+k_extra +1 >= len(all_lines)): break

			#print("lenght: " + str(len(all_lines)) + ", index: " + str(i_line+k_extra))
			#print("It. "+str(i_line)+", Book Num " + all_lines[i_line+k_extra])


			## Add data to the corresponding field list for each page
			Book_num.append(all_lines[i_line+k_extra])
			Book_title.append(all_lines[i_line+1+k_extra])
			Book_author.append(all_lines[i_line+2+k_extra])

			if (i_page == 0 and i_line !=0) or (i_page != 0):
				if  (len(all_lines[i_line+3+k_extra]) != 4 or not (all_lines[i_line+3+k_extra].isdigit() )): ## check if edition field is a year or another author line
					#print("::: Found a extra line jump in the author field :::")
					#print("Wrong field: "+all_lines[i_line+3+k_extra])
					Book_author[k] = all_lines[i_line+2+k_extra]+all_lines[i_line+2+k_extra+1] ## adds the extra authors to the field
					k_extra += 1 # if the edition field has not length 4, it detects an extra line in the author field
					if  (len(all_lines[i_line+3+k_extra]) != 4 or not (all_lines[i_line+3+k_extra].isdigit())):
						#print("Second wrong field: "+all_lines[i_line+3+k_extra])
						Book_author[k] = all_lines[i_line+2+k_extra-1]+all_lines[i_line+2+k_extra]+all_lines[i_line+2+k_extra+1] ## adds the extra authors to the field
						k_extra += 1
						if  (len(all_lines[i_line+3+k_extra]) != 4 or not (all_lines[i_line+3+k_extra].isdigit())):
							#print("Third wrong field: "+all_lines[i_line+3+k_extra])
							Book_author[k] = Book_author[k]+all_lines[i_line+2+k_extra+1]
							k_extra += 1
							if  (not (all_lines[i_line+2+k_extra].isdigit())): print("Error! At book nº " + str(Book_num[k]))

			#print("k_extra:"+str(k_extra)+", Len year:"+str(len(all_lines[i_line+3+k_extra])))
			Book_edition.append(all_lines[i_line+3+k_extra])
			Book_url.append(all_lines[i_line+4+k_extra])
			k = +1

		## Add the data collected for each page to the full field lists
		Book_nums.extend(Book_num)
		Book_titles.extend(Book_title)
		Book_authors.extend(Book_author)
		Book_editions.extend(Book_edition)
		Book_urls.extend(Book_url)

		#print(Book_num)
		#print(Book_title)
		#print(Book_author)
		#print(Book_edition)
		#print(Book_url)
		#print('')
	#print(" :::::::::::::::::::::::::::::::::::::::::::::::::::::::::.")
	#print("Final data lists")
	#print(len(Book_nums),len(Book_titles),len(Book_authors),len(Book_editions),len(Book_urls))
	## Printing the data lists in columns to check if everything is correct.
	#for v in zip(*[ Book_nums,[' ::: ']*len(Book_nums), Book_titles,[' ::: ']*len(Book_nums), Book_authors,[' ::: ']*len(Book_nums), Book_editions, [' ::: ']*len(Book_nums), Book_urls  ]):
	#	print(*v)
		## Found that author fields with special characteres are not read, instead filled with ''
	print("Number of Books read from pdf: "+str(len(Book_nums)))
	data_dic = { "Number": Book_nums, "Title": Book_titles, "Author": Book_authors,"Edition": Book_editions,"URL": Book_urls}
	return data_dic

#def url_crop(url_list)
############################################################
## Get web source code:
import requests
import urllib.parse

def read_webcode(url_web,erased):
	#weburl = "https://link.springer.com/book/10.1007%2Fb100747"

	down_urls = []
	url_constant = "https://link.springer.com/content/pdf/1"

	#erased = [10,13,15, 31, 53, 117,406]
	for jj in range(0,len(url_web)):
		if jj in erased: continue
		weburl = url_web[jj]
		print(jj),print(weburl)

		webcode =  requests.get(weburl)

		plaincode = webcode.text
		#'href="/content/pdf/1*\.pdf"'
		ini_index = plaincode.index('href="/content/pdf/1')+20
		fin_index = plaincode.index('.pdf"',ini_index)+4
		new_url= plaincode [ini_index:fin_index]

		down_url = url_constant+new_url
		down_urls.append(down_url)

	print('Number of urls: '+ str(len(down_urls)))
	print(down_urls)
	return down_urls

####################################################################################
## Crea el nombre de cada fichero a partir del año y el titulo
def create_filename(book_nums,book_years,book_titles,erased):
	## Creates a file name from the year and title of the book:
	## yyyy_title
	#erased = [10,13, 15, 31, 53, 117,406]
	file_names = []
	for jk in range(0,len(book_years)):
		if jk in erased: continue
		new_name = book_titles[jk]
		_years_= book_years[jk]
		numbers__ = book_nums[jk]
		try:
			new_name = new_name.replace(' ', '')
		except ValueError:
			pass  # do nothing!
		try:
			new_name = new_name.replace('.', '-')
		except ValueError:
			pass  # do nothing!
		#try:
		#	new_name = new_name.replace('.', '-')
		#except ValueError:
		#	pass  # do nothing!
		file_name = numbers__+'_'+new_name+'_'+_years_
		file_names.append(file_name)
	print('Number of names: '+ str(len(file_names)))
	print(file_names)
	return file_names

####################################################################################
## Parte de la descarga
import urllib.request

def download_file(down_urls,file_names):

	down_folder = "/media/dani/A490B32290B2FA3E1/Home/Documents/Biblioteca Springer/" ## constante, carpeta de descarga
	k_urls = 0
	for jkk in range(0,len(down_urls)):
		#if jkk < 3 : continue
		file_name = down_folder+file_names[jkk]
		d_url = down_urls[jkk]
		urllib.request.urlretrieve(d_url,file_name)
		k_urls += 1
	print('Number of files downloaded: '+ str(k_urls) )


########################################



def prepare_data(pdfFile,erased):
	"This functions returns the values directly used for download: url and complete file name."

	## read:    http://link.springer.com/openurl?genre=book&isbn=978-1-4939-9621-6
	## to down: https://link.springer.com/content/pdf/10.1007%2F978-3-319-91155-7.pdf
	#indx_last = rfind()
	data_dic = read_pdf(pdfFile)

	urls_web = data_dic["URL"]
	urls_web = urls_web[1:]


	book_nums = data_dic["Number"]
	book_nums = book_nums[1:]
	book_years = data_dic["Edition"]
	book_years = book_years[1:]
	book_titles = data_dic["Title"]
	book_titles = book_titles[1:]

	#print(urls_web)
	down_urls = read_webcode(urls_web,erased)
	file_names = create_filename(book_nums,book_years,book_titles,erased)
	download_file(down_urls,file_names)


	############################################################################################
	############################################################################################

erased = [10,13, 15, 31, 53, 54, 66, 109, 117,172, 174, 196, 279, 347, 373, 377, 348, 406]

pdfFile = "0Springer Ebooks list.pdf"
prepare_data(pdfFile,erased)
