#Clase que se utiliza para el manejo de directorios
class Dirs():


    def __init__(self):
        self._dir_imagenes=""
        self._dir_collage=""
        self._dir_memes=""
    

    def set_dir_imagenes(self,path):
        self._dir_imagenes = path


    def set_dir_collage(self,path):
        self._dir_collage = path


    def set_dir_memes(self,path):
        self._dir_memes = path


    def get_dir_imagenes(self):
        return self._dir_imagenes


    def get_dir_collage(self):
        return self._dir_collage
    

    def get_dir_memes(self):
        return self._dir_memes


dirs = Dirs()
