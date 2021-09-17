from collections import defaultdict
import sys
import csv
from getpass import getpass
from datetime import datetime as dt
from lifestore_file import lifestore_products,lifestore_sales,lifestore_searches

"""
This is the LifeStore_SalesList data:

lifestore_searches = [id_search, id product]
lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
lifestore_products = [id_product, name, price, category, stock]
"""
# Primero creamos un diccionario con el nombre, el stock y el precio.
# en este diccionario guardaremos la informacion acumulada de cada producto
# para despues ordenarla dependiendo de lo que queramos visualizar
summary = defaultdict(lambda:defaultdict(lambda:0))
for x in lifestore_products:
	summary[x[0]]['name'] = x[1]
	summary[x[0]]['stock'] = x[4]
	summary[x[0]]['price'] = x[2]
	summary[x[0]]['category'] = x[3]

# El diccionario que acabamos de crear lo utilizamos para guardar las 
# ventas[num_opinions], el acumulado de las reseñas del producto[average]
# y el numero de refunds totales por cada producto
for x in lifestore_sales:
	summary[x[1]]['average'] += x[2]
	summary[x[1]]['num_opinions'] += 1
	summary[x[1]]['num_refunds'] += x[4] 

#Sobre los datos ya almacenados en el diccionario calculamos el promedio de
# calificacion de las reseñas del producto [average] (no lo calculamos antes pq
# no teniamos el numero total de opiniones/ventas) y el dinero acumulado
# de sus ventas [profits] (sin contar los refunds, pq ese no fue dinero que ingresó)
for x in summary:
	if summary[x]['num_opinions'] > 0: 
		summary[x]['average'] = summary[x]['average'] / summary[x]['num_opinions']
		summary[x]['profits'] = summary[x]['num_opinions']*summary[x]['price'] - summary[x]['num_refunds']*summary[x]['price']

#calculamos las busquedas totales realizadas por cada producto
for x in lifestore_searches: 
	summary[x[1]]['buscado'] +=1

# esta funcion ordena el diccionario 'summary' basado en
# el numero de ventas [num_opinions]que tuvo cada producto
# y la muestra en consola
def list_sales():
	total_scores_by_product = sorted(summary.items(),key=lambda x: x[1]['num_opinions'] )
	print("\n{:*^150}".format(" MAS VENDIDOS "))
	print("\n{:^10}{:^40}{:^20}{:^10}{:^10}{:^10}{:^15}{:^20}\n".format(
		"ID",
		"PRODUCTO",
		"CATEGORIA",
		"SCORE",
		"VENDIDOS",
		"DEVUELTOS",
		"VECES BUSCADO",
		"INGRESOS GENERADOS")
	)
	for x in total_scores_by_product:
		print("{:^10}{:<.35}{:>20}{:10.1f}{:10}{:10}{:15}{:^20}".format(
			x[0],
			lifestore_products[x[0]-1][1],
			x[1]['category'],
			x[1]['average'],
			x[1]['num_opinions'],
			x[1]['num_refunds'],
			x[1]['buscado'],
			x[1]['profits']
		))
def list_sales_profits():
	total_scores_by_product = sorted(summary.items(),key=lambda x: x[1]['profits'] )
	print("\n{:*^150}".format(" MAS INGRESOS "))
	print("\n{:^10}{:^40}{:^20}{:^10}{:^10}{:^10}{:^15}{:^20}\n".format(
		"ID",
		"PRODUCTO",
		"CATEGORIA",
		"SCORE",
		"VENDIDOS",
		"DEVUELTOS",
		"VECES BUSCADO",
		"INGRESOS GENERADOS")
	)
	for x in total_scores_by_product:
		print("{:^10}{:<.35}{:>20}{:10.1f}{:10}{:10}{:15}{:^20}".format(
			x[0],
			lifestore_products[x[0]-1][1],
			x[1]['category'],
			x[1]['average'],
			x[1]['num_opinions'],
			x[1]['num_refunds'],
			x[1]['buscado'],
			x[1]['profits']
		))

# esta funcion ordena el diccionario 'summary' basado en
# el numero de busquedas[buscado] que tuvo cada producto
# y la muestra en consola
def list_searches():
	total_scores_by_product = sorted(summary.items(),key=lambda x: x[1]['buscado'] )
	print("\n{:*^150}".format(" BUSQUEDAS "))
	print("\n{:^10}{:^40}{:^20}{:^10}{:^10}{:^10}{:^15}{:^20}\n".format(
		"ID",
		"PRODUCTO",
		"CATEGORIA",
		"SCORE",
		"VENDIDOS",
		"DEVUELTOS",
		"VECES BUSCADO",
		"INGRESOS GENERADOS")
	)
	for x in total_scores_by_product:
		print("{:^10}{:<.35}{:>20}{:10.1f}{:10}{:10}{:15}{:^20}".format(
			x[0],
			lifestore_products[x[0]-1][1],
			x[1]['category'],
			x[1]['average'],
			x[1]['num_opinions'],
			x[1]['num_refunds'],
			x[1]['buscado'],
			x[1]['profits']
		))

# esta funcion ordena el diccionario 'summary' basado en
# el promedio total de puntaje en la reseña [average] que tuvo cada producto
# y la muestra en consola

def list_best_scores():
	total_scores_by_product = sorted(summary.items(),key=lambda x: x[1]['average'])
	#print(total_scores_by_product)
	print("\n{:*^150}".format(" MEJORES RESEÑAS "))
	print("\n{:^10}{:^40}{:^15}{:^10}{:^10}\n".format("ID","PRODUCTO","SCORE","VENDIDOS","DEVUELTOS"))
	for x in total_scores_by_product:
		print("{:^10}{:<.35}{:15.1f}{:10}{:10}".format(
			x[0],
			lifestore_products[x[0]-1][1],
			x[1]['average'],
			x[1]['num_opinions'],
			x[1]['num_refunds']
		))

# esta funcion calcula el total de ventas por año y mes
# y los muestra por en consola 
def sales_by_periods():
	#definiciones para conocer el mes dado su numero
	meses = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",
			 5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",
			 9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}

	#convierte la fecha de cada venta en 'lifestore_sales' a objeto strptime
	for i,x in enumerate(lifestore_sales,0):
		lifestore_sales[i][3]= dt.strptime(lifestore_sales[i][3],"%d/%m/%Y")
	#ordena 'lifestores_sales' por fecha de venta mas vieja a mas reciente 
	sales = sorted(lifestore_sales,key=lambda x:x[3])

	#creamos un diccionario para almacenar las ventas y los ingresos por año y mes
	month_total_sales = defaultdict(lambda:defaultdict(lambda:
		{"total_ingresos":0,
		 "total_ventas":0,
		 "productos_vendidos": defaultdict(lambda:0)}))

	for x in sales:
		month_total_sales[x[3].year][x[3].month]["total_ingresos"] += lifestore_products[x[1]-1][2]
		month_total_sales[x[3].year][x[3].month]["total_ventas"] += 1
		month_total_sales[x[3].year][x[3].month]["productos_vendidos"][x[1]] += 1
	total_count = 0 # variable para almacenar el acumulado de los meses por año
	#imprimimos los datos calculados de forma ordenada
	for years in month_total_sales:
		print("\n┌ Año: {}\n│".format(years))
		#print("│{:^14} {:^13} {:^9}\n│".format("MES","INGRESOS","VENTAS"))
		for month in month_total_sales[years]:
			print("├─  {:<13} Ingresos: ${:<12} Ventas realizadas: {:^8}".format(
				meses[month],
				month_total_sales[years][month]["total_ingresos"],
				month_total_sales[years][month]["total_ventas"])
			)
			mas_vendidos = sorted(month_total_sales[years][month]["productos_vendidos"].items(),key=lambda x:x[1],reverse=True)
			print("│\n│    mas vendidos:")
			for idx,num in mas_vendidos[0:5]:
				print("│    {:<4} {:.28}{:8}".format(
					idx,
					lifestore_products[idx-1][1],
					num
				))
			print("│")
			total_count += month_total_sales[years][month]["total_ingresos"]
		print("└ Total: ${}".format(total_count))


if __name__ == "__main__":
	#if getpass() != "emtech1234":
	#	print("Password incorrecta")
	#	sys.exit()
	#para mostrar algo de ayuda al ejecutar el programa
	if(len(sys.argv) < 2):
		print("\nUso del programa:")
		print("  \npy name.py <tipo de reporte> \n\n")
		print("posibles valores para <tipo de reporte>: \n")
		print("{:20} {}".format("ventas","lista el total de productos VENDIDOS de menor a mayor numero de ventas"))
		print("{:20} {}".format("ventas_mas_ingresos","lista los productos por ingresos generados de menor a mayor "))
		print("{:20} {}".format("busquedas","lista los productos BUSCADOS de menor a mayor numero de busquedas"))
		print("{:20} {}".format("best","lista los productos con mejor reseña en orden ascendente"))
		print("{:20} {}".format("ventas_mes","imprime un resumen de las ventas por mes "))
		sys.exit()
	if(sys.argv[1] == "ventas"):
		list_sales()
	elif(sys.argv[1] == "ventas_mas_ingresos"):
		list_sales_profits()
	elif(sys.argv[1] == "busquedas"):
		list_searches()
	elif(sys.argv[1] == "best"):
		list_best_scores()
	elif(sys.argv[1] == "ventas_mes"):
		sales_by_periods()