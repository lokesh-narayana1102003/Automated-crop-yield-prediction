
from flask import Flask, render_template, request, send_file,redirect
import numpy as np
import pickle
import requests

model_model=pickle.load(open('models/ridge.pkl',"rb"))


app = Flask(__name__)


app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu'
}


def prediction(input_data):
    url = " https://bmcs8oedn7.execute-api.ap-south-1.amazonaws.com/stage_1/dev"

    # payload = "215.82,24.9,35.0,7.7,278.7,30.5,357.0,1.43,15.33,1.63,19.33,29.09,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0"
    my_string = ','.join(map(str, input_data))  
    print(my_string)
  
    headers = {
    'Content-Type': 'text/csv'
    }

    response = requests.request("POST", url, headers=headers, data=my_string)

    res=response.json()
    return res["Prediction"]   
def weather_predict(city_name):
    
    url = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"
    

    querystring = {"city":city_name}

    headers = {
        "X-RapidAPI-Key": "456ef42d3bmsha76e2021d578ad6p1047dfjsnab34a3f2d63e",
        "X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    x=response.json()
    print(x)
    if x.get("error") is None:
        rainfall=x["cloud_pct"]
        min_temp=x["min_temp"]
        max_temp=x["max_temp"]
        return rainfall,min_temp,max_temp
    else:
        return None


# app.config['LANGUAGES'] = {
#     'en': 'English',
#     'hi': 'Hindi',
#     'te': 'Telugu'
# }

@app.route("/")
def main_page():
    return render_template("start.html")

# @app.route('/show')
# def show_static_pdf():
#     with open('forestfire-main/static/pdf/DATA FOR REFERENC1.pdf', 'rb') as static_file:
#         return send_file(static_file, attachment_filename='DATA FOR REFERENC1.pdf')

@app.route('/show') #the url you'll send the user to when he wants the pdf
def pdfviewer():
    return redirect("static/pdf/DATA FOR REFERENC1.pdf") #the pdf itself


@app.route("/predict_yield", methods=["GET", "POST"])
def predict_page():


    if request.method == "POST":
        rainfall = float(request.form["rainfall"])
        min_temp = float(request.form["min_temp"])
        max_temp = float(request.form["max_temp"])
        ph = float(request.form["ph"])
        n = float(request.form["n"])
        p = float(request.form["p"])
        k = float(request.form["k"])
        zn = float(request.form["zn"])
        fe = float(request.form["fe"])
        cu = float(request.form["cu"])
        mn = float(request.form["mn"])
        irrigation = float(request.form["irrigation"])
        district_mapping = {
            "Adilabad": 0,
            "Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Godavari": 4,
            "Gadwal": 5,
            "Lingampet": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "asifabad": 9,
            "Mahbubabad": 10,
            "Mahbubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Venkatapuram": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Vemulawada": 22,
            "Hayathnagar": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Atmakur": 28,
            "Warangal": 29,
            "Warangal": 30,
            "Bhuvanagiri": 31,
        }
        f=0

        district = request.form["district"]
        district_index = district_mapping[district]
        district_encoded = np.zeros(32)
        district_encoded[district_index] = 1


        season_mapping ={
            "Kharif":0,
            "rabi":1,
        }
        season = request.form["season"]
        season_index = season_mapping[season]
        season_encoded = np.zeros(2)
        season_encoded[season_index] = 1
        
        
        crop_mapping = {
            "Crop_Groundnut": 0,
            "Crop_Maize": 1,
            "Crop_Moong(Green Gram)": 2,
            "Crop_Rice": 3,
            "Crop_cotton(lint)": 4,
        }
        
        crop = request.form["crop"]
        if crop=="Crop_cotton(lint)":
            f=f+1
        crop_index = crop_mapping[crop]
        crop_encoded = np.zeros(5)
        crop_encoded[crop_index] = 1

        test_input = np.array(
            [
                [
                    rainfall,
                    min_temp,
                    max_temp,
                    ph,
                    n,
                    p,
                    k,
                    zn,
                    fe,
                    cu,
                    mn,
                    irrigation,
                    *district_encoded,
                    *season_encoded,
                    *crop_encoded,
                ]
            ]
        )
        result=model_model.predict(test_input)
        result[0]=round(result[0],3)
        print(test_input[0])
        # result=prediction(test_input[0])
        if(f==0):
            b="Tonnes/Hectare"
        else:
            b="Bales/Hectare"
        c=str(result[0])

        return render_template("yieldfinal.html",result=c+" "+b)
    else:
        return render_template("yieldfinal.html")


@app.route('/yield-page', methods=["GET", "POST"])
def yield2_page():

    if request.method == "POST":
        district = request.form.get("district")
        season = request.form.get("season")
        crop = request.form.get("crop")
        rainfall,min_temp,max_temp = weather_predict(district)
        
        print(district)
            
        return render_template('yieldfinal.html',rainfall=rainfall,min_temp=min_temp,max_temp=max_temp, district=district, season=season, crop=crop)
    else:
        return render_template('yield1.html')



@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/prediction')
def prediction():
    return render_template('index1.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/soil')
def soil():
    return redirect('https://www.soilhealth.dac.gov.in/soil-health-map/TELANGANA/')

@app.route('/rain')
def rain():
    return redirect('https://www.tsdps.telangana.gov.in/Weather&Climatology_of_telangana.pdf')

@app.route('/irrigation')
def irrigation():
    return redirect('https://www.telangana.gov.in/PDFDocuments/Telangana-Statistical-Abstract-2021.pdf')

@app.route('/yield')
def yiel():
    return redirect('https://data.desagri.gov.in/website/crops-apy-report-web')

@app.route('/download')
def download():
    file_path = 'static/pdf/DATA FOR REFERENC1.pdf'
    return send_file(file_path, as_attachment=True)

@app.route("/default_yield", methods=["GET", "POST"])
def default_page():
    if request.method == "POST":
        
        
        f=0
        district_mapping = {
            "Adilabad": 0,
            "Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Godavari": 4,
            "Gadwal": 5,
            "Lingampet": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "asifabad": 9,
            "Mahbubabad": 10,
            "Mahbubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Venkatapuram": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Vemulawada": 22,
            "Hayathnagar": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Atmakur": 28,
            "Warangal": 29,
            "Warangal": 30,
            "Bhuvanagiri": 31,
        }
        f=0

        district = request.form["district"]
        district_index = district_mapping[district]
        district_encoded = np.zeros(32)
        district_encoded[district_index] = 1


        season_mapping ={
            "Kharif":0,
            "rabi":1,
        }
        season = request.form["season"]
        season_index = season_mapping[season]
        season_encoded = np.zeros(2)
        season_encoded[season_index] = 1
        
        
        crop_mapping = {
            "Crop_Groundnut": 0,
            "Crop_Maize": 1,
            "Crop_Moong(Green Gram)": 2,
            "Crop_Rice": 3,
            "Crop_cotton(lint)": 4,
        }
        
        crop = request.form["crop"]
        if crop=="Crop_cotton(lint)":
            f=f+1
        crop_index = crop_mapping[crop]
        crop_encoded = np.zeros(5)
        crop_encoded[crop_index] = 1
        
        rainfall,min_temp,max_temp = weather_predict(district)

        test_input = np.array(
            [
                [
                    rainfall,
                    min_temp,
                    max_temp,
                    7.257323944,
                    219.5738468,
                    34.36901408,
                    304.3738028,
                    1.370602817,
                    13.66366197,
                    1.883211268,
                    12.78577465,
                    11.35644869,
                    *district_encoded,
                    *season_encoded,
                    *crop_encoded,
                ]
            ]
        )
        result=model_model.predict(test_input)
        result[0]=round(result[0],3)
        # result=prediction(test_input)
        if(f==0):
            b="Tonnes/Hectare"
        else:
            b="Bales/Hectare"
        
        c=str(result[0])

        return render_template("yield_no_parameter.html", result=c+" "+b)
    else:
        default_values = {
            "rainfall": 86.78491341,
            "min_temp": 24.08427214,
            "max_temp": 41.1943379,
            "ph": 7.257323944,
            "n": 219.5738468,
            "p": 34.36901408,
            "k": 304.3738028,
            "zn": 1.370602817,
            "fe": 13.66366197,
            "cu": 1.883211268,
            "mn": 12.78577465,
            "irrigation": 11.35644869,
        }
        
        return render_template("yield_no_parameter.html", default_values=default_values)

if __name__ == "__main__":
    app.run(host="0.0.0.0")