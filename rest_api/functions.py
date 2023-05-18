import vk
import traceback
import time
import datetime

def getGroupsWithMutual(api_key, api_version, user_id, substring):
    """
    Функция для рассчета 1 метода (по группам пользователя и друзей ищет группы по подстроке)

    input:
        api_key: string
        api_version: float
        user_id: int
        substring: string

    output:
        string of group names
    """
    api = vk.session.API(api_key)
    my_friends = api.friends.get(user_id=user_id, v=api_version)['items']

    my_groups = [x['name'] for x in api.groups.get(user_id=user_id, extended=1,v=api_version)['items']]

    all_groups = [my_groups]
    count = 0
    for friend in my_friends:
        # просто чтобы видно было на каком этапе парсинг
        print(f'{count}/{len(my_friends)}')
        count+=1
        try:
            friend_groups = api.groups.get(user_id=friend,v=api_version)['items']
        except:
            pass
        time.sleep(0.3)
        all_groups.append(friend_groups)

    all_groups = list(set(sum(all_groups, [])))
    groups_like = [x['name'] for x in api.groups.search(q=substring, type='group', v=api_version)['items']]

    answer = list(set(all_groups) & set(groups_like))

    return str(answer)[1:-1]


def getGroupsWithoutMutual(api_key, api_version, user_id, substring):
    """
    Функция для рассчета 2 метода (по группам пользователя ищет группы по подстроке)

    input:
        api_key: string
        api_version: float
        user_id: int
        substring: string

    output:
        string of group names, parameters of query, datetime of query
    """
    api = vk.session.API(api_key)
    dt = datetime.datetime.now()

    my_groups = [x['name'] for x in api.groups.get(user_id=user_id, extended=1,v=api_version)['items']]
    groups_like = [x['name'] for x in api.groups.search(q=substring, type='group', v=api_version)['items']]
    answer = list(set(my_groups) & set(groups_like))

    parameters = {'user_id':user_id, 'substring': substring, 'groups_search_type': 'group', 'api_version' :api_version}
    return str(answer)[1:-1], parameters, dt
