from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text, DECIMAL,DateTime
from sqlalchemy.orm import declarative_base,sessionmaker, relationship

#Configurazione del motore di SQLAlchemy per connettersi al database MySQL
DATABASE_URL = "mysql+mysqlconnector://root:King@localhost/ecommercedivideogiochi"

#Creazione dell'engine e la base per le classi
engine = create_engine(DATABASE_URL)
Base = declarative_base()


#Creazione di una sessione per interagire con il database
Session = sessionmaker(bind=engine)
session = Session()

#Definizioni delle classi per rappresentare le tabelle
class Cliente(Base):
    __tablename__ = 'Cliente'
    ID_Cliente = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(50), nullable=False)
    Cognome = Column(String(50), nullable=False)
    DataNascita = Column(Date)
    IndirizzoResidenza = Column(String(100))
    Email = Column(String(255),unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    NumeroTelefono = Column(String(20), unique=True)


class Amministratore(Base):
    __tablename__ = 'Amministratore'
    ID_Amministratore = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(50), nullable=False)
    Cognome = Column(String(50), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    NumeroTelefono = Column(String(20), unique=True)


class Magazzino(Base):
    __tablename__ = 'Magazzino'
    ID_Magazzino = Column(Integer, primary_key=True, autoincrement=True)
    QunatitaProdotto = Column(Integer, nullable=False)


class Prodotto(Base):
    __tablename__ = 'Prodotto'
    ID_Prodotto = Column(Integer, primary_key=True, autoincrement=True)
    Titolo = Column(String(100), nullable=False)
    Descrizione = Column(Text)
    Categoria = Column(String(30))
    Piattaforma = Column(String(30))
    DataPubblicazione = Column(Date)
    Prezzo = Column(DECIMAL(10, 2), nullable=False)
    ID_Magazzino = Column(Integer, ForeignKey('Magazzino.ID_Magazzino'))
    ID_Amministratore = Column(Integer, ForeignKey('Amministratore.ID_Amministratore'))

class Ordine(Base):
    __tablename__ = 'Ordine'
    ID_Ordine = Column(Integer, primary_key=True, autoincrement=True)
    DataCreazione = Column(DateTime, nullable=False)
    DataConsegna = Column(Date)
    Stato = Column(String(30))
    MetodoPagamento = Column(String(50))
    IndirizzoConsegna = Column(String(100))
    Totale = Column(DECIMAL(10, 2), nullable=False)
    ID_Cliente = Column(Integer, ForeignKey('Cliente.ID_Cliente'))
    ID_Amministratore = Column(Integer, ForeignKey('Amministratore.ID_Amministratore'))
    cliente = relationship("Cliente", backref="ordini")
    amministratore = relationship("Amministratore", backref="ordini")

class Recensione(Base):
    __tablename__ = 'Recensione'
    ID_Recensione = Column(Integer, primary_key=True, autoincrement=True)
    DataCreazione = Column(Date)
    Valutazione = Column(Integer, nullable=False, check="Valutazione BETWEEN 1 AND 5")
    Commento = Column(Text)
    ID_Cliente = Column(Integer, ForeignKey('Cliente.ID_Cliente'))
    ID_Prodotto = Column(Integer, ForeignKey('Prodotto.ID_Prodotto'))
    ID_Amministratore = Column(Integer, ForeignKey('Amministratore.ID_Amministratore'))
    cliente = relationship("Cliente", backref="recensioni")
    prodotto = relationship("Prodotto", backref="recensioni")
    amministratore = relationship("Amministratore", backref="recensioni")

class Wishlist(Base):
    __tablename__ = 'Wishlist'
    ID_Wishlist = Column(Integer, primary_key=True, autoincrement=True)
    Nome =Column(String(50))
    ID_Cliente = Column(Integer, ForeignKey('Cliente.ID_Cliente'))
    cliente = relationship("Cliente", backref="wishlists")

class OrdineProdotto(Base):
    __tablename__ = 'Ordine_Prodotto'
    ID_Ordine = Column(Integer, ForeignKey('Ordine.ID_Ordine'), primary_key=True)
    ID_Prodotto = Column(Integer, ForeignKey('Prodotto.ID_Prodotto'), primary_key=True)
    Quantita = Column(Integer, nullable=False)
    ordine = relationship("Ordine", backref="prodotti_ordinati")
    prodotto = relationship("Prodotto", backref="ordini")

class WishlistProdotto(Base):
    __tablename__ = 'Wishlist_Prodotto'
    ID_Wishlist = Column(Integer, ForeignKey('Wishlist.ID_Wishlist'), primary_key=True)
    ID_Prodotto = Column(Integer, ForeignKey('Prodotto.ID_Prodotto'), primary_key=True)
    Quantita = Column(Integer, nullable=False)
    wishlist= relationship("Wishlist", backref="prodotti_nella_wishlist")
    prodotto = relationship("Prodotto", backref="wishlist_prodotti")

Base.metadata.create_all(engine)

#Implementazioni delle operazioni CRUD

#CREATE - Aggiungere un nuovo cliente
def crea_cliente(nome, cognome, email, password, telefono):
    nuovo_cliente =Cliente(
        Nome=nome,
        Cognome=cognome,
        Email=email,
        Password=password,
        NumeroTelefono=telefono
    )
    session.add(nuovo_cliente)
    session.commit()
    print(f"Cliente {nome} {cognome} creato con succeso!")

# - Aggiungere un nuovo amministratore
def crea_amministratore(nome, cognome, email, password, telefono):
    nuovo_amministratore = Amministratore(
        Nome=nome,
        Cognome=cognome,
        Email=email,
        Password=password,
        NumeroTelefono=telefono
    )
    session.add(nuovo_amministratore)
    session.commit()
    print(f"Amministratore {nome} {cognome} creato con succeso!")

# - Aggiungere un nuovo prodotto
def crea_prodotto(titolo, descrizione, categoria, piattaforma, prezzo, id_magazzino, id_amministratore):
    nuovo_prodotto = Prodotto(
        Titolo=titolo,
        Descrizione=descrizione,
        Categoria=categoria,
        Piattaforma=piattaforma,
        Prezzo=prezzo,
        ID_Magazzino=id_magazzino,
        ID_Amministratore=id_amministratore
    )
    session.add(nuovo_prodotto)
    session.commit()
    print(f"Prodotto {titolo} creato con succeso!")

# - Aggiungere un nuovo ordine
def crea_ordine(data_creazione, stato, metodo_pagamento, indirizzo_consegna, totale, id_cliente, id_amministartore):
    nuovo_ordine = Ordine(
        DataCreazione=data_creazione,
        Stato=stato,
        MetodoPagamento=metodo_pagamento,
        IndirizzoConsegna=indirizzo_consegna,
        Totale=totale,
        ID_Cliente=id_cliente,
        ID_Amministratore=id_amministartore
    )
    session.add(nuovo_ordine)
    session.commit()
    print(f"L'ordine per il cliente {id_cliente} è stato creato con successo!")

# - Aggiungere una nuova recensione
def crea_recensione(data_creazione, valutazione, commento, id_cliente, id_prodotto, id_amministatore):
    prodotto = session.query(Prodotto).filter_by(ID_Prodotto=id_prodotto).first()
    if prodotto:
        nuova_recensione = Recensione(
            DataCreazione=data_creazione,
            Valutazione=valutazione,
            Commento=commento,
            ID_Cliente=id_cliente,
            ID_Prodotto=id_prodotto,
            ID_Amministratore=id_amministatore
        )
        session.add(nuova_recensione)
        session.commit()
        print(f"La recensione per {prodotto.Titolo} è stata creata con successo!")
    else:
        print(f"Prodotto con ID {id_prodotto} non trovato.")

# - Aggiungere una wishlist (unica per ogni cliente)
def crea_wishlist(nome, id_cliente):
    wishlist_esistente= session.query(Wishlist).filter_by(ID_Cliente=id_cliente).first()
    if wishlist_esistente:
        print(f"Il cliente {id_cliente} ha gia una wishlist.")
    else:
        nuova_wishlist = Wishlist(
            Nome=nome,
            ID_Cliente=id_cliente
        )
        session.add(nuova_wishlist)
        session.commit()
        print(f"La Whislist '{nome}' è stata creata per il cliente {id_cliente}!")

# - Inserimento di un prodotto all'interno di un'ordine
def aggiungi_prodotto_a_ordine(id_ordine, id_prodotto, quantita):
    prodotto = session.query(Prodotto).filter_by(ID_Prodotto=id_prodotto).first()
    if prodotto:
        nuovo_ordine_prodotto = OrdineProdotto(
            ID_Ordine=id_ordine,
            ID_Prodotto=id_prodotto,
            Quantita=quantita
        )
        session.add(nuovo_ordine_prodotto)
        session.commit()
        if quantita == 1:
            print(f"{prodotto.Titolo} è stato aggiunto all'ordine {id_ordine}.")
        else:
            print(f"{quantita} unità di '{prodotto.Titolo}' sono state aggiunte all'ordine {id_ordine}.")
    else:
        print(f"Prodotto con ID {id_prodotto} non trovato.")

# - Inserimento di un prodotto all'interno di una wishlist
def aggiungi_prodotto_a_wishlist(id_wishlist, id_prodotto):
    prodotto = session.query(Prodotto).filter_by(ID_Prodotto=id_prodotto).first()
    if prodotto:
        prodotto_nella_wishlist = session.query(WishlistProdotto).filter_by(ID_Wishlist=id_wishlist,
                                                                            ID_Prodotto=id_prodotto).first()
        if prodotto_nella_wishlist:
            print(f"'{prodotto.Titolo}' è gia presente nella wishlist {id_wishlist}.")
        else:
            nuovo_wishlist_prodotto = WishlistProdotto(
                ID_Wishlist=id_wishlist,
                ID_Prodotto=id_prodotto,
                Quantita=1
            )
            session.add(nuovo_wishlist_prodotto)
            session.commit()
            print(f"{prodotto.Titolo} aggiunto alla wishlist {id_wishlist}!")
    else:
        print(f"Prodotto con ID {id_prodotto} non trovato.")

#READ - Visualizzare una lista di tutti i clienti
def lista_clienti():
    clienti = session.query(Cliente).all()
    for cliente in clienti:
        print(f"ID: {cliente.ID_Cliente}, Nome:{cliente.Nome}, Cognome:{cliente.Cognome}, Email: {cliente.Email}")

# - Visualizzare una lista di tutti gli amministratori
def lista_amministratori():
    amministratori = session.query(Amministratore).all()
    for amministratore in amministratori:
        print(f"ID: {amministratore.ID_Amministratore}, Nome:{amministratore.Nome},"
              f"Cognome: {amministratore.Cognome}, Email: {amministratore.Email}")

# - Lista dei prodotti all'interno del magazzino
def lista_prodotti_magazzino(id_magazzino):
    prodotti = session.query(Prodotto).filter_by(ID_Magazzino=id_magazzino).all()
    if prodotti:
        totale_quantita = 0
        print(f"Lista dei prodotti nel magazzino {id_magazzino}:\n")
        for prodotto in prodotti:
            quantita = prodotto.ID_Magazzino
            print(f"ID Prodotto: {prodotto.ID_Prodotto}, Titolo: {prodotto.Titolo}, Quantita: {quantita}")
            totale_quantita += quantita
            print(f"\nTotale quantità di tutti i prodotti nel magazzino: {totale_quantita}.")
    else:
        print(f"Il magazzino è vuoto.")

# - Visulizzare un singolo prodotto
def visualizza_prodotto(id_prodotto):
    prodotto= session.query(Prodotto).filter_by(ID_Prodotto=id_prodotto).first()
    if prodotto:
        print(f"ID: {prodotto.ID_Prodotto}, Titolo: {prodotto.Titolo}, Descrizione: {prodotto.Descrizione}, "
              f"Prezzo: {prodotto.Prezzo}")
    else:
        print(f"Il prodotto con ID {id_prodotto} non è stato trovato.")

# - Visualizzare lo storico degli ordini di un singolo cliente
def storico_ordini_cliente(id_cliente):
    ordini = session.query(Ordine).filter_by(ID_Cliente=id_cliente).all()
    if ordini:
        for ordine in ordini:
            print(f"ID Ordine: {ordine.ID_Ordine}, Data Craezione: {ordine.DataCraezione}, Totale: {ordine.Totale},"
                  f"Stato: {ordine.Stato}")
    else:
            print(f"Nessun ordine trovato per il cliente con ID {id_cliente}.")

# - Visualizzare le recensioni relative ad un prodotto
def recensioni_prodotto(id_prodotto):
    recensioni = session.query(Recensione).filter_by(ID_Prodotto=id_prodotto).all()
    if recensioni:
        for recensione in recensioni:
            print(f"ID Recensione: {recensione.ID_Recensione}, Valutazione: {recensione.Valutazione},"
                  f"Commento: {recensione.Commento}")
    else:
        print(f"Nessuna recensione trovata per il prodotto con ID {id_prodotto}.")

# - Lista di prodotti all'interno di un ordine
def prodotti_in_ordine(id_ordine):
    prodotti = session.query(OrdineProdotto).filter_by(ID_Ordine=id_ordine).all()
    if prodotti:
        for prodotto in prodotti:
            prod = session.query(Prodotto).filter_by(ID_Prodotto=prodotto.ID_Prodotto).first()
            print(f"ID Prodotto: {prod.ID_Prodotto}, Titolo: {prod.Titolo}, Quantita: {prod.Quantita}")
    else:
        print(f"Nessuna prodotto trovato per l'ordine con ID {id_ordine}.")

# - Lista di prodotti all'interno di una wishlist
def prodotti_in_wishlist(id_wishlist):
    prodotti = session.query(WishlistProdotto).filter_by(ID_Wishlist=id_wishlist).all()
    if prodotti:
        for prodotto in prodotti:
            prod = session.query(Prodotto).filter_by(ID_Prodotto=prodotto.ID_Prodotto).first()
            print(f"ID Prodotto: {prod.ID_Prodotto}, Titolo: {prod.Titolo}, Quantita: {prod.Quantita}")
    else:
        print(f"Nessun prodotto trovato nella wishlist con ID {id_wishlist}.")

#UPDATE - Aggiornare i dati di un cliente
def aggiorna_cliente(id_cliente, nuovo_nome=None, nuovo_cognome=None, nuova_email=None, nuovo_telefono=None,
                     nuova_password=None):
    cliente = session.query(Cliente).filter_by(ID_Cliente=id_cliente).first()
    if cliente:
        if nuovo_nome:
            cliente.Nome = nuovo_nome
        if nuovo_cognome:
            cliente.Cognome = nuovo_cognome
        if nuova_email:
            cliente.Email = nuova_email
        if nuovo_telefono:
            cliente.Telefono = nuovo_telefono
        if nuova_password:
            cliente.Password = nuova_password
        session.commit()
        print(f"I dati del cliente {id_cliente} sono stati aggiornati con successo!")
    else:
        print("Cliente non trovato.")

# - Aggiorna i dati di un amministratore
def aggiorna_amministratore(id_amministratore, nuovo_nome=None, nuovo_cognome=None, nuova_email=None,
                            nuovo_telefono=None, nuova_password=None):
    amministratore = session.query(Amministratore).filter_by(ID_Amministratore=id_amministratore).first()
    if amministratore:
        if nuovo_nome:
            amministratore.Nome = nuovo_nome
        if nuovo_cognome:
            amministratore.Cognome = nuovo_cognome
        if nuova_email:
            amministratore.Email = nuova_email
        if nuovo_telefono:
            amministratore.Telefono = nuovo_telefono
        if nuova_password:
            amministratore.Password= nuova_password
        session.commit()
        print(f"I dati dell'amministratore {id_amministratore} sono stati aggiornati con successo!")
    else:
        print("Amministratore non trovato.")

# - Aggiornare la quantità dei prodotti all'interno del magazzino
def aggiorna_quantita_prodotto(id_prodotto, nuova_quantita):
    prodotto = session.query(Prodotto).filter_by(ID_Prodotto=id_prodotto).first()
    if prodotto:
        magazzino = session.query(Magazzino).filter_by(ID_Magazzino=prodotto.ID_Magazzino).first()
        if magazzino:
            magazzino.QunatitaProdotto = nuova_quantita
            session.commit()
            print(f"Quantità di '{prodotto.Titolo}' aggiornata a {nuova_quantita}.")
        else:
            print(f"Il prodotto con ID {id_prodotto} non è stato trovato all'interno del magazzino.")
    else:
        print(f"Il prodotto con ID {id_prodotto} non è stato trovato.")

# - Aggiornare i dati di un prodotto
def aggiorna_prodotto(id_prodotto, nuovo_titolo=None, nuova_descrizione=None, nuova_categoria=None,
                      nuova_piattaforma=None, nuovo_prezzo=None):
    prodotto = session.query(Prodotto).filter_by(ID_Prodotto=id_prodotto).first()
    if prodotto:
        if nuovo_titolo:
            prodotto.Titolo = nuovo_titolo
        if nuova_descrizione:
            prodotto.Descrizione = nuova_descrizione
        if nuova_categoria:
            prodotto.Categoria = nuova_categoria
        if nuova_piattaforma:
            prodotto.PiattaForma = nuova_piattaforma
        if nuovo_prezzo:
            prodotto.Prezzo = nuovo_prezzo
        session.commit()
        print(f"Il prodotto con ID {id_prodotto} è stato aggiornato con successo!")
    else:
        print(f"Prodotto con ID {id_prodotto} non è stato trovato.")

# - Aggiornare lo stato degli ordini
def aggiorna_stato_ordine(id_ordine, nuovo_stato):
    ordine = session.query(Ordine).filter_by(ID_Ordine=id_ordine).first()
    if ordine:
        ordine.Stato= nuovo_stato
        session.commit()
        print(f"Lo stato dell'ordine con ID {id_ordine} è stato aggiornato a '{nuovo_stato}'.")
    else:
        print(f"L'ordine con ID {id_ordine} non è stato trovato.")

#DELETE - Eliminare un cliente
def elimina_cliente(email):
    cliente = session.query(Cliente).filter_by(Email=email).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        print(f"Cliente {email} eliminato con successo!")
    else:
        print("Cliente non trovato.")

# - Eliminare un amministratore
def elimina_amministratore(email):
    amministratore = session.query(Amministratore).filter_by(Email=email).first()
    if amministratore:
        session.delete(amministratore)
        session.commit()
        print(f"Amministratore {email} eliminato con successo!")
    else:
        print("Amministratore non trovato.")

 # - Eliminare un prodotto
def elimina_prodotto(id_prodotto):
    prodotto = session.query(Prodotto).filter_by(ID_Prodotto=id).first()
    if prodotto:
        session.delete(prodotto)
        session.commit()
        print(f"Prodotto con ID {id_prodotto} è stato eliminato con successo!")
    else:
        print(f"Il prodotto con ID {id_prodotto} non è stato trovato.")

 # - Eliminare un ordine
def elimina_ordine(id_ordine):
     ordine = session.query(Ordine).filter_by(ID_Ordine=id_ordine).first()
     if ordine:
         session.query(OrdineProdotto).filter_by(ID_Ordine=id_ordine).delete()
         session.delete(ordine)
         session.commit()
         print(f"L'ordine con ID {id_ordine} eliminato con successo!")
     else:
         print(f"L'ordine con ID {id_ordine} non trovato.")

 # - Eliminare una recensione
def elimina_recensione(id_recensione):
     recensione = session.query(Recensione).filter_by(ID_Recensione=id_recensione).first()
     if recensione:
         session.delete(recensione)
         session.commit()
         print(f"Recensione con ID {id_recensione} eliminata con successo!")
     else:
         print(f"Recensione con ID {id_recensione} non trovata.")

 # - Eliminare una wishlist
def elimina_wishlist(id_wishlist):
     wishlist = session.query(Wishlist).filter_by(ID_Wishlist=id_wishlist).first()
     if wishlist:
         session.query(WishlistProdotto).filter_by(ID_Wishlist=id_wishlist).delete()
         session.delete(wishlist)
         session.commit()
         print(f"Wishlist con ID {id_wishlist} eliminata con successo!")
     else:
         print(f"Wishlist con ID {id_wishlist} non trovata.")

 # - Rimozione di un prodotto all'interno di un'ordine
def rimuovi_prodotto_da_ordine(id_ordine, id_prodotto):
     ordine_prodotto = session.query(OrdineProdotto).filter_by(ID_Ordine=id_ordine, ID_Prodotto=id_prodotto).first()
     if ordine_prodotto:
         session.delete(ordine_prodotto)
         session.commit()
         print(f"Prodotto con ID {id_prodotto} rimosso dall'ordine {id_ordine}.")
     else:
         print(f"Prodotto con ID {id_prodotto} non trovato nell'ordine {id_ordine}.")

 # - Rimozione di un prodotto all'interno di una wishlist
def rimuovi_prodotto_da_wishlist(id_wishlist, id_prodotto):
    wishlist_prodotto = session.query(WishlistProdotto).filter_by(ID_Wishlist=id_wishlist,
                                                                  ID_Prodotto=id_prodotto).first()
    if wishlist_prodotto:
        session.delete(wishlist_prodotto)
        session.commit()
        print(f"Prodotto con ID {id_prodotto} rimosso dall'wishlist {id_wishlist}.")
    else:
        print(f"Prodotto con ID {id_prodotto} non trovato nella wishlist {id_wishlist}.")