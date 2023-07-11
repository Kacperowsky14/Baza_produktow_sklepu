import tkinter as tk
from tkinter import ttk
import psycopg2

#Funkcja słuząca do obsługi pokazywania produktu
def show_products(product_type):
    selected_product = products_list[product_type].get()
    for product in products[product_type]:
        if product[1] == selected_product:
            product_price = product[2]
            label_price.config(text="Cena: " + str(product_price) + " zł")
            break

#Funkcja dodająca nowy produkt 
def add_product(product_type):
    name = new_product_entry.get()
    price = new_product_price_entry.get()

    if name and price:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="mydatabase",
            user="postgres",
            password="password"
        )

        c = conn.cursor()
        #Pobranie najwyzszego id produktu i dodanie id o jeden większy do dodanego produktu 
        if product_type == "rtv":
            c.execute("SELECT MAX(id_produktu) FROM produkty_rtv")
        elif product_type == "agd":
            c.execute("SELECT MAX(id_produktu) FROM produkty_agd")
        max_id = c.fetchone()[0]
        new_product_id = max_id + 1 if max_id is not None else 1
        

        if product_type == "rtv":
            c.execute("INSERT INTO produkty_rtv (id_produktu, nazwa_produktu, cena) VALUES (%s, %s, %s)", (new_product_id, name, price))
        elif product_type == "agd":
            c.execute("INSERT INTO produkty_agd (id_produktu, nazwa_produktu, cena) VALUES (%s, %s, %s)", (new_product_id, name, price))

        conn.commit()
        conn.close()

        refresh_product_list(product_type)

        new_product_entry.delete(0, tk.END)
        new_product_price_entry.delete(0, tk.END)
    else:
        tk.messagebox.showwarning("Błąd", "Proszę podać nazwę i cenę produktu.")

#Funkcja, która zajmuje się odswiezeniem listy produktów 
def refresh_product_list(product_type):
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="mydatabase",
        user="postgres",
        password="password"
    )

    c = conn.cursor()
    #Zastosowanie zapytań SQL do pobrania wartości tabel
    if product_type == "rtv":
        c.execute("SELECT * FROM produkty_rtv")
        products_rtv = c.fetchall()
        products_list_rtv['values'] = [product[1] for product in products_rtv]
        products["rtv"] = products_rtv
    elif product_type == "agd":
        c.execute("SELECT * FROM produkty_agd")
        products_agd = c.fetchall()
        products_list_agd['values'] = [product[1] for product in products_agd]
        products["agd"] = products_agd

    conn.close()


if __name__ == "__main__":

    # Nawiązanie połączenia z bazą danych
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="mydatabase",
        user="postgres",
        password="password"
    )

    root = tk.Tk()
    root.title("Sklep z produktami")
    notebook = ttk.Notebook(root)
    notebook.pack()

    tab_rtv = ttk.Frame(notebook)
    notebook.add(tab_rtv, text="Produkty RTV")
            
    tab_agd = ttk.Frame(notebook)
    notebook.add(tab_agd, text="Produkty AGD")

    c = conn.cursor()

    c.execute("SELECT * FROM produkty_rtv")
    products_rtv = c.fetchall()

    c.execute("SELECT * FROM produkty_agd")
    products_agd = c.fetchall()

    c.close()

    #Przycisk do wyświetlania ceny produktów agd i rtv
    products_list_rtv = ttk.Combobox(tab_rtv, values=[product[1] for product in products_rtv])
    products_list_rtv.pack()
    button_rtv = tk.Button(tab_rtv, text="Pokaż cenę produktu", command=lambda: show_products("rtv"))
    button_rtv.pack()

    products_list_agd = ttk.Combobox(tab_agd, values=[product[1] for product in products_agd])
    products_list_agd.pack()
    button_agd = tk.Button(tab_agd, text="Pokaż cenę produktu", command=lambda: show_products("agd"))
    button_agd.pack()

    
    label_price = tk.Label(root, text="Cena:")
    label_price.pack()

    # Słownik przechowujący rozwijane listy
    products_list = {
        "rtv": products_list_rtv,
        "agd": products_list_agd
    }

    # Słownik przechowujący wyniki dla każdej kategorii produktów
    products = {
        "rtv": products_rtv,
        "agd": products_agd
    }

    #Dodawanie produkt
    new_product_label = tk.Label(root, text="Dodaj produkt")
    new_product_label.pack()

    new_product_entry = tk.Entry(root)
    new_product_entry.pack()

    #Wprowadzenie ceny nowego produktu
    new_product_price_label = tk.Label(root, text="Cena:")
    new_product_price_label.pack()

    new_product_price_entry = tk.Entry(root)
    new_product_price_entry.pack()

    add_rtv_button = tk.Button(tab_rtv, text="Dodaj produkt", command=lambda: add_product("rtv"))
    add_rtv_button.pack()
    add_agd_button = tk.Button(tab_agd, text="Dodaj produkt", command=lambda: add_product("agd"))
    add_agd_button.pack()

    refresh_product_list("rtv")
    refresh_product_list("agd")

    root.mainloop()
    conn.close()

