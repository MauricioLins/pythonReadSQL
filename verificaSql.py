import os
import datetime
import time
from variaveisIniciais import location_ini

dataDefault = str(datetime.datetime.date(datetime.datetime.now()))
dateTime    = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')

def salvaDados(user,tabela, data, tipo):
	if(tipo == 'primeiraLeitura'):
		arquivo = 'queries_resultado_' + dataDefault + '.txt'
	else:
		arquivo = 'queries_resultado_final_' + dataDefault + '.txt'

	with open(arquivo, mode='a') as file:
		linha = user + '|' + tabela + '|' + data
		if(tipo == 'primeiraLeitura'):
			file.write(linha+'\n')
		else:
			file.write(linha)

def limpaDados(user,tabela, data):
	nmTabela = tabela.strip()
	
	if(nmTabela[-2:] == r'\N'):
		nmTabela = tabela[:-2]
	if(nmTabela[-1:] == ';'):
		nmTabela = tabela[:-1]
	if(nmTabela[-1:] == ','):
		nmTabela = tabela[:-1]
	if(nmTabela[-1:] == ')'):
		nmTabela = tabela[:-1]

	if(nmTabela != '(SELECT'):
		salvaDados(user, nmTabela, data, 'limpeza')

def main():

	print('###########################################################################')
	print('INICIO DA VERIFICACAO DOs SQLs...........................' + dateTime)
	print('###########################################################################')

	with open(location_ini) as f:
		all_lines = f.readlines()
		numlin = 1
		for line in all_lines:
			vSql = line.upper()
	##########################################################################################################
	####### VERIFICA O SQL POSSUI ALGUM 'FROM' E REALIZA UM SPLIT 
	##########################################################################################################
			if(vSql.find('FROM') != -1):
				sqlSplit = vSql.split() #ATENCAO COM O SPLIT *************************************************
				for parse in range(0,len(sqlSplit)):
					if(sqlSplit[parse] == 'FROM'):
	##########################################################################################################
	################### VERIFICA SE HA MAIS DE UMA TABELA DECLARADA NO FROM
	##########################################################################################################
						if(sqlSplit[parse+1][-1:] == ','):
							for pasert in range(parse+1,len(sqlSplit)): # "loopa"da primeira tabela ate o WHERE
								if(sqlSplit[pasert] == 'WHERE'):
									break # para ao encontrar a clausula WHERE
								else:
									table = sqlSplit[pasert].strip()
									#print(numlin, '-----',table)
									salvaDados('userT', table, dataDefault,'primeiraLeitura')
						else:
							table = sqlSplit[parse+1].strip() # apenas captura a tabela do from caso acima seja falso
							#print(numlin, '-----',table)
						salvaDados('userT', table, dataDefault,'primeiraLeitura')
	##########################################################################################################
	############### VERIFICA SE HA DECLARADA A CLAUSULA JOIN E 
	##########################################################################################################
					if(sqlSplit[parse] == 'JOIN'): # caso encontre a clausula JOIN e captura a tabela definida
						table = sqlSplit[parse+1].strip()
						#print(numlin, '-----',table)
						salvaDados('userT', table, dataDefault,'primeiraLeitura')
			numlin +=1

	print('###########################################################################')
	print('FIM VERIFICACAO SQLs.....................................' + dateTime)
	print('###########################################################################')

	time.sleep(5)

	print('###########################################################################')
	print('INICIO DA LIMPEZA........................................' + dateTime)
	print('###########################################################################')

	arquivo = 'queries_resultado_' + dataDefault + '.txt'

	with open(arquivo, mode='r') as fileopen:
		linha_limpeza = fileopen.readlines()
		for linha in linha_limpeza:
			vUserLimpeza   = linha.split('|')[0]
			vTabelaLimpeza = linha.split('|')[1]
			vDataLimpeza   = linha.split('|')[2]
			#if(vTabelaLimpeza.strip())
			limpaDados(vUserLimpeza, vTabelaLimpeza, vDataLimpeza)

	print('###########################################################################')
	print('FIM DA LIMPEZA...........................................' + dateTime)
	print('###########################################################################')
	print('REMOVENDO ARQUIVO INTERMEDIARIO..........................' + dateTime)

	os.remove(arquivo)
	time.sleep(5)

	print('###########################################################################')
	print('CRIADO ARQUIVO: queries_resultado_final_' + dataDefault + '.txt')
	print('###########################################################################')

if __name__ == '__main__':main()