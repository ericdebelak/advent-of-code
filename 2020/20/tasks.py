import re
from math import prod, sqrt


def _parse_tiles(file):
    tiles = {}
    all_sides = []
    groups = file.read().split('\n\n')
    for group in groups:
        lines = group.splitlines()
        tile_id = re.findall(r'(\d+)', lines[0])[0]
        tiles[tile_id] = _find_all_sides(lines[1:])
        all_sides += tiles[tile_id]
    return tiles, all_sides


def test_find_all_sides():
    assert _find_all_sides(
        [
            '####...##.',
            '#..##.#..#',
            '##.#..#.#.',
            '.###.####.',
            '..###.####',
            '.##....##.',
            '.#...####.',
            '#.##.####.',
            '####..#...',
            '.....##...'
        ]
    ) == [
        '####...##.',
        '.##...####',
        '.....##...',
        '...##.....',
        '###....##.',
        '.##....###',
        '.#..#.....',
        '.....#..#.'
    ]


def _find_all_sides(tile):
    sides = []
    # add top and bottom rows and their reverses
    sides.append(tile[0])
    sides.append(tile[0][::-1])
    sides.append(tile[len(tile) - 1])
    sides.append(tile[len(tile) - 1][::-1])
    # get left and ride sides
    left_side = ''
    right_side = ''
    for row in tile:
        left_side += row[0]
        right_side += row[len(row) - 1]
    # append the left and right sides
    sides.append(left_side)
    sides.append(left_side[::-1])
    sides.append(right_side)
    sides.append(right_side[::-1])
    return sides


def test_find_matches():
    tile = [
        '####...##.',
        '.##...####',
        '.....##...',
        '...##.....',
        '##########',
    ]
    all_sides = [
        '####...##.',
        '.##...####',
        '.....##...',
        '...##.....',
        '###....##.',
        '.##....###',
        '.#..#.....',
        '.....#..#.'
    ]
    assert _find_matches(tile, all_sides) == 4


def _find_matches(tile, all_sides):
    return len([i for i in all_sides if i in tile])


def test_task_one():
    assert task_one('test-data.txt') == 20899048083289
    assert task_one('real-data.txt') == 15006909892229


def task_one(filename):
    with open(filename, 'r') as file:
        tiles, all_sides = _parse_tiles(file)
        corners = []
        for tile_id, tile in tiles.items():
            # corners with have all their side possibilities match, plus 2 and their reverses, so 12 matches
            if _find_matches(tile, all_sides) == 12:
                corners.append(int(tile_id))
        return prod(corners)


def _rotate_90_deg_clockwise(tile):
    return list(''.join(x[::-1]) for x in zip(*tile))


def _flip(tile):
    return list(reversed(tile.copy()))


def _build_tile_transformations(tile):
    tile90 = _rotate_90_deg_clockwise(tile)
    tile180 = _rotate_90_deg_clockwise(tile90)
    tile270 = _rotate_90_deg_clockwise(tile180)
    return [tile, tile90, tile180, tile270, _flip(tile), _flip(tile90), _flip(tile180), _flip(tile270)]


def _assemble_image(tile_transformations, side_length):
    image_matrix = [[(0, 0)] * side_length for _ in range(side_length)]
    remaining_tiles = set(tile_transformations.keys())

    def _assemble_tiles(row_column):
        if row_column == side_length * side_length:
            return True
        row, column = row_column // side_length, row_column % side_length
        for tile_id in list(remaining_tiles):
            for i, transformation in enumerate(tile_transformations[tile_id]):
                up_matches = left_matches = True
                if row > 0:
                    up_tile_id, up_transformation = image_matrix[row - 1][column]
                    up_tile = tile_transformations[up_tile_id][up_transformation]
                    up_matches = all(transformation[0][i] == up_tile[9][i] for i in range(10))
                if column > 0:
                    left_tile_id, left_transformation = image_matrix[row][column - 1]
                    left_tile = tile_transformations[left_tile_id][left_transformation]
                    left_matches = all(transformation[i][0] == left_tile[i][9] for i in range(10))
                if up_matches and left_matches:
                    image_matrix[row][column] = (tile_id, i)
                    # remove the tile from remaining and keep running it
                    remaining_tiles.remove(tile_id)
                    if _assemble_tiles(row_column + 1):
                        return True
                    # if the whole image doesn't match, add back the tiles and try again
                    remaining_tiles.add(tile_id)
        return False

    _assemble_tiles(0)

    return image_matrix


def _parse_tiles_two(file):
    tiles, tile_id = {}, 0
    for group in file.read().split('\n\n'):
        lines = group.splitlines()
        tile_id = re.findall(r'(\d+)', lines[0])[0]
        tiles[int(tile_id)] = lines[1:]
    return tiles


def test_task_two():
    assert task_two('test-data.txt') == 273
    assert task_two('real-data.txt') == 2190


def task_two(filename):
    with open(filename, 'r') as file:
        tiles = _parse_tiles_two(file)
        # build every possible tile orientation
        tile_transformations = {tile_id: _build_tile_transformations(tile) for tile_id, tile in tiles.items()}
        # figure out the size of the image
        side_length = int(sqrt(len(tile_transformations)))
        # build the image with the tile id and transformation index
        tile_matrix = _assemble_image(tile_transformations, side_length)
        # get position of monster
        monster_pattern = [
            '                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   '
        ]
        monster_indexes = [
            (row, column)
            for row in range(3)  # monster number of rows
            for column in range(20)  # monster length of columns
            if monster_pattern[row][column] == '#'
        ]

        # build a default image of all periods so we have all the indexes
        image = [['.'] * (side_length * 8) for _ in range(side_length * 8)]
        # update the default image with the actual image from the tiles
        for row in range(side_length):
            for column in range(side_length):
                tile_id, transformation_index = tile_matrix[row][column]
                tile = tile_transformations[tile_id][transformation_index]
                for i in range(1, 9):
                    for j in range(1, 9):
                        image[8 * row + i - 1][8 * column + j - 1] = tile[i][j]

        # go through different image orientations to find the monsters
        for image in _build_tile_transformations(image):
            monster = 0
            for row in range(len(image) - 3):  # the monster has a height of 3, so we need to offset for this
                for column in range(len(image) - 20):  # the monster has a length of 20, so we need to offset for this
                    if all(image[row + mr][column + mc] == '#' for mr, mc in monster_indexes):
                        monster += 1
            if monster > 0:
                total = sum(row.count('#') for row in image)
                return total - monster * len(monster_indexes)
