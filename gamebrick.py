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


