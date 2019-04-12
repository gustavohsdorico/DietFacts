import xmlrpclib
import csv

server = "http://localhost:8069"
database = "dietfacts2"
user = "admin"
pwd = "admin"

common = xmlrpclib.ServerProxy('%/xmlrpc/2/common' % server)

#print common.version()

uid = common.authenticate(database,user,pwd, {})

#print uid

OdooApi = xmlrpclib.ServerProxy('%/xmlrpc/2/object' % server)

filter = [[('largemeal','=','True')]]
product_count = OdooApi.execute_kw(database,uid,pwd,'res.users.meal','search_count',filter)

#print product_count

Filename = "importdata.csv"

reader = csv.reader(open(Filename,'rb'))

filter = [[('name','=','Diet Items')]]

categ_id = OdooApi.execute_kw(database,uid,pwd,'product.category','search',filter)

for row in reader:  

    productname = row[0]
    calories = row[1]

    filter = [[('name','=','productname')]]
    product_id = OdooApi.execute_kw(database,uid,pwd,'product.template','search',filter)
    if product_id:
        record = {'calories': calories,'categ_id': categ_id[0]}
        OdooApi.execute_kw(database,uid,pwd,'product.template','write',[product_id, record])
        print "Upa the product id=" + str(product_id)

    else:
        print "Adding Product:" + productname
        record = [{'name': productname,'calories': calories,'categ_id': categ_id[0]}]
        OdooApi.execute_kw(database,uid,pwd,'product.template','create',record)
