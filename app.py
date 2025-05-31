# Author: Bugheciu Stefan, Universitatea Transilvania
# Description: This is a Flask App that uses SQLite3 to
# execute (C)reate, (R)ead, (U)pdate, (D)elete operations

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

# Route to add a new record (INSERT) student data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            nume = request.form['nume']
            prenume = request.form['prenume'] #ceea ce este inclus intre [], reprezinta numele campurilor transmise de catre formularul din student.html
            scoala = request.form['scoala']
            telefon = request.form['telefon']
            emisfera = request.form['emisfera']
            personalitate = request.form['personalitate']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO elevi (nume, prenume, scoala, numar_de_telefon, predominanta_de_emisfera, tipologia_de_personalitate) VALUES (?,?,?,?,?,?)",
                            (nume, prenume, scoala, telefon, emisfera, personalitate))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route to SELECT all data from the database and display in a table      
@app.route('/list', methods=['GET'])
def list():
    selected_table = request.args.get('table', 'persoane')
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM persoane")
    persoane = cur.fetchall()
    cur.execute("SELECT * FROM profil_psihologic")
    profil_psihologic = cur.fetchall()
    cur.execute("SELECT * FROM educatie")
    educatie = cur.fetchall()
    cur.execute("SELECT * FROM experienta_profesionala")
    experienta_profesionala = cur.fetchall()
    cur.execute("SELECT * FROM familie")
    familie = cur.fetchall()
    cur.execute("SELECT * FROM firme")
    firme = cur.fetchall()

    con.close()
    return render_template(
        "list.html",
        persoane=persoane,
        profil_psihologic=profil_psihologic,
        educatie=educatie,
        experienta_profesionala=experienta_profesionala,
        familie=familie,
        firme=firme,
        selected_table=selected_table
    )

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM elevi WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            nume = request.form['nume']
            prenume = request.form['prenume']
            scoala = request.form['scoala']
            telefon = request.form['telefon']
            emisfera = request.form['emisfera']
            personalitate = request.form['personalitate']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE elevi SET nume='"+nume+"', prenume='"+prenume+"', scoala='"+scoala+"', numar_de_telefon='"+telefon+"', predominanta_de_emisfera='"+emisfera+"', tipologia_de_personalitate='"+personalitate+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE elevi SET nume='"+nume+"', prenume='"+prenume+"', scoala='"+scoala+"', numar_de_telefon='"+telefon+"', predominanta_de_emisfera='"+emisfera+"', tipologia_de_personalitate='"+personalitate+"' WHERE rowid="+rowid
        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM elevi WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

@app.route('/add_persoana', methods=['POST'])
def add_persoana():
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        sex = request.form.get('sex')
        varsta = request.form.get('varsta')
        tip_client = request.form.get('tip_client')
        numar_de_telefon = request.form.get('numar_de_telefon')
        adresa = request.form.get('adresa')
        oras = request.form.get('oras')
        permis_conducere = 1 if request.form.get('permis_conducere') else 0
        abonament_platit = 1 if request.form.get('abonament_platit') else 0
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO persoane (nume, prenume, sex, varsta, tip_client, numar_de_telefon, adresa, oras, permis_conducere, abonament_platit) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (nume, prenume, sex, varsta, tip_client, numar_de_telefon, adresa, oras, permis_conducere, abonament_platit))
            con.commit()
        return redirect(url_for('list'))

@app.route('/add_profil_psihologic', methods=['POST'])
def add_profil_psihologic():
    if request.method == 'POST':
        id_persoana = request.form['id_persoana']
        predominanta_de_emisfera = request.form.get('predominanta_de_emisfera')
        tipologia_de_personalitate = request.form.get('tipologia_de_personalitate')
        intentii_viitoare = request.form.get('intentii_viitoare')
        hobbyuri = request.form.get('hobbyuri')
        preferinte_job = request.form.get('preferinte_job')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO profil_psihologic (id_persoana, predominanta_de_emisfera, tipologia_de_personalitate, intentii_viitoare, hobbyuri, preferinte_job) VALUES (?,?,?,?,?,?)",
                        (id_persoana, predominanta_de_emisfera, tipologia_de_personalitate, intentii_viitoare, hobbyuri, preferinte_job))
            con.commit()
        return redirect(url_for('list'))

@app.route('/add_educatie', methods=['POST'])
def add_educatie():
    if request.method == 'POST':
        id_persoana = request.form['id_persoana']
        nivel = request.form.get('nivel')
        scoala = request.form.get('scoala')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO educatie (id_persoana, nivel, scoala) VALUES (?,?,?)",
                        (id_persoana, nivel, scoala))
            con.commit()
        return redirect(url_for('list'))

@app.route('/add_experienta_profesionala', methods=['POST'])
def add_experienta_profesionala():
    if request.method == 'POST':
        id_persoana = request.form['id_persoana']
        loc_de_lucru_anterior = request.form.get('loc_de_lucru_anterior')
        experienta_anterioara = request.form.get('experienta_anterioara')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO experienta_profesionala (id_persoana, loc_de_lucru_anterior, experienta_anterioara) VALUES (?,?,?)",
                        (id_persoana, loc_de_lucru_anterior, experienta_anterioara))
            con.commit()
        return redirect(url_for('list'))

@app.route('/add_familie', methods=['POST'])
def add_familie():
    if request.method == 'POST':
        id_persoana = request.form['id_persoana']
        parinti = request.form.get('parinti')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO familie (id_persoana, parinti) VALUES (?,?)",
                        (id_persoana, parinti))
            con.commit()
        return redirect(url_for('list'))

@app.route('/add_firma', methods=['POST'])
def add_firma():
    if request.method == 'POST':
        nume_firma = request.form['nume_firma']
        nr_angajati = request.form.get('nr_angajati')
        locuri_disponibile = request.form.get('locuri_disponibile')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO firme (nume_firma, nr_angajati, locuri_disponibile) VALUES (?,?,?)",
                        (nume_firma, nr_angajati, locuri_disponibile))
            con.commit()
        return redirect(url_for('list'))

@app.route('/delete_persoana', methods=['POST'])
def delete_persoana():
    id = request.form['id']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM persoane WHERE id=?', (id,))
        con.commit()
    return redirect(url_for('list'))

@app.route('/delete_profil_psihologic', methods=['POST'])
def delete_profil_psihologic():
    id_profil = request.form['id_profil']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM profil_psihologic WHERE id_profil=?', (id_profil,))
        con.commit()
    return redirect(url_for('list'))

@app.route('/delete_educatie', methods=['POST'])
def delete_educatie():
    id_educatie = request.form['id_educatie']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM educatie WHERE id_educatie=?', (id_educatie,))
        con.commit()
    return redirect(url_for('list'))

@app.route('/delete_experienta_profesionala', methods=['POST'])
def delete_experienta_profesionala():
    id_exp = request.form['id_exp']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM experienta_profesionala WHERE id_exp=?', (id_exp,))
        con.commit()
    return redirect(url_for('list'))

@app.route('/delete_familie', methods=['POST'])
def delete_familie():
    id_familie = request.form['id_familie']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM familie WHERE id_familie=?', (id_familie,))
        con.commit()
    return redirect(url_for('list'))

@app.route('/delete_firma', methods=['POST'])
def delete_firma():
    id_firma = request.form['id_firma']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM firme WHERE id_firma=?', (id_firma,))
        con.commit()
    return redirect(url_for('list'))

@app.route('/edit_persoana', methods=['POST'])
def edit_persoana():
    id = request.form['id']
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM persoane WHERE id=?', (id,))
        persoana = cur.fetchone()
    return render_template('edit.html', entity='persoana', data=persoana)

@app.route('/edit_profil_psihologic', methods=['POST'])
def edit_profil_psihologic():
    id_profil = request.form['id_profil']
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM profil_psihologic WHERE id_profil=?', (id_profil,))
        profil = cur.fetchone()
    return render_template('edit.html', entity='profil_psihologic', data=profil)

@app.route('/edit_educatie', methods=['POST'])
def edit_educatie():
    id_educatie = request.form['id_educatie']
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM educatie WHERE id_educatie=?', (id_educatie,))
        educatie = cur.fetchone()
    return render_template('edit.html', entity='educatie', data=educatie)

@app.route('/edit_experienta_profesionala', methods=['POST'])
def edit_experienta_profesionala():
    id_exp = request.form['id_exp']
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM experienta_profesionala WHERE id_exp=?', (id_exp,))
        exp = cur.fetchone()
    return render_template('edit.html', entity='experienta_profesionala', data=exp)

@app.route('/edit_familie', methods=['POST'])
def edit_familie():
    id_familie = request.form['id_familie']
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM familie WHERE id_familie=?', (id_familie,))
        familie = cur.fetchone()
    return render_template('edit.html', entity='familie', data=familie)

@app.route('/edit_firma', methods=['POST'])
def edit_firma():
    id_firma = request.form['id_firma']
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM firme WHERE id_firma=?', (id_firma,))
        firma = cur.fetchone()
    return render_template('edit.html', entity='firma', data=firma)

@app.route('/update_persoana', methods=['POST'])
def update_persoana():
    id = request.form['id']
    nume = request.form['nume']
    prenume = request.form['prenume']
    sex = request.form.get('sex')
    varsta = request.form.get('varsta')
    tip_client = request.form.get('tip_client')
    numar_de_telefon = request.form.get('numar_de_telefon')
    adresa = request.form.get('adresa')
    oras = request.form.get('oras')
    permis_conducere = 1 if request.form.get('permis_conducere') else 0
    abonament_platit = 1 if request.form.get('abonament_platit') else 0
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE persoane SET nume=?, prenume=?, sex=?, varsta=?, tip_client=?, numar_de_telefon=?, adresa=?, oras=?, permis_conducere=?, abonament_platit=? WHERE id=?",
                    (nume, prenume, sex, varsta, tip_client, numar_de_telefon, adresa, oras, permis_conducere, abonament_platit, id))
        con.commit()
    return redirect(url_for('list'))

@app.route('/update_profil_psihologic', methods=['POST'])
def update_profil_psihologic():
    id_profil = request.form['id_profil']
    id_persoana = request.form['id_persoana']
    predominanta_de_emisfera = request.form.get('predominanta_de_emisfera')
    tipologia_de_personalitate = request.form.get('tipologia_de_personalitate')
    intentii_viitoare = request.form.get('intentii_viitoare')
    hobbyuri = request.form.get('hobbyuri')
    preferinte_job = request.form.get('preferinte_job')
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE profil_psihologic SET id_persoana=?, predominanta_de_emisfera=?, tipologia_de_personalitate=?, intentii_viitoare=?, hobbyuri=?, preferinte_job=? WHERE id_profil=?",
                    (id_persoana, predominanta_de_emisfera, tipologia_de_personalitate, intentii_viitoare, hobbyuri, preferinte_job, id_profil))
        con.commit()
    return redirect(url_for('list'))

@app.route('/update_educatie', methods=['POST'])
def update_educatie():
    id_educatie = request.form['id_educatie']
    id_persoana = request.form['id_persoana']
    nivel = request.form.get('nivel')
    scoala = request.form.get('scoala')
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE educatie SET id_persoana=?, nivel=?, scoala=? WHERE id_educatie=?",
                    (id_persoana, nivel, scoala, id_educatie))
        con.commit()
    return redirect(url_for('list'))

@app.route('/update_experienta_profesionala', methods=['POST'])
def update_experienta_profesionala():
    id_exp = request.form['id_exp']
    id_persoana = request.form['id_persoana']
    loc_de_lucru_anterior = request.form.get('loc_de_lucru_anterior')
    experienta_anterioara = request.form.get('experienta_anterioara')
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE experienta_profesionala SET id_persoana=?, loc_de_lucru_anterior=?, experienta_anterioara=? WHERE id_exp=?",
                    (id_persoana, loc_de_lucru_anterior, experienta_anterioara, id_exp))
        con.commit()
    return redirect(url_for('list'))

@app.route('/update_familie', methods=['POST'])
def update_familie():
    id_familie = request.form['id_familie']
    id_persoana = request.form['id_persoana']
    parinti = request.form.get('parinti')
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE familie SET id_persoana=?, parinti=? WHERE id_familie=?",
                    (id_persoana, parinti, id_familie))
        con.commit()
    return redirect(url_for('list'))

@app.route('/update_firma', methods=['POST'])
def update_firma():
    id_firma = request.form['id_firma']
    nume_firma = request.form['nume_firma']
    nr_angajati = request.form.get('nr_angajati')
    locuri_disponibile = request.form.get('locuri_disponibile')
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE firme SET nume_firma=?, nr_angajati=?, locuri_disponibile=? WHERE id_firma=?",
                    (nume_firma, nr_angajati, locuri_disponibile, id_firma))
        con.commit()
    return redirect(url_for('list'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    tables = {
        'persoane': ['nume', 'prenume', 'sex', 'varsta', 'tip_client', 'numar_de_telefon', 'adresa', 'oras', 'permis_conducere', 'abonament_platit'],
        'profil_psihologic': ['id_persoana', 'predominanta_de_emisfera', 'tipologia_de_personalitate', 'intentii_viitoare', 'hobbyuri', 'preferinte_job'],
        'educatie': ['id_persoana', 'nivel', 'scoala'],
        'experienta_profesionala': ['id_persoana', 'loc_de_lucru_anterior', 'experienta_anterioara'],
        'familie': ['id_persoana', 'parinti'],
        'firme': ['nume_firma', 'nr_angajati', 'locuri_disponibile']
    }
    results = None
    selected_table = None
    selected_field = None
    search_value = None
    if request.method == 'POST':
        selected_table = request.form['table']
        selected_field = request.form['field']
        search_value = request.form['value']
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            query = f"SELECT * FROM {selected_table} WHERE {selected_field} LIKE ?"
            cur.execute(query, (f"%{search_value}%",))
            results = cur.fetchall()
    return render_template('search.html', tables=tables, results=results, selected_table=selected_table, selected_field=selected_field, search_value=search_value)

# Pornire server Flask corectă
if __name__ == '__main__':
    print("Flask server starting...")
    app.run(debug=True)