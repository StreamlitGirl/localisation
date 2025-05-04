from flask import Flask, request, jsonify
import mysql.connector
import requests
from fastapi import FastAPI, Query
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)
@app.route('/api/address', methods=['GET'])

def getAdress():
    mail = request.args.get('mail')
    try:
        connection = mysql.connector.connect(
            host='mysql.railway.internal',
            user="root",
            password="waNRyNtpGEtXaaqQiDPCuACUAPhsFLZS",
            database="railway"
        )
        if connection.is_connected():
            sql = f"SELECT location FROM docteur WHERE Mail = %s"
            if sql:
                cursor = connection.cursor()
                cursor.execute(sql, (mail,))

                location = cursor.fetchall()
                if location:
                    msg = location[0][0]
                    success = True
                else:
                    success = False
                    msg = "medecin ou localisation de medecin non trouvé"
            else:
                msg = "probleme de requete sql"
                success = False
        else:
            msg = "probleme de connection a la database"
            success = False
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)})

    return jsonify({"success": success, "msg": msg})

@app.route('/api/changeAddress', methods=['PUT'])
def changeAddress():
    data = request.get_json()
    mail = data.get('mail')
    location = data.get('change')
    try:
        connection = mysql.connector.connect(
            host='mysql.railway.internal',
            user="root",
            password="waNRyNtpGEtXaaqQiDPCuACUAPhsFLZS",
            database="railway"
        )
        if connection.is_connected():
            sql = f"UPDATE docteur SET location = %s WHERE Mail = %s"
            if sql:
                cursor = connection.cursor()
                cursor.execute(sql, (location, mail))
                sqlVerif =  f"SELECT location FROM docteur WHERE Mail = %s""
                if sqlVerif:
                    cursorVerif =  connection.cursor()
                    cursorVerif.execute(sqlVerif, (location, mail))
                    verifier = cursorVerif.fetchone();
                    if verifier:
                        msg = verifier[0]
                        success = True
                    else :
                        msg = "update n a pas réussie ";
                        success = False;
                        
                
                    
                
                
                connection.commit()
               
            else:
                success = False
                msg = "Probleme de requete SQL"
        else:
            success = False
            msg = "Probleme de connection a la database"
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)})

    return jsonify({"success": success, "msg": msg})


    
    




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
   
