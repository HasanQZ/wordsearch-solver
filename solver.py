from PIL import Image, ImageDraw, ImageFont

def strcoords(string, substr):
    ret = string.find(substr)
    if ret == -1:
        return []
        
    coords = []

    for i in range(ret, ret + len(substr)):
        coords.append(i)

    return coords


def fdiagonal(l):
    max_col = len(l[0])
    max_row = len(l)

    fdiag = [[] for _ in range(max_row + max_col - 1)]

    for x in range(max_col):
        for y in range(max_row):
            fdiag[x+y].append(l[y][x])

    return fdiag


def bdiagonal(l):
    max_col = len(l[0])
    max_row = len(l)

    bdiag = [[] for _ in range(max_row + max_col - 1)]
    min_bdiag = -max_row + 1

    for x in range(max_col):
        for y in range(max_row):
            bdiag[x-y-min_bdiag].append(l[y][x])

    return bdiag


def r_fdiagonal(l):
    x = []
    for i in fdiagonal(l):
        x.append(list(reversed(i)))

    return x


def r_bdiagonal(l):
    x = []
    for i in bdiagonal(l):
        x.append(list(reversed(i)))

    return x


def frows(l): # here for consistency 
    return [i for i in l]


def fcols(l):
    cols = []
    for i in range(len(l[0])):
        ccol = []
        for row in l:
            ccol.append(row[i])

        cols.append(ccol)

    return cols


def crds(l):
    coords = []
    for y, row in enumerate(l):
        coordrow = []
        for x, col in enumerate(row):
            coordrow.append((x, y))

        coords.append(coordrow)
    return coords


def solve(l, searchterms):
    # converting to a list of searchterms, otherwise Python will read each character individually if a string is passed.
    if type(searchterms) != list: 
        searchterms = [searchterms]

    found_indexes = []
    words_and_locations = {}

    l_indexes = crds(l)

    fdiag = fdiagonal(l)
    bdiag = bdiagonal(l)

    # reverse diagonals
    r_fdiag = r_fdiagonal(l)
    r_bdiag = r_bdiagonal(l)
   
    rows = frows(l)
    rrows = []
    for row in rows:
        rrows.append(row[::-1])

    cols = fcols(l)
    rcols = []
    for col in cols:
        rcols.append(col[::-1])

    for searchterm in searchterms:
        word_found = False
        # horizontal 
        for ypos, row in enumerate(rows):
            coords = strcoords(''.join(row), searchterm)
            cwordi = []
            if coords != []:
                for xpos in coords:
                    cwordi.append((xpos, ypos))

                found_indexes.append(cwordi)
                word_found = True
                
        # horizontal reversed
        for ypos, row in enumerate(rows):
            coords = strcoords(''.join(row[::-1]), searchterm)
            cwordi = []
            if coords != []:
                for xpos in coords:
                    cwordi.append((len(row[::-1]) - xpos - 1, ypos))
                found_indexes.append(cwordi)
                word_found = True

        # vertical going down
        for xpos, col in enumerate(cols):
            coords = strcoords(''.join(col), searchterm)
            cwordi = []
            if coords != []:
                for ypos in coords:
                    cwordi.append((xpos, ypos))
                found_indexes.append(cwordi)
                word_found = True

        # vertical going up
        for xpos, col in enumerate(cols):
            coords = strcoords(''.join(reversed(col)), searchterm)
            cwordi = []
            if coords != []:
                for ypos in coords:
                    cwordi.append((xpos, len(col) - ypos - 1))
                found_indexes.append(cwordi)
                word_found = True

        # diagonals and their matching functions
        for _fdiag, func in [(fdiag, fdiagonal), (bdiag, bdiagonal), (r_fdiag, r_fdiagonal), (r_bdiag, r_bdiagonal)]:
            for diagc, diag in enumerate(_fdiag):
                coords = strcoords(''.join(diag), searchterm)
                if coords != []:
                    diaglinecoords = func(l_indexes)[diagc]
                    wordcoords = [diaglinecoords[i] for i in coords]
                    found_indexes.append(wordcoords)
                    word_found = True
                    

        if word_found:
            words_and_locations[searchterm] = found_indexes
        else:
            words_and_locations[searchterm] = None
            
        found_indexes = []

    return words_and_locations


def solve_to_image(board, words, filename='output.jpg', font='./WeretigerRegular.ttf'):
    termdict = solve(board, words)
    
    bcrds = crds(board)
    crdlocs = []

    for term in termdict:
        coords = termdict[term]
        if coords != None:
            for coordpair in coords:
                crdlocs += coordpair

    imwidth = len(board[0]) * 35
    imheight = len(board) * 30

    img = Image.new(mode='RGB', size=(imwidth, imheight), color=(255, 255, 255))
    try:
        myfont = ImageFont.truetype(font, 30)
    except OSError:
        myfont = ImageFont.load_default()
        print(f'WARNING: could not load font {font}, reverting to default font (characters may be very small!)')

    d1 = ImageDraw.Draw(img)

    fontx = 0
    fonty = 0
    for ri, row in enumerate(board):
        for ci, col in enumerate(row):
            x, y = bcrds[ri][ci]
            if (x, y) in crdlocs:
                color = (255, 0, 0)
            else:
                color = (0, 0, 0)
                
            d1.text((fontx, fonty), col, font=myfont, fill=color)
            fontx += 35

        fonty += 30
        fontx = 0

    img.save(filename)
