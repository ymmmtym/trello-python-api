from trello import TrelloClient
import os


client = TrelloClient(
    api_key = os.environ['TRELLO_API_KEY'],
    token   = os.environ['TRELLO_TOKEN']
)

cwd = os.getcwd()
boards = client.list_boards()

def backup_md(archived=False):
    for board in boards:
        os.makedirs(board.name,exist_ok=True)
        os.chdir(board.name)
        board = client.get_board(board.id)
        lists = board.all_lists()
        for target_list in lists:
            if target_list.closed is archived:
                os.makedirs(target_list.name,exist_ok=True)
                os.chdir(target_list.name)
                cards = board.get_list(target_list.id).list_cards()
                for card in cards:
                    path = card.name + '.md'
                    with open(path, mode='w') as f:
                        f.write(card.desc)
                os.chdir('../')
        os.chdir('../')


def delete_archived_lists():
    tmp_board = client.add_board("tmp")
    for board in boards:
        board = client.get_board(board.id)
        lists = board.all_lists()
        for target_list in lists:
            if target_list.closed is True:
                client.fetch_json(
                    "/lists/{list_id}/idBoard".format(list_id=target_list.id),
                    http_method="PUT",
                    post_args={'value': tmp_board.id}
                )

    client.fetch_json(
        "/boards/{board_id}".format(board_id=tmp_board.id),
        http_method="DELETE"
    )

if __name__ == '__main__':
    backup_md(archived=False)
    delete_archived_lists()