import typing as tp
from collections import defaultdict

import community as community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from vkapi.friends import get_friends, get_mutual


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """
    graph = set()
    if friends is None:
        target_uids = get_friends(user_id=user_id).items
        active_users = [user["id"] for user in target_uids if
                        user.get("deactivated") is None and not user.get("is_closed")]
        for i in target_uids:
            graph.add((user_id, i["id"]))
        mutual_friends = get_mutual(source_uid=user_id, target_uids=active_users)
        for i in mutual_friends:
            for j in i["common_friends"]:
                graph.add((i["id"], j))
    else:
        mutual_friends = get_mutual(source_uid=user_id, target_uids=friends)
        for i in mutual_friends:
            for j in i["common_friends"]:
                if i["id"] != None and j != None:
                    graph.add((i["id"], j))
    return list(graph)






def plot_ego_network(net: tp.List[tp.Tuple[int, int]], with_labels: bool = True) -> None:
    """
    Отрисовать эгоцентричный граф друзей.

    :param net: Граф, созданный с помощью функции ego_network.
    :param with_labels: Наносить или нет на граф имена пользователей.
    """
    graph = nx.Graph()
    graph.add_edges_from(net)

    # put your code here

    layout = nx.spring_layout(graph)
    nx.draw(graph, layout, node_size=10, node_color="black", alpha=0.5)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    partition = community_louvain.best_partition(graph)
    nx.draw(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8)
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)
    partition = community_louvain.best_partition(graph)
    for uid, cluster in partition.items():
        communities[cluster].append(uid)
    return communities


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],
    friends: tp.List[tp.Dict[str, tp.Any]],
    fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])  # type: ignore
                    break
    return pd.DataFrame(data=data, columns=["cluster"] + fields)
