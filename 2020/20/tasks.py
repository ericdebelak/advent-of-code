import re
from math import prod


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
            if _find_matches(tile, all_sides) == 12:
                corners.append(int(tile_id))
        return prod(corners)
