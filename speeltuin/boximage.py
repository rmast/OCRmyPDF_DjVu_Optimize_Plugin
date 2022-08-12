import easyocr
reader = easyocr.Reader(['nl','en']) # this needs to run only once to load the model into memory
bounds = reader.readtext('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg', detail=0,paragraph=False, y_ths=0.01, x_ths=0.01,text_threshold=0.9)
#result = reader.readtext('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')
#print (result)
print (bounds)

