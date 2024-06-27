class Usuario:
    def __init__(self,Nombre,Apellido,Edad,Localizacion,Correo,Password,ListaAmigos=[],Chats=[]):
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Edad = Edad
        self.Localizacion = Localizacion
        self.Password = Password
        self.Correo = Correo
        self.ListaAmigos = ListaAmigos
        self.Chats = Chats
    def toDBCollection(self):
        Pais, Ciudad = self.Localizacion.split(",")
        return{
            'Nombre':self.Nombre,
            'Apellido':self.Apellido,
            'Edad':int(self.Edad),
            'Localizacion':{"Pais":Pais,"Ciudad":Ciudad},
            'Correo':self.Correo,
            'Password':self.Password,
            'ListaAmigos':self.ListaAmigos,
            'Chats':self.Chats
        }
    
    def toDBCollectionUpdate(self):
        Pais, Ciudad = self.Localizacion.split(",")
        return{
            'Nombre':self.Nombre,
            'Apellido':self.Apellido,
            'Edad':int(self.Edad),
            'Localizacion':{"Pais":Pais,"Ciudad":Ciudad},
            'Correo':self.Correo,
            'Password':self.Password,
        }