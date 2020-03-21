import requests
import sys
import datetime
import os

folderPath = os.getcwd() + '/tasks'
today = datetime.datetime.today()
completedTasks = []
remainingTasks = []


def get_json(url):
    try:
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            return response.json()
        else:
            raise Exception("Server returned error (url={0}): {1}".format(url, status))

    except Exception as err:
        print('Getting json from server error: {0}'.format(err))
        sys.exit()


def create_directory(folder):
    if os.path.exists(folder):
        pass
    else:
        try:
            return os.mkdir(folder)
        except OSError:
            print("Создать директорию %s не удалось" % folder)
        else:
            print("Успешно создана директория %s " % folder)


todoList = get_json('https://json.medrating.org/todos')
users = get_json('https://json.medrating.org/users')

create_directory(folderPath)


for task in todoList:
    if task['completed']:
        completedTasks.append(task)
    else:
        remainingTasks.append(task)


for user in users:
    userCompletedTasks = [x['title'] for x in completedTasks if x['userId'] == user['id']]
    userRemainingTasks = [x['title'] for x in remainingTasks if x['userId'] == user['id']]
    company = user['company']
    filename = folderPath + "/%s.txt" % user['username']
    if os.path.isfile(filename):
        createTime = os.path.getctime(filename)
        timeOfCreated = datetime.datetime.fromtimestamp(createTime).strftime("%d.%m.%YT%H.%M")
        oldFile = filename
        newFile = os.getcwd() + "/tasks" + "/%s" % user['username'] + "_" + timeOfCreated + ".txt"
        os.rename(oldFile, newFile)
    with open(filename, 'a') as file:
        file.write(user['name'] + "<" + user['email'] + ">" + " " +
                   today.strftime("%d.%m.%Y %H:%M") + "\n" + company['name'] + "\n\n" + "Завершенные задачи:" + "\n")
        for task in userCompletedTasks:
            if len(task) > 50:
                task = task[0:50] + "..."
            file.write(task + "\n")
        file.write("\nОставшиеся задачи:\n")
        for task in userRemainingTasks:
            if len(task) > 50:
                task = task[0:50] + "..."
            file.write(task + "\n")
