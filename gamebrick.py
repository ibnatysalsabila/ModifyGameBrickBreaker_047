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


