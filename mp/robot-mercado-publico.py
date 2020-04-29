from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import json

driver = webdriver.Chrome("C:\\Users\\roger\\Downloads\\Programas\\chromedriver.exe")
driver.get("http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=2")

boton_inicial = driver.find_element_by_xpath('//*[@id="btnBusqueda"]')
boton_inicial.click()

onclick=[]
time.sleep(5)
busqueda=1
array_text=[]

table = driver.find_element_by_xpath('//*[@id="pnlSearch1"]/table[1]') 
rows = table.find_elements(By.TAG_NAME, "tr") 

for row in rows: 
	for col in row.find_elements(By.TAG_NAME, "td"):
		try:
			a = col.find_element(By.TAG_NAME, "a")
			onclick.append(a.get_attribute("onclick"))
		except:
			print("No hago nada")

avanzar=11
i=0
while busqueda < 60:
	time.sleep(2)
	table = driver.find_element_by_xpath('//*[@id="pnlSearch1"]/table[1]') 
	rows = table.find_elements(By.TAG_NAME, "tr") 

	if i > 40:
		for row in rows: 
			for col in row.find_elements(By.TAG_NAME, "td"):
				try:
					a = col.find_element(By.TAG_NAME, "a")
					onclick.append(a.get_attribute("onclick"))
				except:
					print(i)

	#Paginador
	table_paginador = driver.find_element_by_xpath('//*[@id="PaginadorBusqueda__TblPages"]') 
	rows_paginador = table_paginador.find_elements(By.TAG_NAME, "tr") 
	for row_p in rows_paginador: 
		for col in row_p.find_elements(By.TAG_NAME, "td"):
			try:
				div_text = col.find_element(By.TAG_NAME, "div").text
				
				if i == avanzar:
					if avanzar > 11:
						driver.find_element_by_xpath('//*[@id="PaginadorBusqueda__TblPages"]/tbody/tr/td[13]/div').click() 
					else:
						driver.find_element_by_xpath('//*[@id="PaginadorBusqueda__TblPages"]/tbody/tr/td[12]/div').click() 
					i=avanzar-1
					avanzar=avanzar+10
					time.sleep(2)

				if int(div_text) == i:
					div = col.find_element(By.TAG_NAME, "div").click()
			except:
				div_text=""
	i=i+1
	if i == 60:
		busqueda=100
	else:
		busqueda=i

#Obtener codigos
codigo_link=None
array_codigo_link=[]
for on in onclick:
	try:
		codigo_link = on[90:114]
		if codigo_link != "":
			if codigo_link not in array_codigo_link:
				array_codigo_link.append(codigo_link)
	except:
		codigo_link=None

#Abrir ventanas por codigos
array_final=[]
for c in array_codigo_link:
	obje_final={}
	array_info_deudor=[]
	array_info_cliente=[]

	driver.get("http://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?qs="+c)
	try:
		orden_comprar=driver.find_element_by_id('lblTitleNumberAq').text
	except:
		orden_comprar=""

	try:
		nombre_orden_comprar=driver.find_element_by_id('lblTitleNameAq').text
	except:
		nombre_orden_comprar=""

	obje_final['orden_comprar']=orden_comprar
	obje_final['nombre_orden_comprar']=nombre_orden_comprar

	table_deudor = driver.find_element_by_xpath('//*[@id="tblBuyer"]') 
	rows_deudor = table_deudor.find_elements(By.TAG_NAME, "tr") 
	obje_deudor={}
	d=0	
	for row in rows_deudor: 
		for col in row.find_elements(By.TAG_NAME, "td"):
			array_info_deudor=[]
			try:
				span = col.find_element(By.TAG_NAME, "span").text
				if span != "Unidad de Compra" and span != "Razón Social" and span != "R.U.T." and span != "Dirección de Unidad de Compra":
					if d == 1:
						obje_deudor['u_compra']=span
					elif d == 3:
						obje_deudor['razon_social']=span
					elif d == 5:
						obje_deudor['rut']=span
					elif d == 7:
						obje_deudor['direccion_u_compra']=span
			except:
				span=""

			array_info_deudor.append(obje_deudor)
			d=d+1
			obje_final['info_deudor']=array_info_deudor

	table_cliente = driver.find_element_by_xpath('//*[@id="tblProveedor"]') 
	rows_cliente = table_cliente.find_elements(By.TAG_NAME, "tr") 
	obje_cliente={}
	c=0
	for row in rows_cliente:
		array_info_cliente=[]
		for col in row.find_elements(By.TAG_NAME, "td"):
			array_info_cliente=[]
			try:
				span = col.find_element(By.TAG_NAME, "span").text
				if span != "Proveedor" and span != "Razón Social" and span != "R.U.T." and span != "Sucursal" and span != "Dirección" and span != "Comuna" and span != "Contacto del Proveedor" and span != "Cargo" and span != "Teléfono" and span != "Fax" and span != "E-mail":
					if c == 1:
						obje_cliente['proveedor']=span
					elif c == 3:
						obje_cliente['razon_social']=span
					elif c == 5:
						obje_cliente['rut']=a
					elif c == 7:
						obje_cliente['sucursal']=span
					elif c == 9:
						obje_cliente['direccion']=span
					elif c == 11:
						obje_cliente['comuna']=span
					elif c == 12:
						obje_cliente['contacto_proveedor']=span
					elif c == 15:
						obje_cliente['cargo']=span
					elif c == 17:
						obje_cliente['telefono']=span
					elif c == 19:
						obje_cliente['fax']=span
					elif c == 21:
						obje_cliente['email']=span
			except:
				try:
					rut=driver.find_element_by_id('lblRutValueP').text
				except:
					rut=""
				obje_cliente['rut']=rut

			array_info_cliente.append(obje_cliente)
			c=c+1
			obje_final['info_cliente']=array_info_cliente

	if orden_comprar != "":
		array_final.append(obje_final)
#print(array_final)

#Ir a arrayan
headers = {
	'Content-Type': 'application/json', 
	'Accept':'application/json'
}

array=json.dumps(array_final)
response = requests.post(
	url='https://api-arrayan.cl/Publico/',
	data=array, headers=headers
)
print(response.text)