#pip install flask-mysqldb

from flask import Flask ,render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
###############################################
#   Index
###############################################
@app.route('/')
def index():
    return render_template('index.html')

##############################################
#MYSQL-Konfiguration
##############################################

app.config['MYSQL_Host'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_43345_schule'

mysql = MySQL(app)
#mysql.init_app(app)
###################################################
#   schüler
###################################################

@app.route('/schüler', methods=['GET','POST'])
def schueler():
    #verbindung mit Datenbank herstellen
    cursor = mysql.connection.cursor()
    #SQL Abfrage
    query = '''
            SELECT tbl_klassen.Bezeichnung,
                tbl_raeume.Bezeichnung,
                tbl_lehrer.Vorname,
                tbl_lehrer.Nachname,
                tbl_schueler.Vorname,
                tbl_schueler.Nachname
            FROM tbl_klassen
            INNER JOIN tbl_raeume ON tbl_klassen.FIDRaum = tbl_raeume.IDRaum
            INNER JOIN tbl_lehrer ON tbl_klassen.FIDKV = tbl_lehrer.IDLehrer
            INNER JOIN tbl_schueler ON tbl_klassen.IDKlasse = tbl_schueler.FIDKlasse\n
    '''
    # abfragen ob Post daten erhalten sind für suche
    if request.method == 'POST':
        if request.form['VN'] and request.form['NN']:
            query_search = request.form['VN'], request.form['NN']
            query += f'''\n WHERE tbl_schueler.Vorname LIKE '%{query_search[0]}%' and tbl_schueler.Nachname LIKE '%{query_search[1]}%';
        '''
       # print(query)

        if request.form['VN']:
            query_search = request.form['VN']
            query += f'''\n WHERE tbl_schueler.Vorname LIKE '%{query_search}%' '''
            print(query_search)



            #print(query_vn)
        if request.form['NN']:
            query_search = request.form['NN']
            print(query_search)
            query += f'''
                    WHERE tbl_schueler.Nachname LIKE '%{query_search}%'\n
            '''

            #print(query_nn)




    cursor.execute(query)
    schueler = cursor.fetchall()

    print(schueler)
    return render_template('schüler.html',schueler=schueler)


@app.route('/räume')
def raeume():
    #Verbindung zur Datenbank
    cursor = mysql.connection.cursor()

    query = '''
            SELECT tbl_raeume.*,
            tbl_klassen.Bezeichnung
            FROM tbl_raeume
            LEFT JOIN tbl_klassen ON tbl_raeume.IDRaum = tbl_klassen.FIDRaum
    '''
    cursor.execute(query)
    raeume = cursor.fetchall()
    print(raeume)
    return render_template('räume.html',raeume=raeume)



if __name__ == '__main__':
    app.run(debug=True)