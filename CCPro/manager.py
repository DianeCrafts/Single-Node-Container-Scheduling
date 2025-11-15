import threading
import time
import os
import random
import string



task = []
password = 'xxxx'

def firstCon( i , data ):
    out = get_random_string(5 , data[0])
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp ' +data[1] +' container1:/'))
    time.sleep(0.5)
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  container1 sh -c "python3 python.py '+ data[0] + ' ' + data[1] + ' '+ out + '"'))
    time.sleep(0.5)
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp container1:/' +out +' ' +data[2]))
    containers[i] = 1


def secondCon( i, data):
    out = get_random_string(5, data[0])
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp ' +data[1] +' container2:/'))
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  container2 sh -c "python3 python.py '+ data[0] + ' ' + data[1] + ' '+ out + '"'))
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp container2:/' +out +' ' +data[2]))
    containers[i] = 1


def thirdCon( i, data):
    out = get_random_string(5, data[0])
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp ' +data[1] +' container3:/'))
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker exec  container3 sh -c "python3 python.py '+ data[0] + ' ' + data[1] + ' '+ out + '"'))
    p = os.system('echo %s|sudo -S %s' % (password, 'sudo docker cp container3:/' +out +' ' +data[2]))
    containers[i] = 1


containers = [1 , 1 , 1]

def get_task(name):
    while 1:

        user_input= input("enter input: ")
        input_list = []
        task.append('*')
        parseInput(user_input , input_list)
        for i in range(len(input_list)):
            req = input_list[i].split(',')

            task.append(req)
        
        print(task)



def assign_task(name):

    while 1:

        for i in range(0 , 3):
            if(containers[i] == 1 and len(task) > 0):
                containers[i] = 0
                job = task.pop()
                if(job == '*'):
                    print('done!!!!!!!')
                else:
                    if (i == 0):
                        m = threading.Thread(target= firstCon , args = (i, job))
                        m.start()
                    if (i == 1):
                        n =threading.Thread(target= secondCon , args = (i, job))
                        n.start()
                    if (i == 2):
                        k = threading.Thread(target= thirdCon , args = (i, job))
                        k.start()
                    print("task " + job[0]+" assigned to container " + str(i+1))
        time.sleep(0.5)



def parseInput(input , a_list):
    a=input 
    # "{<min,input.txt>,<avg,input2.txt>,<max,input2.txt>,<avg,input.txt>,<sort,input2.txt>,<wc,input.txt>,<max,input2.txt><~/CCPro/newFolder>}"
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


def get_random_string(length,method):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    result_str = method+result_str + '.txt'
    return result_str



if __name__ == "__main__":
    x = threading.Thread(target=get_task, args=(1,))
    x.start()
    y = threading.Thread(target=assign_task, args=(1,))
    y.start()
