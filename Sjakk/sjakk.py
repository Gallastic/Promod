import pygame
pygame.init()

def draw_board(skjerm,brun,hvit,svart,rute):       #Tegner brettet
    skjerm.fill(brun)  
    for row in range(8):
        for col in range(8):
            color = hvit if (row + col) % 2 == 0 else svart
            pygame.draw.rect(skjerm, color, (col * rute+0.5*rute, row * rute+0.5*rute, rute, rute))
def draw_letters(rute,tekst,skjerm):     #Tegner bokstavene på siden av brettet
    LETTERS = ['a','b','c','d','e','f','g','h']
    for l in range(8):
        text = tekst.render(LETTERS[l], True, (0,0,0))
        skjerm.blit(text,(rute*0.9+l*rute,rute*0.15))
        skjerm.blit(text,(rute*0.9+l*rute,rute*8.65))
def draw_numbers(rute,tekst,skjerm):     #Tegner tallene på siden av brettet
    for l in range(8):
        text = tekst.render(str(8-l), True, (0,0,0))        #Legger grunnlaget for å rendre tekst
        skjerm.blit(text,(rute*0.15,rute*0.9+l*rute))       #Render tall på ene side av brette
        skjerm.blit(text,(rute*8.65,rute*0.9+l*rute))       #denne tar andre siden
def draw_current_square(fra, til, farge, rute,skjerm):          #Tegner feltene man trykker på (til og fra)
    if fra != None:
        old_x,old_y = fra
        x_pos,y_pos = int(0.5*rute+old_x*rute),int(rute*0.5+rute*old_y)
        pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
    if til != None:
        x,y = til
        x_pos,y_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*y)
        pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
def plotte_brikker(sjakkbrett,bilde,brikker,rute,skjerm):      #Plotter matrisen med brikker, fin når jeg flytter brikkene i matrisen
    for col in range(8):
        for row in range(8):
            if sjakkbrett[col][row] != None:
                plass = brikker.index(sjakkbrett[col][row])
                skjerm.blit(bilde[plass],(0.5*rute+row*rute,rute*0.5+rute*col))
def load_piece_images(rute):    #Laster inn bilde av brikkene og putter de i en liste
    pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook','pawn']  #Liste over de forskjellige brikkene
    colors = ['black','white']      #Liste over fargene
    images = []     #Lager tom liste for alle brikkene
    for color in colors:
        for piece in pieces:
            key = f"{color}_{piece}"  
            image = pygame.image.load(f"C:\\Users\\jespe\\OneDrive - Akershus fylkeskommune\\Valler Skole\\Tredje Klasse 2024-2025\\Programmering og Moddelering\\Programmering\\sjakk\\{key}.png") #Koden ligger i samme mappe som bildene så filbanen skal kunne fjernes
            images.append(pygame.transform.scale(image,(rute,rute)))        #Laster opp bildene av brikkene riktig skalert for feltene på sjakkbrettet
    return images

#Flytte brikker mønster
def move_pices_line(fra,spillbrett,rute,farge,skjerm,x_rettning ,y_rettning):       #Funksjon som tegner felt i en rettning til den møter en annen brikke eller kanten
    x,y = fra       #Henter koordinatene fra originalfeltet
    x,y = x+x_rettning, y+y_rettning        #Bestemmer hvilken rettning man skal flytte
    while -1 < x < 8 and -1 < y < 8:        #Så lenge koordinatene er inne på feltet
        if spillbrett[y][x] == None:        #sjekker om neste felt er ledig
            x_pos,y_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y))
            pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))    #Tegner feltet gult hvis det er ledig
        elif spillbrett[y][x] != None:      #HVis den møter en brikke, tenger den en siste gang før den gjør x så stor at while løkka stopper
            x_pos,y_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y))
            pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))    #Tegner feltet gult en siste gang
            x = 10
        x,y = x+x_rettning, y+y_rettning        #Leger til en i rettning den skal gå
def one_step(fra,rute,farge,skjerm,x_rettning ,y_rettning):         #Funksjon som kun fargelegger et felt gult (hest og bonde)
    x,y = fra       #Henter original verdi
    x,y = x+x_rettning,y+y_rettning     #flytter fra originalfeltet
    #print(f"({x},{y})")
    if -1 < x < 8 and -1 < y < 8:       #Sjekker om det nye feltet er på brettet
        x_pos,y_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y))
        pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))     #Tenger det nye feltet


#Flytte brikker funksjon
def move_pawn(skjerm,fra,spillbrett,farge,rute):        #Funksjon for alle mulig trekk for en bonde
    if fra != None:
        x,y = fra
        if spillbrett[y][x] == "white_pawn":        #For de hvite
            if y == 6:
                x_pos,y1_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y-1))
                pygame.draw.rect(skjerm, farge, (x_pos, y1_pos, rute, rute))
                x_pos,y2_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y-2))
                pygame.draw.rect(skjerm, farge, (x_pos, y2_pos, rute, rute))
            if -1 < x+1 < 8 and -1 < y-1 < 8 and spillbrett[y][x+1] == "black_pawn" and spillbrett[y-1][x+1] == None and y == 3:
                x_pos,y_pos = int(0.5*rute+(x+1)*rute),int(rute*0.5+rute*(y-1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            elif -1 < x-1 < 8 and -1 < y-1 < 8 and spillbrett[y][x-1] == "black_pawn" and spillbrett[y-1][x-1] == None and y == 3:
                x_pos,y_pos = int(0.5*rute+(x-1)*rute),int(rute*0.5+rute*(y-1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x-1 < 8 and -1 < y-1 < 8 and spillbrett[y-1][x-1] != None:
                x_pos,y_pos = int(0.5*rute+(x-1)*rute),int(rute*0.5+rute*(y-1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x+1 < 8 and -1 < y-1 < 8 and spillbrett[y-1][x+1] != None:
                x_pos,y_pos = int(0.5*rute+(x+1)*rute),int(rute*0.5+rute*(y-1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x < 8 and -1 < y-1 < 8 and spillbrett[y-1][x] == None:
                x_pos,y_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y-1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))


        elif spillbrett[y][x] == "black_pawn":          #for de svarte
            if y == 1:
                x_pos,y1_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y+1))
                pygame.draw.rect(skjerm, farge, (x_pos, y1_pos, rute, rute))
                x_pos,y2_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y+2))
                pygame.draw.rect(skjerm, farge, (x_pos, y2_pos, rute, rute))
            if -1 < x+1 < 8 and -1 < y+1 < 8 and spillbrett[y][x+1] == "white_pawn" and spillbrett[y+1][x+1] == None and y == 4:
                x_pos,y_pos = int(0.5*rute+(x+1)*rute),int(rute*0.5+rute*(y+1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x-1 < 8 and -1 < y+1 < 8 and spillbrett[y][x-1] == "white_pawn" and spillbrett[y+1][x-1] == None and y == 4:
                x_pos,y_pos = int(0.5*rute+(x-1)*rute),int(rute*0.5+rute*(y+1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x-1 < 8 and -1 < y+1 < 8 and spillbrett[y+1][x-1] != None:
                x_pos,y_pos = int(0.5*rute+(x-1)*rute),int(rute*0.5+rute*(y+1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x+1 < 8 and -1 < y+1 < 8 and spillbrett[y+1][x+1] != None:
                x_pos,y_pos = int(0.5*rute+(x+1)*rute),int(rute*0.5+rute*(y+1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))
            if -1 < x < 8 and -1 < y+1 < 8 and spillbrett[y+1][x] == None:
                x_pos,y_pos = int(0.5*rute+x*rute),int(rute*0.5+rute*(y+1))
                pygame.draw.rect(skjerm, farge, (x_pos, y_pos, rute, rute))           
def move_bishop(skjerm,fra,spillbrett,farge,rute):      #Funksjon for flytting av skråløper, viser alle mulig trekk
    if fra != None:
        x,y = fra
        #print(f"({x},{y})")
        if spillbrett[y][x] == "white_bishop" or spillbrett[y][x] == "black_bishop":
            move_pices_line(fra,spillbrett,rute,farge,skjerm,-1 ,-1)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,-1 ,1)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,1 ,-1)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,1 ,1)               
def move_rook(skjerm,fra,spillbrett,farge,rute):        #Funksjon som viser alle låvlige trekk for tårn
    if fra != None:
        x,y = fra
        #print(f"({x},{y})")
        if spillbrett[y][x] == "white_rook" or spillbrett[y][x] == "black_rook":
            move_pices_line(fra,spillbrett,rute,farge,skjerm,0 ,-1)  
            move_pices_line(fra,spillbrett,rute,farge,skjerm,0 ,1)        
            move_pices_line(fra,spillbrett,rute,farge,skjerm,-1 ,0)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,1 ,0)
def move_queen(skjerm,fra,spillbrett,farge,rute):       #Funksjon som viser alle låvlige trekk for dronning
    if fra != None:
        x,y = fra
        #print(f"({x},{y})")
        if spillbrett[y][x] == "white_queen" or spillbrett[y][x] == "black_queen":
            move_pices_line(fra,spillbrett,rute,farge,skjerm,0 ,-1)  
            move_pices_line(fra,spillbrett,rute,farge,skjerm,0 ,1)        
            move_pices_line(fra,spillbrett,rute,farge,skjerm,-1 ,0)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,1 ,0)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,-1 ,-1)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,-1 ,1)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,1 ,-1)
            move_pices_line(fra,spillbrett,rute,farge,skjerm,1 ,1)           
def move_knight(skjerm,fra,spillbrett,farge,rute):       ##Funksjon som viser alle låvlige trekk for tårn
    if fra != None:
        x,y = fra
        if spillbrett[y][x] == "white_knight" or spillbrett[y][x] == "black_knight":
            one_step(fra,rute,farge,skjerm,1 ,-2)
            one_step(fra,rute,farge,skjerm,1 ,2)
            one_step(fra,rute,farge,skjerm,2 ,-1)
            one_step(fra,rute,farge,skjerm,2 ,1)
            one_step(fra,rute,farge,skjerm,-1 ,-2)
            one_step(fra,rute,farge,skjerm,-1 ,2)
            one_step(fra,rute,farge,skjerm,-2 ,-1)
            one_step(fra,rute,farge,skjerm,-2 ,1)
def move_king(skjerm,fra,spillbrett,farge,rute):            ##Funksjon som viser alle låvlige trekk for Konge
    if fra != None:
        x,y = fra
        if spillbrett[y][x] == "white_king" or spillbrett[y][x] == "black_king":
            one_step(fra,rute,farge,skjerm,0 ,1)
            one_step(fra,rute,farge,skjerm,-1 ,1)
            one_step(fra,rute,farge,skjerm,1 ,1)
            one_step(fra,rute,farge,skjerm,-1 ,0)
            one_step(fra,rute,farge,skjerm,1 ,0)
            one_step(fra,rute,farge,skjerm,-1 ,-1)
            one_step(fra,rute,farge,skjerm,1 ,-1)
            one_step(fra,rute,farge,skjerm,0 ,-1)
        
#Sjekke etter seier
def sjekke_seier(spillbrett,hvit,svart,skjerm):
    if not any("white_king" in rad for rad in spillbrett):
        skjerm.fill(svart)
    elif not any("black_king" in rad for rad in spillbrett):
        skjerm.fill(hvit)