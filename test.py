import requests
#req = {"query": "query foodInFridge{allFoods{name}}"}
req = {"query": "query foodInFridge{allFoods(where: { quantity_gt: 0 } ){name,duration,quantity,entryDate,id,image{publicUrlTransformed,filename}}}"}
r = requests.post('https://dumb-fridge.herokuapp.com/admin/api', json= req, headers= {'Accept': 'application/vnd.cap-collectif.preview+json'})
#r = requests.get('https://jsonplaceholder.typicode.com/todos/1')
print(r.status_code)
print(r.json())