from flask import Flask, render_template, request
from laptop_price_pred import laptop_price_pred, unique_data


app = Flask(__name__)


#index 
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        data = unique_data()
        return render_template('index.html', data = data)
    

@app.route('/price', methods = ['GET', 'POST'])
def price():
    if request.method == 'POST':
        print('into POST')
        # Company	TypeName	Inches	ScreenResolution	Cpu	Ram	Memory	Gpu	OpSys	Weight
        company = request.form.get('Company')
        type_name = request.form.get('TypeName')
        screen_resolution = request.form.get('ScreenResolution')
        cpu = request.form.get('Cpu')
        ram = request.form.get('Ram')
        memory = request.form.get('Memory')
        gpu = request.form.get('Gpu')
        opsys = request.form.get('OpSys')
        weight = request.form.get('Weight')
        print(company, type_name, screen_resolution, cpu, ram, memory, gpu, opsys, weight)
        print('_'*10)
        price = laptop_price_pred(company, type_name, screen_resolution, cpu, ram, memory, gpu, opsys, weight)
        print(price)
        return render_template('price.html', price = price, company = company, type_name = type_name, screen_resolution = screen_resolution, cpu = cpu, ram = ram, memory = memory, gpu = gpu, opsys = opsys, weight = weight)
 

if __name__ == "__main__":
    app.run(debug=True)
