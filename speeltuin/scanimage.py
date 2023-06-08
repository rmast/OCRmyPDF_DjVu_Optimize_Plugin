import easyocr
reader = easyocr.Reader(['nl','en']) # this needs to run only once to load the model into memory
#result = reader.readtext('/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')
#result = reader.readtext('/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg', width_ths=0.03 )
result = reader.detect('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')
print (result)

