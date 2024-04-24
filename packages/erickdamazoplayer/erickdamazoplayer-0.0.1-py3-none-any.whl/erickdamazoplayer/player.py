"""
Este es el modulo que incluye la clase
de reproductor de musica
"""


class Player:
    """
    Esta clase crea un reproductor
    de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio como parametro

        Parameters:
        song (str): Este es un string con el Path dse la cancion

        Returns:
        int: Devuelve 1 si reproduce con exito, en caso de fracaso devuelve 0
        """
        print("Reproduciendo cancion...")

    def stop(self):
        print("Stopping...")
