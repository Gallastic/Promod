import pygame
import sjakk as sj
pygame.init()

# Setup
screen_info = pygame.display.Info()  # Henter info om skjermen
HEIGHT = screen_info.current_h * 0.85  # Bruker skjermens høyde i piksler, og skalerer ned for å passe alle skjermer
WHITE = (235, 236, 208)  # Lys farge for sjakkbrett
REAL_WHITE = (255, 255, 255)  # Hvit farge for tekst og menyer
BLACK = (115, 149, 82)  # Mørk farge for sjakkbrett
REAL_BLACK = (0, 0, 0)  # Svart farge for tekst og menyer
BROWN = (101, 67, 33)  # Bakgrunnsfarge for brettet
YELLOW = (200, 200, 50)  # Farge for markeringsfelt
DARK_YELLOW = (150, 150, 50)  # Farge for mer spesifikke markeringer
SQUARE_SIZE = int((HEIGHT - HEIGHT // 9) // 8)  # Beregner størrelsen på hver rute basert på skjermstørrelsen

# Setter opp font og skjermen
font = pygame.font.Font("freesansbold.ttf", 20)  # Fonten som brukes til tall og bokstaver på brettet
screen = pygame.display.set_mode((HEIGHT, HEIGHT))  # Oppretter et kvadratisk vindu

# Setter navn på vinduet
pygame.display.set_caption("Sjakk")

# Setter opp sjakkbrett med brikkematrise
chess_board = [[None for _ in range(8)] for _ in range(8)]  # Lager et tomt sjakkbrett som en 2D-liste

# Laster inn bilder for sjakkbrikker i riktig skala
piece_images = sj.load_piece_images(SQUARE_SIZE)  # Funksjonen finnes i sjakk.py

# Initialiserer brikketyper og farger
pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 'pawn']
colors = ['black', 'white']
piece_list = []  # Liste som inneholder navnene på alle brikker
for color in colors:  # Går gjennom farger og brikker for å lage en liste
    for piece in pieces:
        piece_list.append(f"{color}_{piece}")

# Plasserer brikker på startposisjoner på sjakkbrettet
for l in range(9):  # Indeks 0-7 er hovedbrikkene, 8 er bønder
    plass = 0 if l < 8 else 1
    if plass == 0:
        chess_board[0][l] = piece_list[l]  # Sorte hovedbrikker øverst
        chess_board[7][l] = piece_list[l + 9]  # Hvite hovedbrikker nederst
    elif plass == 1:
        for l in range(8):
            chess_board[1][l] = piece_list[8]  # Sorte bønder
            chess_board[6][l] = piece_list[17]  # Hvite bønder

print(chess_board)  # Debugging: Skriver ut sjakkbrettet i konsollen

# Spilloop
brikke = None  # Lagrer brikken som skal flyttes
selected_pos = None  # Lagrer posisjonen til den valgte brikken
From = None  # Brikkens opprinnelige posisjon
Too = None  # Ny posisjon etter flytting

run = True
while run:  # Hovedløkken for spillet
    for event in pygame.event.get():  # Går gjennom alle hendelser
        if event.type == pygame.QUIT:  # Avslutt spillet hvis vinduet lukkes
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Når en musknapp trykkes
            if event.button == 1:  # Venstre museknapp
                x, y = event.pos  # Henter museposisjonen
                x_pos, y_pos = int(round(abs(x / SQUARE_SIZE - 1), 0)), int(round(abs(y / SQUARE_SIZE - 1), 0))
                if brikke is None:  # Hvis ingen brikke er valgt
                    brikke = chess_board[y_pos][x_pos]  # Velg brikken på denne posisjonen
                    selected_pos = (x_pos, y_pos)
                    From = (int(x_pos), int(y_pos))
                    Too = None
                    if brikke is None:  # Hvis feltet er tomt, nullstill valget
                        brikke = None
                else:  # Hvis en brikke allerede er valgt
                    old_x, old_y = selected_pos
                    if old_x == x_pos and old_y == y_pos:  # Klikk på samme brikke for å avvelge
                        brikke = None
                        From = None
                        Too = None
                    else:  # Flytt brikken til ny posisjon
                        Too = (int(x_pos), int(y_pos))
                        chess_board[y_pos][x_pos] = brikke  # Sett brikken på ny posisjon
                        chess_board[old_y][old_x] = None  # Fjern brikken fra gammel posisjon
                        brikke = None
                print(From)  # Debugging: Skriv ut posisjonen som brikken flyttes fra

    # Tegner sjakkbrettet og andre elementer
    sj.draw_board(screen, BROWN, WHITE, BLACK, SQUARE_SIZE)  # Tegn brettet
    sj.draw_current_square(From, Too, DARK_YELLOW, SQUARE_SIZE, screen)  # Marker posisjon for flytting
    sj.draw_letters(SQUARE_SIZE, font, screen)  # Tegn bokstaver (kolonner)
    sj.draw_numbers(SQUARE_SIZE, font, screen)  # Tegn tall (rader)

    # Marker gyldige trekk for forskjellige brikker
    sj.move_pawn(screen, From, chess_board, YELLOW, SQUARE_SIZE)
    sj.move_bishop(screen, From, chess_board, YELLOW, SQUARE_SIZE)
    sj.move_rook(screen, From, chess_board, YELLOW, SQUARE_SIZE)
    sj.move_queen(screen, From, chess_board, YELLOW, SQUARE_SIZE)
    sj.move_knight(screen, From, chess_board, YELLOW, SQUARE_SIZE)
    sj.move_king(screen, From, chess_board, YELLOW, SQUARE_SIZE)

    # Plotter brikkene på brettet
    sj.plotte_brikker(chess_board, piece_images, piece_list, SQUARE_SIZE, screen)

    # Sjekker om noen har vunnet
    sj.sjekke_seier(chess_board, REAL_WHITE, REAL_BLACK, screen)

    # Oppdaterer skjermen
    pygame.display.flip()
