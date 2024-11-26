import tkinter as tk

# GameObject adalah kelas dasar untuk objek yang digambar pada canvas
class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        # Mendapatkan koordinat posisi objek pada canvas
        return self.canvas.coords(self.item)

    def move(self, x, y):
        # Menggerakkan objek pada canvas sejauh x dan y
        self.canvas.move(self.item, x, y)

    def delete(self):
        # Menghapus objek dari canvas
        self.canvas.delete(self.item)


# Kelas Ball mewarisi GameObject, merepresentasikan bola dalam permainan
class Ball(GameObject):
    def __init__(self, canvas, x, y):
        # Inisialisasi bola dengan radius, arah, dan kecepatan
        self.radius = 10
        self.direction = [1, -1]  # Arah bola (x, y)
        self.speed = 5  # Kecepatan bola
        item = canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill='#87CEEB',  # Warna bola
            outline='#4682B4',  # Warna outline
            width=2
        )
        super(Ball, self).__init__(canvas, item)

    def update(self):
        # Mengupdate posisi bola dan memantul jika menyentuh tepi canvas
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:  # Pantulan horizontal
            self.direction[0] *= -1
        if coords[1] <= 0:  # Pantulan vertikal atas
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        # Mengatur logika tabrakan bola dengan objek lain
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5  # Posisi tengah bola
        if len(game_objects) > 1:
            self.direction[1] *= -1  # Pantulan vertikal
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            # Menentukan arah pantulan berdasarkan posisi tabrakan
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()  # Hit pada brick


# Kelas Paddle mewarisi GameObject, merepresentasikan paddle dalam permainan
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        # Inisialisasi paddle dengan ukuran dan posisi
        self.width = 120
        self.height = 10
        self.ball = None  # Bola yang terhubung dengan paddle
        item = canvas.create_rectangle(
            x - self.width / 2, y - self.height / 2,
            x + self.width / 2, y + self.height / 2,
            fill='#FFB643',  # Warna paddle
            outline='#FF8C00'  # Outline paddle
        )
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        # Menghubungkan paddle dengan bola
        self.ball = ball

    def move(self, offset):
        # Menggerakkan paddle ke kiri atau kanan
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)


# Kelas Brick mewarisi GameObject, merepresentasikan balok dalam permainan
class Brick(GameObject):
    COLORS = {1: '#FF0000', 2: '#FFFF00', 3: '#00FF00', 4: '#0000FF', 5: '#FFFFFF', 6: '#000000'}

    def __init__(self, canvas, x, y, hits):
        # Inisialisasi brick dengan warna sesuai jumlah hits
        self.width = 80  # Lebar brick
        self.height = 20  # Tinggi brick
        self.hits = hits  # Jumlah hits yang diperlukan untuk menghancurkan brick
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(
            x - self.width / 2, y - self.height / 2,
            x + self.width / 2, y + self.height / 2,
            fill=color, tags='brick'  # Tag untuk identifikasi brick
        )
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        # Menghapus brick dari canvas saat terkena bola
        self.delete()
        game.increase_score()  # Menambah skor


# Kelas Game adalah inti dari permainan, mengatur semua objek dan logika permainan
class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        # Inisialisasi variabel game
        self.lives = 3
        self.score = 0
        self.width = 800  # Ukuran canvas (lebar)
        self.height = 600  # Ukuran canvas (tinggi)
        self.canvas = tk.Canvas(self, bg='#A0D6E4',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}  # Menyimpan semua objek game
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width / 2, 550)  # Membuat paddle
        self.items[self.paddle.item] = self.paddle

        self.create_brick_layout()  # Membuat layout brick

        self.hud = None  # Menampilkan nyawa
        self.hud_score = None  # Menampilkan skor
        self.setup_game()  # Setup awal permainan
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))  # Gerakan paddle kiri
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))  # Gerakan paddle kanan

    def create_brick_layout(self):
        # Membuat layout brick secara grid
        brick_width = 80
        brick_height = 20
        padding = 5
        rows = 8
        cols = self.width // (brick_width + padding)

        for row in range(rows):
            for col in range(cols):
                x = padding + col * (brick_width + padding) + brick_width / 2
                y = 50 + row * (brick_height + padding) + brick_height / 2
                hits = (row % 6) + 1  # Variasi jumlah hits per baris
                self.add_brick(x, y, hits)

    def setup_game(self):
        # Setup permainan baru
        self.add_ball()
        self.update_lives_text()
        self.update_score_text()
        self.text = self.draw_text(400, 300, 'Click Space to Start', 19, 'black')
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        # Menambahkan bola baru di atas paddle
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 530)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        # Menambahkan brick baru ke canvas
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size, color):
        # Menampilkan teks di canvas
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text, font=font, fill=color)

    def update_lives_text(self):
        # Mengupdate teks nyawa
        text = 'Lives: %s' % self.lives
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15, 'black')
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def update_score_text(self):
        # Mengupdate teks skor
        text = 'Score: %s' % self.score
        if self.hud_score is None:
            self.hud_score = self.draw_text(750, 20, text, 15, 'black')
        else:
            self.canvas.itemconfig(self.hud_score, text=text)

    def increase_score(self):
        # Menambah skor
        self.score += 10
        self.update_score_text()

    def start_game(self):
        # Memulai game loop
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        # Loop utama permainan
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = None  # Menghentikan bola
            self.draw_text(400, 300, 'You win! You are the Breaker of Bricks.', 20, 'black')
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(400, 300, 'You Lose! Game Over!', 20, 'red')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        # Mengecek tabrakan bola dengan objek lain
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)


# Menjalankan permainan
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Break those Bricks!')
    game = Game(root)
    game.mainloop()