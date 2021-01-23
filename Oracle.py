import cx_Oracle

def consulta_fones():
    try:
        connection = cx_Oracle.connect('USER_BOT_PORTABILIDADE/bot%1@10.6.4.66:1521/DMBD')
    except Exception as e:
        print(e.__str__())

    bloco = connection.cursor().var(cx_Oracle.CURSOR)
    connection.cursor().callproc("BOT_PORTABILIDADE.SP_RESERVA", [700,bloco])
    phones_list = []

    for pk,phone in bloco.getvalue().fetchall():
        phones_list.append({'pk':pk,'phone':phone})

    return phones_list