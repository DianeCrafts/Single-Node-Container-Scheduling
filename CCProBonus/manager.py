import threading
import time
import os
import random
import string



task = []
container = 1
password = 'xxx'
def conRunner(data ):
    global container
    out = get_random_string(5,'.txt')

    if(data[0].endswith('.py')):
        p = os.system('pipreqs ' + data[1])
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp '+ data[1] + data[0] +' bonus1:/'))
        p = os.system('pipreqs ' + data[1])
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp requirements.txt bonus1:/'))
        time.sleep(0.3)
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "pip install -r requirements.txt"'))
        time.sleep(0.3)
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "python3 '+data[0]+' >>'+data[0]+out+'"'))
        time.sleep(0.3)
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp bonus1:/'+data[0]+out+ ' ' + data[2]))
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "rm '+data[0]+' "'))
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "rm requirements.txt"'))
        time.sleep(0.3)
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "rm '+data[0]+out+'"'))
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo rm requirements.txt'))
       
    if(data[0].endswith('.cpp')):
        program = get_random_string(5 ,'.out')
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp '+ data[1] + data[0] +' bonus1:/'))
        time.sleep(0.3)
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "g++ -o '+  program +' '+data[0]+'"'))
        time.sleep(0.3)
        p = os.system('sudo docker exec  bonus1 sh -c "./'+  program +'>>'+data[0]+out +'"')
        time.sleep(0.3)
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp bonus1:/'+data[0]+out+ ' ' + data[2]))
        time.sleep(0.3)
        p=os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "rm '+data[0]+'"'))
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "rm '+program+'"'))
        p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  bonus1 sh -c "rm '+data[0]+out+'"'))

    container = 1





def get_task(name):
    while 1:

        user_input= input("enter input: ")
        input_list = []
        parseInput(user_input , input_list)
        for i in range(len(input_list)):
            req = input_list[i].split(',')

            task.append(req)
        print(task)



def assign_task(name):
    global container
    while 1:
        if( container == 1 and len(task) > 0):
            container = 0
            job = task.pop()
            print("task " + job[0]+" assigned to container \n")
            conRunner(job)
               
            
        time.sleep(1)



def parseInput(input , a_list):
    a=input 
    # "‫‪{<test2.cpp,~/CCProBonus/>,<test.cpp,~/CCProBonus/>,<p.py,~/CCProBonus/>,<~/CCProBonus/>}"
    # "‫‪{<test2.cpp,~/CCProBonus/>,<~/CCProBonus/>}"
    a = a.replace('{' , '')
    a = a.replace('}' , '')
    a = a.replace(">,<", "><")
    b = a.split('><')
    b[0] = b[0][1:]
    b[-1] = b[-1][:-1]
    # a_list = []
    os.system('mkdir -p ' + b[len(b) -1])
    for i in range(len(b) - 1):
        x = b[i] + ',' + b[len(b) -1]
        a_list.append(x)

    print(a_list)


def get_random_string(length , extension):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    result_str = result_str +extension 
    return result_str



if __name__ == "__main__":
    x = threading.Thread(target=get_task, args=(1,))
    x.start()
    y = threading.Thread(target=assign_task, args=(1,))
    y.start()
