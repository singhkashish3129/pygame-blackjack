import pygame
import random

pygame.init()
WIDTH, HEIGHT = 823, 559
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

GREEN = (11, 94, 11)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (209, 176, 56)
RED = (200, 30, 30)
GREY = (100, 100, 100)

font_title = pygame.font.SysFont("Arial", 48, True)
font_label = pygame.font.SysFont("Arial", 32, True)
font_btn = pygame.font.SysFont("Arial", 28)
font_card = pygame.font.SysFont("Arial", 30, True)
font_score = pygame.font.SysFont("Arial", 32, True)
font_note = pygame.font.SysFont("Arial", 28, True)

def draw_card(rank, suit, x, y, hidden=False):
    pygame.draw.rect(screen, WHITE if not hidden else GREY, (x, y, 65, 90), border_radius=5)
    pygame.draw.rect(screen, BLACK, (x, y, 65, 90), 2, border_radius=5)
    if not hidden:
        txt = font_card.render(f"{rank}{suit}", True, BLACK)
    else:
        txt = font_card.render("?", True, BLACK)
    screen.blit(txt, (x+14, y+29))

def hand_score(hand):
    vals = [11 if r=='A' else 10 if r in ['J','Q','K'] else int(r) for r,s in hand]
    score = sum(vals)
    ace_count = sum(1 for v,s in hand if v=='A')
    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1
    return score

def new_deck():
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    deck = [(r, s) for s in suits for r in ranks]
    random.shuffle(deck)
    return deck

def draw_button(rect, label, color, tcolor):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
    txt = font_btn.render(label, True, tcolor)
    tx = rect[0] + (rect[2] - txt.get_width()) // 2
    ty = rect[1] + (rect[3] - txt.get_height()) // 2
    screen.blit(txt, (tx, ty))

def draw_hand(hand, x, y, reveal=True):
    for idx, (r, s) in enumerate(hand):
        hidden = False
        
        if not reveal and idx == 1:
            hidden = True
        draw_card(r, s, x + idx*85, y, hidden)

deal_btn = pygame.Rect(60, 480, 120, 50)
hit_btn = pygame.Rect(220, 480, 120, 50)
stand_btn = pygame.Rect(380, 480, 120, 50)
new_btn = pygame.Rect(590, 480, 160, 50)

def reset_game():
    return new_deck(), [], [], False, False, "", False

deck, player, dealer, stand, bust, msg, can_deal = reset_game()

running = True
while running:
    screen.fill(GREEN)
    screen.blit(font_title.render("Blackjack", True, GOLD), (WIDTH//2-115, 35))

    screen.blit(font_label.render("Dealer", True, WHITE), (60, 120))

    if dealer:
        draw_hand(dealer, 60, 170, reveal=(stand or bust))
        dealer_score_shown = hand_score([dealer[0]]) if not (stand or bust) else hand_score(dealer)
        screen.blit(font_score.render(f"Dealer: {dealer_score_shown}", True, WHITE), (WIDTH-225, 120))

    pygame.draw.line(screen, WHITE, (35, 280), (WIDTH-35, 280), 2)

    screen.blit(font_label.render("Player", True, WHITE), (60, 310))
    draw_hand(player, 60, 360, reveal=True)
    player_score = hand_score(player)
    screen.blit(font_score.render(f"Player: {player_score}", True, WHITE), (WIDTH-225, 310))

    if msg:
        m = font_note.render(msg, True, GOLD)
        screen.blit(m, (WIDTH//2 - m.get_width()//2, 420))

    draw_button(deal_btn, "Deal", GOLD, BLACK)
    draw_button(hit_btn, "Hit", WHITE, BLACK)
    draw_button(stand_btn, "Stand", WHITE, BLACK)
    draw_button(new_btn, "New Game", RED, WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if deal_btn.collidepoint(mx, my) and not player and not can_deal:
                player = [deck.pop(), deck.pop()]
                dealer = [deck.pop(), deck.pop()]
                stand = bust = False
                msg = ""
                can_deal = True
            elif hit_btn.collidepoint(mx, my) and player and not stand and not bust:
                player.append(deck.pop())
                if hand_score(player) > 21:
                    bust = True
                    msg = "Bust! Dealer wins."
            elif stand_btn.collidepoint(mx, my) and player and not stand and not bust:
                stand = True
                while hand_score(dealer) < 17:
                    dealer.append(deck.pop())
                ps, ds = hand_score(player), hand_score(dealer)
                if ds > 21:
                    msg = "Dealer busts! You win."
                elif ps > ds:
                    msg = "You win!"
                elif ps < ds:
                    msg = "Dealer wins."
                else:
                    msg = "Push! Tie game."
            elif new_btn.collidepoint(mx, my):
                deck, player, dealer, stand, bust, msg, can_deal = reset_game()

    pygame.display.flip()
pygame.quit()
