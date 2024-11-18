

from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'stock'

mysql = MySQL(app)

data = []
options = []
codes = []
data1 = []
supplierID = 0
itemNumber = 0
ino = 0


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    return render_template('login.html', msg=msg)


@app.route('/admin')
def admin():
    msg = ''
    return render_template('admin.html', msg=msg)


@app.route('/dasboard')
def dasboard():
    msg = ''
    return render_template('dasboard.html', msg=msg)


@app.route('/bill', methods=['GET', 'POST'])
def bill():
    user = []
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT pdate, purchaseID, supplierID, itemNumber, itemName, quantity, fquantity, unitprice, Amount, sgst, cgst, netAmountInput, cmts, status FROM pform order by purchaseID desc')
    users = cursor.fetchone()
    cursor.close()
    return render_template('bill.html', user=users, users=user)


@app.route('/listt', methods=['GET', 'POST'])
def listt():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT sid FROM supplier')
        options = cursor.fetchall()
        cursor.execute('SELECT code, name, qty, units, cp, sp, si, ro, exp, date, sg, cg, img FROM listt')
        users = cursor.fetchall()
        cursor.close()
        return render_template('listt.html', options=options, users=users)

    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        qty = request.form['qty']
        units = request.form['units']
        cp = request.form['cp']
        sp = request.form['sp']
        si = request.form.get('si')
        ro = request.form['ro']
        exp = request.form['exp']
        date = request.form['date']
        sg = request.form['sg']
        cg = request.form['cg']
        img = request.form['img']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO listt VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)''',
                       (code, name, qty, units, cp, sp, si, ro, exp, date, sg, cg, img))
        mysql.connection.commit()

        cursor.execute('SELECT code, name, qty, units, cp, sp, si, ro, exp, date, sg, cg, img FROM listt')
        users = cursor.fetchall()
        cursor.close()
        return render_template('listt.html', users=users)


@app.route('/updatelistt', methods=['POST', 'GET'])
def updatelistt():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        qty = request.form['qty']
        units = request.form['units']
        cp = request.form['cp']
        sp = request.form['sp']
        si = request.form.get('si')
        ro = request.form['ro']
        exp = request.form['exp']
        date = request.form['date']
        sg = request.form['sg']
        cg = request.form['cg']
        img = request.form['img']
        cursor = mysql.connection.cursor()
        cursor.execute(
            """ UPDATE listt SET code=%s, name=%s, qty=%s, units=%s, cp=%s, sp=%s, si=%s, ro=%s, exp=%s, date=%s, sg=%s, cg=%s, img=%s WHERE code=%s """,
            (code, name, qty, units, cp, sp, si, ro, exp, date, sg, cg, img, code))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('listt'))


@app.route('/deletelistt/<string:code>', methods=['GET'])
def deletelistt(code):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM listt WHERE code=%s", (code,))
    mysql.connection.commit()
    return redirect(url_for('listt'))


@app.route('/pform', methods=['GET', 'POST'])
def pform():
    global data, options, codes, data1, supplierID, itemNumber  # declare data as global

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT sid,sname FROM supplier')
        options = cursor.fetchall()

        cursor.execute('SELECT code, name FROM listt')
        codes = cursor.fetchall()
        cursor.close()
        return render_template('pform.html', data1=data1, codes=codes, data=data, options=options)


    print(1)
    if request.method == 'POST':
        print(2)

        if request.form.get('itemName') == "":
            #supplierID = request.form.get('supplierID')
            print(supplierID)
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT sname FROM supplier WHERE sid = %s', (supplierID,))
            data = cursor.fetchone()
            cursor.close()

            itemNumber = request.form.get('itemNumber')
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT name, sp, sg, cg FROM listt WHERE code = %s''', (itemNumber,))
            data1 = cursor.fetchall()
            cursor.close()
            data = []
            return render_template('pform.html', data=data, data1=data1, options=options, codes=codes, supplierID=supplierID)

        else:
            cursor = mysql.connection.cursor()
            pdate = request.form.get('pdate')
            purchaseID = request.form.get('purchaseID')
            purchaseDate = request.form.get('purchaseDate')
            supplierID = request.form.get('supplierID')
            cursor.execute('SELECT sid,sname FROM supplier where sname=%s',(supplierID,))
            dr = cursor.fetchone()
            supplierID=dr[0]
            supplier = request.form.get('supplier')
            deliverPerson = request.form.get('deliverPerson')
            deliverContact = request.form.get('deliverContact')
            itemNumber = request.form.get('itemNumber')
            cursor.execute('''SELECT code, sp, sg, cg FROM listt WHERE name = %s''', (itemNumber,))
            dr = cursor.fetchone()
            itemNumber = dr[0]
            itemName = request.form.get('itemName')
            quantity = request.form.get('quantity')
            fquantity = request.form.get('fquantity')
            unitprice = request.form.get('unitprice')
            Amount = request.form.get('Amount')
            sgst = request.form.get('sgst')
            cgst = request.form.get('cgst')
            netAmountInput = request.form.get('netAmountInput')
            cmts = request.form.get('cmts')
            status = request.form.get('status')
            print(pdate, purchaseID, purchaseDate, supplierID, supplier, deliverPerson, deliverContact, itemNumber,
                  itemName, quantity, fquantity, unitprice, Amount, sgst, cgst, netAmountInput, cmts, status)

            cursor.execute(
                '''INSERT INTO pform VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (pdate, purchaseID, purchaseDate, supplierID, supplier, deliverPerson, deliverContact, itemNumber, itemName,
                quantity, fquantity, unitprice, Amount, sgst, cgst, netAmountInput, cmts, status))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor()
            code = request.form.get('code')
            cursor.execute("""UPDATE listt SET qty=qty+%s WHERE code = %s""", (code, quantity,))
            mysql.connection.commit()
            cursor.close()
        return redirect(url_for('bill'))


@app.route('/purchasedetails', methods=['GET', 'POST'])
def purchasedetails():
    user = []
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT pdate, purchaseID, purchaseDate, supplierID, supplier, deliverPerson, deliverContact, itemNumber, itemName, quantity, fquantity, unitprice, Amount, sgst, cgst, netAmountInput, cmts, status FROM pform')
    users = cursor.fetchall()
    cursor.close()
    return render_template('purchasedetails.html', users=users, user=user)


@app.route('/Sform', methods=['GET', 'POST'])
def Sform():
    global ino, data1
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT code,name FROM listt')
        codes = cursor.fetchall()
        cursor.close()
        return render_template('Sform.html', codes=codes, data1=data1)

    if request.method == 'POST':
        if request.form.get('iname') == "":
            ino = request.form.get('ino')
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT name, sp, sg, cg FROM listt WHERE code = %s''', (ino,))
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('sform.html', data1=data1)
        else:
            cursor = mysql.connection.cursor()
            hdate = request.form.get('hdate')
            ono = request.form.get('ono')
            odate = request.form.get('odate')
            cusid = request.form.get('cusid')
            cname = request.form.get('cname')
            dperson = request.form.get('dperson')
            dcont = request.form.get('dcont')
            ino = request.form.get('ino')
            cursor.execute('''SELECT code, sp, sg, cg FROM listt WHERE name = %s''', (ino,))
            print(('''SELECT code, sp, sg, cg FROM listt WHERE name = %s''', (ino,)))
            dr = cursor.fetchone()
            ino = dr[0]
            iname = request.form.get('iname')
            quantity = request.form.get('quantity')
            fquantity = request.form.get('fquantity')
            unitprice = request.form.get('unitprice')
            amount = request.form.get('amount')
            stax = request.form.get('stax')
            ctax = request.form.get('ctax')
            netAmount = request.form.get('netAmount')
            cmts = request.form.get('cmts')
            status = request.form.get('status')

            cursor.execute(
                '''INSERT INTO sales VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                hdate, ono, odate, cusid, cname, dperson, dcont, ino, iname, quantity, fquantity, unitprice, amount, stax,
                ctax, netAmount, cmts, status))
            mysql.connection.commit()
            cursor.close()
        return redirect(url_for('salesbill'))


@app.route('/view_sales_details', methods=['GET', 'POST'])
def view_sales_details():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT hdate, ono, odate, cusid, cname, dperson, dcont, ino, iname, quantity, fquantity, unitprice, amount, stax, ctax, netAmount, cmts, status FROM sales')
        users = cursor.fetchall()
        cursor.close()
        return render_template('view_sales_details.html', users=users)


@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name FROM listt')
        options = cursor.fetchall()
        cursor.execute('SELECT sid, sname, addr, email, mb, vat, balance, state FROM supplier')
        users = cursor.fetchall()
        cursor.close()
        return render_template('supplier.html', options=options, users=users)

    if request.method == 'POST':
        sid = request.form['sid']
        sname = request.form['sname']
        addr = request.form['addr']
        email = request.form['email']
        mb = request.form['mb']
        vat = request.form.get('vat')
        balance = request.form['balance']
        state = request.form['state']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO supplier VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                       (sid, sname, addr, email, mb, vat, balance, state))
        mysql.connection.commit()

        cursor.execute('SELECT sid, sname, addr, email, mb, vat, balance, state FROM supplier')
        users = cursor.fetchall()
        cursor.close()
        return render_template('supplier.html', users=users)


@app.route('/updatesupplier', methods=['POST', 'GET'])
def updatesupplier():
    if request.method == 'POST':
        sid = request.form['sid']
        sname = request.form['sname']
        addr = request.form['addr']
        email = request.form['email']
        mb = request.form['mb']
        vat = request.form.get('vat')
        balance = request.form['balance']
        state = request.form['state']
        cursor = mysql.connection.cursor()
        cursor.execute(
            """ UPDATE supplier SET sid=%s, sname=%s, addr=%s, email=%s, mb=%s, vat=%s, balance=%s, state=%s WHERE sid=%s """,
            (sid, sname, addr, email, mb, vat, balance, state,sid))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('supplier'))


@app.route('/deletesupplier/<string:sid>', methods=['GET'])
def deletesupplier(sid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM supplier WHERE sid=%s", (sid,))
    mysql.connection.commit()
    return redirect(url_for('supplier'))


@app.route('/salesbill', methods=['GET', 'POST'])
def salesbill():
    if request.method == 'GET':
        user = []

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT hdate, ono, cusid, ino, iname, quantity, fquantity, '
                       'unitprice, amount, stax, ctax, netAmount, cmts, status FROM sales order by ono desc')
        users = cursor.fetchone()
        cursor.close()
        return render_template('salesbill.html', user=users, users=user)


@app.route('/report', methods=['GET', 'POST'])
def report():
    msg = ''
    date1 = request.form.get('date1')
    date2 = request.form.get('date2')

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT pdate, purchaseID, supplierID, supplier, deliverPerson, deliverContact, itemNumber, 
        itemName, quantity, fquantity, unitprice, Amount, sgst, cgst, netAmountInput, cmts, status FROM pform 
        where purchaseDate between %s and %s''', (date1, date2,))
    users = cursor.fetchall()
    cursor.close()

    return render_template('report.html', msg=msg, users=users)


@app.route('/report2', methods=['GET', 'POST'])
def report2():
    msg = ''
    date1 = request.form.get('date1')
    date2 = request.form.get('date2')

    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT hdate, ono, cusid, cname, dperson, dcont, ino, iname, quantity, fquantity, unitprice, amount, stax, ctax, netAmount, cmts, status FROM sales where hdate between %s and %s''', (date1, date2,))
    users = cursor.fetchall()
    cursor.close()

    return render_template('report2.html', msg=msg, users=users)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
