import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id=user_id, fields=["bdate"])
    print(friends)
    years = []
    for i in friends.items:
        try:
            years.append(i['bdate'])
        except:
            pass
    years = [i[-4:] for i in years]
    years = [i.replace(".", "") for i in years]
    years = [i for i in years if len(i) == 4]
    ages = [2024 - int(i) for i in years]
    ages = sorted(ages)
    return ages[len(ages) // 2] if len(ages) > 0 else None
