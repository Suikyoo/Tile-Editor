def set_tile_id(matrix):
    tileDict = {}
    for y in range(len(matrix)):
        for x in matrix[y]:
            tileDict[x[0]] = x[1]
    return tileDict

