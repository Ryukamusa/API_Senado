#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:12:35 2017

@author: helio
"""
#==============================================================================
#==============================================================================
# # 1a
#==============================================================================
#==============================================================================
class Plenario(object):
    def __init__(self):
        self.numero_senadores=0 #inicia o número de senadores no plenário (começa vazio)
        self.senadores=[] #inicia a lista de senadores no plenário (começa vazio)
    def adicionar(self,nome):
        '''Adiciona novo senador ao plenário'''
        self.numero_senadores+=1 #aumenta o número de senadores no plenário
        self.senadores.append(nome) #coloca o senador de nome "nome" na lista de senadores em exercício no plenário
    def senadores_nomes(self):
        ret=[sen.nome for sen in self.senadores]
        return ret



class Parlamentar(object):
    def __init__(self,lista,plenario):
        #### Parlamentar ID
        id_dic,mand_dic,legis,titular,suplentes,exercicio=lista
        self.codigo=id_dic['codigo'] # code
        self.nome=id_dic['nome'] # nome
        self.nome_completo=id_dic['nome_completo'] # nome completo
        self.sexo=id_dic['sexo'] # sexo
        self.forma_tratamento=id_dic['forma'] # forma tratamento
        self.foto=id_dic['foto'] # foto url
        self.pagina=id_dic['pagina'] # pagina pessoal
        self.email=id_dic['email'] # email pessoal
        self.partido=id_dic['partido'] # partido de filiacao
        self.UF=id_dic['uf'] # UF de partido
        plenario.adicionar(self)
        #### Mandato parlamentar
        self.mandato=Mandato(mand_dic,legis,titular,suplentes,exercicio)


class Mandato(object):
    def __init__(self,mand_dic,legis,titl,supl,exerc):
        self.codigo=mand_dic['codigo'] # codigo do mandato
        self.UF=mand_dic['uf'] # UF do mandato
            # legislatura 1
        self.legislatura_1=Legislatura(legis,k='1')
        self.legislatura_2=Legislatura(legis,k='2')
        self.suplente_1=Suplente(supl,k='1')
        self.suplente_2=Suplente(supl,k='2')
        self.titular=Titular(titl)
        self.exercicios=Exercicios(exerc)

class Legislatura(object):
    def __init__(self,legis,k='1'):
        self.numero=legis['leg%s'%k]['n'] # 1a legislatura
        self.inicio=legis['leg%s'%k]['inicio'] # 1a legislatura
        self.fim=legis['leg%s'%k]['fim'] # 1a legislatura

class Titular(object):
    def __init__(self,titl,k='1'):
        self.codigo=titl['codigo'] # 1o titular
        self.nome=titl['nome'] # 1o titular
        self.participacao=titl['particip'] # 1o titular

class Suplente(object):
        def __init__(self,supl,k='1'):
            self.codigo=supl['sup%s'%k]['codigo'] # 1o suplente
            self.nome=supl['sup%s'%k]['nome'] # 1o suplente
            self.participacao=supl['sup%s'%k]['particip'] # 1o suplente

class Exercicios(object):
    def __init__(self,exerc):
        self.exercicios=exerc

#==============================================================================
#==============================================================================
# # 1b
#==============================================================================
#==============================================================================


import requests
from xml.etree import ElementTree

def getp(lst,k='Parlam'):
    for i in range(len(lst)):
        a=lst[i]
        if k in a.tag:
            return i
def get_ID(parlamentar):
    ids=parlamentar.find('IdentificacaoParlamentar')
    cod=ids.find('CodigoParlamentar').text
    nome=ids.find('NomeParlamentar').text
    nome_comp=ids.find('NomeCompletoParlamentar').text
    sexo=ids.find('SexoParlamentar').text
    forma=ids.find('FormaTratamento').text
    foto=ids.find('UrlFotoParlamentar').text
    pagina=ids.find('UrlPaginaParlamentar').text
    email=ids.find('EmailParlamentar').text
    uf=ids.find('UfParlamentar').text
    partido=ids.find('SiglaPartidoParlamentar').text
    id_dic={'codigo':cod,'nome':nome,'nome_completo':nome_comp,'sexo':sexo,
            'forma':forma,'foto':foto,'pagina':pagina,'email':email,'uf':uf,
            'partido':partido}
    return id_dic

def get_mandato(parlamentar):
    ids=parlamentar.find('Mandato')
    cod=ids.find('CodigoMandato').text
    uf=ids.find('UfParlamentar').text
    mand_dic={'codigo':cod,'uf':uf}
    return mand_dic

def get_legislatura(parlamentar):
    id1=parlamentar.find('Mandato').find('PrimeiraLegislaturaDoMandato')
    id2=parlamentar.find('Mandato').find('SegundaLegislaturaDoMandato')
    n1,in1,fin1=id1.find('NumeroLegislatura').text,id1.find('DataInicio').text,id1.find('DataFim').text
    n2,in2,fin2=id2.find('NumeroLegislatura').text,id2.find('DataInicio').text,id2.find('DataFim').text
    legis={'leg1':{'n':n1,'inicio':in1,'fim':fin1},
           'leg2':{'n':n2,'inicio':in2,'fim':fin2}}
    return legis

def get_titular(parlamentar):
    try:
        ids=parlamentar.find('Mandato').find('Titular')
        code,nome,part=ids.find('CodigoParlamentar').text,ids.find('NomeParlamentar').text,ids.find('DescricaoParticipacao').text
        tit={'codigo':code,'nome':nome,'particip':part}
    except:
        tit={'codigo':None,'nome':None,'particip':None}
    return tit

def get_suplentes(parlamentar):
    suplentes={'sup1':{'codigo':None,'nome':None,'particip':None},
               'sup2':{'codigo':None,'nome':None,'particip':None}}
    for ids in parlamentar.find('Mandato').find('Suplentes'):
        code,nome,part=ids.find('CodigoParlamentar').text,ids.find('NomeParlamentar').text,ids.find('DescricaoParticipacao').text
        sup={'codigo':code,'nome':nome,'particip':part}
        suplentes['sup%i'%int(part[0])]=sup
    return suplentes

def get_exercicio(parlamentar):
    ids=parlamentar.find('Mandato').find('Exercicios')
    exercicios={}
    for n,ex in enumerate(ids):
        exr={}
        for chl in ex:
            exr[chl.tag]=chl.text
        exercicios[ex.tag+"%i"%(n+1)]=exr
    return exercicios



def getParlamentarInfo(parlamentar):
    id_dic=get_ID(parlamentar)
    mand_dic=get_mandato(parlamentar)
    legis=get_legislatura(parlamentar)
    titular=get_titular(parlamentar)
    suplentes=get_suplentes(parlamentar)
    exercicio=get_exercicio(parlamentar)
    return [id_dic,mand_dic,legis,titular,suplentes,exercicio]


url = "http://legis.senado.gov.br/dadosabertos/senador/lista/atual"

response = requests.get(url)

tree = ElementTree.fromstring(response.content)
chld=tree.getchildren()

pos=getp(chld,k='Parl')
parlams=tree[pos].findall('Parlamentar')

plenario=Plenario()
for i in range(len(parlams)):
    infos_list=getParlamentarInfo(parlams[i])
    _=Parlamentar(infos_list,plenario)
