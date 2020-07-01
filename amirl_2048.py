# Ran 0545402820 
import random
from copy import copy, deepcopy


win_value = 2048


class Game2048:

    def __init__(self, board_size=4):
        self.size = board_size
        self.free_spaces = pow(self.size, 2)
        self.matrix = [[0 for x in range(self.size)] for y in range(self.size)]
        self.next_step_matrix = None
        self.open_cells_list = [(x, y) for x in range(self.size) for y in range(self.size)]
        self.tiles = [2] * 90 + [4] * 10
        self.game_status = True
        self.is_win = False
        self.set_new_tiles()
        self.set_new_tiles()

    def set_new_tiles(self):
        """"""
        if self.open_cells_list:
            value = random.choice(self.tiles)
            selected_new_tail = random.randrange(len(self.open_cells_list)-1)
            selected_new_tail_value = self.open_cells_list[selected_new_tail]
            print(f'selected {selected_new_tail_value[0]} {selected_new_tail_value[1]} : tiles value {value}')
            del self.open_cells_list[selected_new_tail]
            self.matrix[selected_new_tail_value[0]][selected_new_tail_value[1]] = value
            self.free_spaces -= 1
        # no open cells to allocate set game status to False(lose)
        else:
            self.game_status = False

    def draw_board(self):
        for i in range(self.size):
            print(self.matrix[i])

    def make_move(self, direction):
        """
        :param direction: ch for each direction - u,d,l,r
        :return: bool - if valid True else False, update_board if valid
        """
        self.next_step_matrix = deepcopy(self.matrix)
        is_valid_move = self.push_matrix(direction)
        if is_valid_move:
            self.matrix = deepcopy(self.next_step_matrix)
            self.draw_board()
            self.open_cells_list = [(x, y) for x in range(self.size) for y in range(self.size) if not self.matrix[x][y]]
            return True
        return False

    def push_matrix(self, direction):
        matrix_changed = False

        for x in range(self.size):
            if direction in ["r", "l"]:
                line_to_change = self.matrix[x]
                new_line = [num for num in line_to_change if num]

                # calc merge
                ret_list = self.make_merge(new_line, direction)

                if line_to_change != ret_list:
                    matrix_changed = True
                    self.next_step_matrix[x] = ret_list

            if direction in ["d", "u"]:
                col_to_change = self.get_col(x)
                new_line = [num for num in col_to_change if num]

                # calc merge
                ret_list = self.make_merge(new_line, direction)

                if col_to_change != ret_list:
                    matrix_changed = True
                    self.update_col(x, ret_list)
        return matrix_changed

    def get_col(self, idx_y):
        return [self.matrix[x][idx_y] for x in range(self.size)]

    def update_col(self, idx_y, col):
        for x in range(self.size):
            self.next_step_matrix[x][idx_y] = col[x]

    def make_merge(self, mrg_lst, direction):
        ret_list = []
        i = 0
        while i < len(mrg_lst):
            if i+1 < len(mrg_lst)  and mrg_lst[i] == mrg_lst[i+1]:
                product = mrg_lst[i] * 2
                if product == win_value:
                    self.is_win = True
                ret_list.append(product)
                i += 2
            else:
                ret_list.append(mrg_lst[i])
                i += 1
        current_len = len(ret_list)

        if direction in ["u", "l"]:
            ret_list = ret_list + [0] * (self.size - current_len)
        else:
            ret_list = [0] * (self.size - current_len) + ret_list
        return ret_list


my_game = Game2048()
my_game.draw_board()

while not my_game.is_win:
    chosen_dir = user_dir = input("side:")
    is_valid = my_game.make_move(user_dir)
    while not is_valid:
        chosen_dir =user_dir = input("invalid selection please try again:")
        is_valid = my_game.make_move(user_dir)
    if my_game.is_win:
        print(" won!!")
        break
    my_game.set_new_tiles()
    my_game.draw_board()
    if not my_game.game_status:
        print("lose!!")





