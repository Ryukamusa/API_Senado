from collections import OrderedDict
import subprocess

class Project(object):
    opinion=OrderedDict({'Favoravel':0,'Nao-favoravel':0,'Indiferente':0})
    def __init__(self,name,status):
        self.name=name
        self.status=status
        self.coments={}
        self.coment_number=0
        self.followers=[]
    def opiniao(self,opin):
        self.opinion[opin]+=1
    def coment(self,person,coment):
        self.coments[person]=coment
        self.coment_number+=1
    def change_status(self,new_status):
        time=subprocess.check_output('date').split(' ')
        self.status=new_status
        for fl in self.followers:
            fl.notification_list.append(self.name+' changed status in %s %s'%(time[2],time[1]))

class User(object):

    def __init__(self,name,idade,sexo,proj_list=[]):
        self.name=name
        self.idade=idade
        self.sexo=sexo
        self.following=[]
        self.notification_list=[]
        self.friends_request=[]
        self.friends=[]
        if proj_list!=[]:
            self.coments=dict(zip(self.following, [None]*len(self.following)))
            [self.seguir(proj) for proj in proj_list]
        else:
            self.coments={}

    def comentar(self,proj,coment):
        self.coments[proj.name]=coment
        proj.coment(self.name,coment)
    def opinar(self,proj,opin):
        proj.opiniao(opin)
    def seguir(self,proj):
        proj.followers.append(self)
        self.following.append(proj.name)
        self.coments[proj.name]=None
    def new_friend(self,amigo):
        self.friends.append(amigo.name)
        amigo.friends_request.append(self.name)
    def clear_frequest(self,amigo):
        self.friends_request.remove(amigo.name)

def print_coments(proj,user):
    users=[user.name]
    [users.append(usr) for usr in user.friends]
    coment_print={}
    for coment in proj.coments.items():
        if coment[0] in users:
            coment_print[coment[0]]=coment[1]
    return coment_print










#==============================================================================
#==============================================================================
# # EXEMPLOS
#==============================================================================
#==============================================================================


proj1=Project('projeto_teste','em andamento')
proj2=Project('projeto_realizar','concluido')
proj3=Project('projeto_MariaPenha','funciona')

carlos=User("Carlos",65,"M",proj_list=[proj1])
ze=User("Ze",49,"M",proj_list=[proj1,proj2])
gina=User("Gina",23,"F",proj_list=[proj1,proj2,proj3])
ze.new_friend(carlos)
carlos.new_friend(ze)
carlos.opinar(proj1,'Favoravel')
carlos.comentar(proj1,'cena')
carlos.comentar(proj2,'nice')
proj1.change_status('enviado para a ')

print print_coments(proj1,ze)
