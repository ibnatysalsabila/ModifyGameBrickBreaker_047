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

