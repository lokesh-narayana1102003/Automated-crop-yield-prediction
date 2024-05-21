

from flask import Flask, render_template, request, send_file
import numpy as np
import pickle

model_model=pickle.load(open('models/ridge.pkl',"rb"))

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")
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
        # Create the district mapping
        district_mapping = {
            "Adilabad": 0,
            "Bhadradri Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Jayashankar": 4,
            "Jogulamba": 5,
            "Kamareddy": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "Komaram bheem asifabad": 9,
            "Mahabubabad": 10,
            "Mahabubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Mulugu": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Rajanna": 22,
            "Rangareddy": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Wanaparthy": 28,
            "Warangal": 29,
            "Warangal Urban": 30,
            "Yadadri": 31,
        }

        # Retrieve the index of the selected district
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
        
        """if season == "Kharif":
            arr_seson = [1, 0]
        else:
            arr_seson = [0, 1]"""
        
        crop_mapping = {
            "Crop_Groundnut": 0,
            "Crop_Maize": 1,
            "Crop_Moong(Green Gram)": 2,
            "Crop_Rice": 3,
            "Crop_cotton(lint)": 4,
        }
        crop = request.form["crop"]
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
        return render_template("yield.html", result=result[0])
    else:
        return render_template("yield.html")

@app.route('/predict_crop',methods=['GET','POST'])
def predict_crop():
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
        district = request.form["district"]
        season=request.form["season"]
        #crop=request.form["crop"]
        # Create the district mapping
        district_mapping = {
            "Adilabad": 0,
            "Bhadradri Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Jayashankar": 4,
            "Jogulamba": 5,
            "Kamareddy": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "Komaram bheem asifabad": 9,
            "Mahabubabad": 10,
            "Mahabubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Mulugu": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Rajanna": 22,
            "Rangareddy": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Wanaparthy": 28,
            "Warangal": 29,
            "Warangal Urban": 30,
            "Yadadri": 31,
        }
        season_mapping={
            "Kharif":0,
            "Rabi":1,
        }
        
        district_index = district_mapping[district]
        district_encoded = np.zeros(32)
        district_encoded[district_index] = 1
        
        season_index=season_mapping[season]
        season_encoded=np.zeros(2)
        season_encoded[season_index]=1
        max=0
        maxi=0
        for i in range(0,5):
            crop_encoded=np.zeros(5)
            crop_encoded[i]=1

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

            results=model_model.predict(test_input)
            if float(results[0])>max:
                max=results[0]
                maxi=i
        if maxi==0:
            return render_template("crop.html",result="Groundnut")
        elif maxi==1:
            return render_template("crop.html",result="Maize")
        elif maxi==2:
            return render_template("crop.html",result="Moong")
        elif maxi==3:
            return render_template("crop.html",result="Rice")
        elif maxi==4:
            return render_template("crop.html",result="Cotton")
        else:
            return render_template("crop.html",result="ERROR")
     else:
         return render_template("crop.html")
@app.route('/download')
def download():
    # Path to the file you want to download
    file_path = 'dataset/FINAL-Dataset-csv.csv'

    # Send the file as an attachment for download
    return send_file(file_path, as_attachment=True)
@app.route('/another-page')
def another_page():
    return render_template('data.html')
@app.route('/yield')
def yield_page():
    return render_template('indexyield.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0")