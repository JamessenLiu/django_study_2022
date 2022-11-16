from apps.tasks.task import app
from apps.users.models import Users
import csv
import time


@app.task
def export_users():
    time.sleep(10)
    print('------------export_users------------')
    users = Users.objects.all().values()
    with open('user.csv', 'w', encoding='utf-8') as fp:
        user_file = csv.DictWriter(fp, fieldnames=['first_name', 'last_name', 'email'])
        user_file.writeheader()
        for user in users:
            user_file.writerow({
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "email": user['email']
            })
    return
