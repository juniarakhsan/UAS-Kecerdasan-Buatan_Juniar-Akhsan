from tkinter import *
# mengimpor pustaka acak
import random

# Menambahkan variable global

# variable global
# Pengaturan jendela
WIDTH = 900
HEIGHT = 300

# PENGATURAN RAKET
# lebar raket & tinggi raket
PAD_W = 10
PAD_H = 100

# PENGATURAN BOLA
# seberapa besar kecepatan bola akan meningkat setiap pukulan
BALL_SPEED_UP = 1.05
# kecepatan bola maksimum & radius bola
BALL_MAX_SPEED = 40
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

# SKOR PEMAIN
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# MENAMBAHKAN VARIABLE GLOBAL UNTUK JARAK
# ke tepi kanan lapangan permainan
right_line_distance =  WIDTH - PAD_W

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player =="right":
      PLAYER_1_SCORE += 1
      c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
      PLAYER_2_SCORE += 1
      c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
  global BALL_X_SPEED
  # letakkan bola dibagian tengah
  c.coords(BALL, WIDTH/2-BALL_RADIUS/2, 
           HEIGHT/2-BALL_RADIUS/2, 
           WIDTH/2+BALL_RADIUS/2, 
           HEIGHT/2+BALL_RADIUS/2)
  # aturan arah bola ke pemain yang kalah tapi mengurangi kecepatan ke semula
  BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)

# FUNGSI BOLA PANTUL
def bounce(action):
  global BALL_X_SPEED, BALL_Y_SPEED
  # memukul dengan raket
  if action == "strike":
    BALL_Y_SPEED = random.randrange(-10, 10)
    if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
      BALL_X_SPEED *= -BALL_SPEED_UP
    else:
      BALL_X_SPEED = -BALL_X_SPEED
  else:
    BALL_Y_SPEED = -BALL_Y_SPEED

# MEMASANG JENDELA
root = Tk()
root.title("Pong")

# AREA ANIMASI
c = Canvas(root, width=WIDTH, height=HEIGHT, background="purple")
c.pack()

# ELEMEN LAPANGAN BERMAIN
# garis kiri, garis kanan, garis tengah
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

# PEMASANGAN FASILITAS PERMAINAN
# membuat bola
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="white")

# raket kiri
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")

# raket yang tepat
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, 
                          PAD_H, width=PAD_W, fill="yellow")

p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4, 
                         text=PLAYER_1_SCORE,
                         font="Arial 20", 
                         fill="white")

p_2_text = c.create_text(WIDTH/6, PAD_H/4, 
                         text=PLAYER_2_SCORE,
                         font="Arial 20", 
                         fill="white")

# MENAMBAHKAN VARIABLE GLOBAL UNTUK KECEPATAN BOLA
# di seluruh dan secara vertikal
BALL_0_CHANGE = 20
BALL_Y_CHANGE = 0

def move_ball():
    # menentukan koordinat sisi bola dan pusatnya
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    # pantulan vertikal
    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W: 
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]: 
                bounce("strike")
            else:
                update_score("left") 
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]: 
                bounce("strike")
            else:
                update_score("right") 
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED) 
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)

    # pantulan horizontal
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT: 
        bounce("ricochet")

# mengatur variable global untuk kecepatan raket
# kecepatan gerak raket yang akan dilalui
PAD_SPEED = 20
# kecepatan plaform kiri
LEFT_PAD_SPEED = 0
# kecepatan platform kanan
RIGHT_PAD_SPEED = 0

# fungsi pergerakan kedua raket
def move_pads():
   # untuk kenyamanan, ciptakan kosakata yang gampang
   PADS = {LEFT_PAD: LEFT_PAD_SPEED,
           RIGHT_PAD : RIGHT_PAD_SPEED}
   for pad in PADS:
      c.move(pad, 0, PADS[pad])
      if c.coords(pad)[1] < 0:
         c.move(pad, 0, -c.coords(pad)[1])
      elif c.coords(pad)[3] > HEIGHT:
         c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
  move_ball()
  move_pads()
  # memanggil dirinya sendiri setiap 30detik
  root.after(30, main)

# mengatur fokus pada canvas untuk merespons penekanan tombol
c.focus_set()

# mari menulis fungsi untuk menangani penekanan tombol
def movement_handler(event):
  global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
  if event.keysym == "w":
    LEFT_PAD_SPEED = -PAD_SPEED
  elif event.keysym == "s":
    LEFT_PAD_SPEED = PAD_SPEED
  elif event.keysym == "Up":
    RIGHT_PAD_SPEED = -PAD_SPEED
  elif event.keysym == "Down":
    RIGHT_PAD_SPEED = PAD_SPEED

# mengikat fungsi ini ke canvas
c.bind("<KeyPress>", movement_handler)

# membuat fungsi respons pelepasan tombol
def stop_pad(event):
  global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
  if event.keysym == "ws":
    LEFT_PAD_SPEED = 0
  elif event.keysym in ("Up", "Down"):
    RIGHT_PAD_SPEED = 0

#m ari mengikat fungsi ini ke canvas
c.bind("<KeyRelease>", stop_pad)

# pengaturan dalam pergerakan
main()

# menjalankan jendela
root.mainloop()
