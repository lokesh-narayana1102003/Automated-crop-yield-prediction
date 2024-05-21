const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));

// Define routes
app.get('/predict_yield', (req, res) => {
    res.render('yield');
});

app.post('/predict_yield', (req, res) => {
    const rainfall = parseFloat(req.body.rainfall);
    const min_temp = parseFloat(req.body.min_temp);
    const max_temp = parseFloat(req.body.max_temp);
    const ph = parseFloat(req.body.ph);
    const n = parseFloat(req.body.n);
    const p = parseFloat(req.body.p);
    const k = parseFloat(req.body.k);
    const zn = parseFloat(req.body.zn);
    const fe = parseFloat(req.body.fe);
    const cu = parseFloat(req.body.cu);
    const mn = parseFloat(req.body.mn);
    const irrigation = parseFloat(req.body.irrigation);

    const district_mapping = {
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
        // Add other district mappings
    };

    const district = req.body.district;
    const district_index = district_mapping[district];
    const district_encoded = Array(32).fill(0);
    district_encoded[district_index] = 1;

    const season_mapping = {
        "Kharif": 0,
        "rabi": 1,
    };

    const season = req.body.season;
    const season_index = season_mapping[season];
    const season_encoded = Array(2).fill(0);
    season_encoded[season_index] = 1;

    const crop_mapping = {
 
        "Crop_Groundnut": 0,
        "Crop_Maize": 1,
        "Crop_Moong(Green Gram)": 2,
        "Crop_Rice": 3,
        "Crop_cotton(lint)": 4,       // Add other crop mappings
    };

    const crop = req.body.crop;
    const crop_index = crop_mapping[crop];
    const crop_encoded = Array(5).fill(0);
    crop_encoded[crop_index] = 1;

    // Get historical weather data
    const oneYearAgo = new Date();
    oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
    const rainfallFromAPI = getHistoricalWeather(req.body.district, oneYearAgo);

    // Continue with the rest of the code
    // ...

    res.render('yield', { result: result[0] });
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
