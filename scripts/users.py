import uuid

from django.contrib.auth import get_user_model


def set_name():
    users = get_user_model().objects.filter(first_name__exact='')
    num = users.count()

    if num > 0:
        print(f'{num} users to process...')

        for u in users:
            u.first_name = 'User'
            u.last_name = str(uuid.uuid4())[:5]
            u.save()
            print(f'User {u.username} was updated')

        print('Process completed...')
