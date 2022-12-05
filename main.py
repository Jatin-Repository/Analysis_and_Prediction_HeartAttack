import pickle
import pandas as pd
from flask import Flask, redirect, url_for, render_template, request
import numpy as np
import sklearn
import ast

from jinja2.runtime import Context

app = Flask(__name__)



@app.route("/")
def home():
    print("Root Function is called ")
    return render_template("Register.html")


@app.route("/read")
def read():
    url = request.url
    print(url)
    print(type(url))
    url_new = url.replace("%3A+",":")
    url_new_new = url_new.replace('+', '')
    list1 = url_new_new.split(",")
    print(list1)
    list1[0] = (list1[0].split("http://127.0.0.2:5000/read?info=%7B"))[1]
    pre = (((list1[-1].split("&"))[1]).split("="))[1]
    list1[-1] = ((list1[-1].split("%"))[0])
    print(list1)
    length = len(pre)
    """new = ""
    for i in range(0, length):
        if i == 3 and pre == "lowchances":
            new += " "+ pre[i]
        elif i == 4 and pre == "highchances":
            new += " " + pre[i]
        else:
            new += pre[i]
    pre = new"""
    print(list1)
    length2 = len(list1)
    p_name = (list1[0].split(":"))[1]
    number = (list1[1].split(":"))[1]
    u_id = (list1[2].split(":"))[1]
    h_name = (list1[3].split(":"))[1]
    age = (list1[4].split(":"))[1]
    thalach = (list1[5].split(":"))[1]
    trtbps = (list1[6].split(":"))[1]
    oldpeak = (list1[7].split(":"))[1]
    sex = (list1[8].split(":"))[1]
    cst = (list1[9].split(":"))[1]
    exang = (list1[10].split(":"))[1]
    slope = (list1[11].split(":"))[1]
    ca = (list1[12].split(":"))[1]
    thal = (list1[13].split(":"))[1]
    chol = (list1[14].split(":"))[1]
    restecg = (list1[15].split(":"))[1]
    fbs = (list1[16].split(":"))[1]
    print(p_name, sex, u_id, age)
    if sex == 1:
        sex = 'Female'
    else:
        sex = "Male"
    if cst == 1:
        cst = "Typical Angina"
    elif cst == 2:
        cst = "Atypical Angina"
    elif cst == 3:
        cst = "Non-Anginal Pain"
    else:
        cst = "Asymptomatic"
    if restecg == 1:
        restecg = "Normal"
    elif restecg == 2:
        restecg = "ST-T wave abnormality"
    elif restecg == 0:
        restecg = "Hypertrophy"
    if exang == 1:
        exang = "Yes"
    else:
        exang = "No"
    if slope == 2:
        slope = "Up Sloping"
    elif slope == 1:
        slope = "Flat"
    else:
        slope = "Down Sloping"
    if thal == 2:
        thal = "Normal"
    elif thal == 1:
        thal = "Flat"
    elif thal == 3:
        thal = "Reversable Defect"
    print(p_name, number,u_id,h_name,age,sex)
    return render_template("fetch.html", name = p_name,number = number, u_id = u_id, h_name =h_name,age =age,sex =sex,pre = pre)

@app.route('/fetch', methods =["GET", "POST"])
def fetch():
    print("Read Method is called")
    if request.method == "POST":
        p_name = request.form.get("p_name")  # Paitent Name
        num = request.form.get("num")
        u_id = request.form.get("u_id")
        h_name = request.form.get("h_name")
        age = int(request.form.get("age"))
        sex = int(request.form.get("sex"))
        cst = float(request.form.get("cst"))
        trestbps = float(request.form.get("trestbps"))
        chol = float(request.form.get("chol"))
        fbs = float(request.form.get("fbs"))
        restecg = int(request.form.get("restecg"))
        thalach = float(request.form.get("thalach"))
        exang = int(request.form.get("exang"))
        oldpeak = float(request.form.get("oldpeak"))
        slope = int(request.form.get("slope"))
        ca = int(request.form.get("ca"))
        thal = int(request.form.get("thal"))
        info = {
            'pname': p_name,
            'number': num,
            'u_id': u_id,
            'h_name': h_name,
            'age': age,
            'thalach': thalach,
            'trtbps': trestbps,
            'oldpeak': oldpeak,
            'sex': sex,
            'cst': cst,
            'exang': exang,
            'slope': slope,
            'ca': ca,
            'thal': thal,
            'chol': chol,
            'restecg': restecg,
            'fbs': fbs}
        ca_1 = ca_2 = ca_3 = ca_4 = 0
        sex_1 = sex
        exang_1 = exang
        age = (age-55)/(47.5-61.0)
        slope_1 = slope_2 = 0
        trtbps_winsorize = (trestbps - 130)/(140-120) # for normalising input
        oldpeak_winsorize_sqrt = (np.sqrt(oldpeak) - np.sqrt(0.80))/np.sqrt(1.60)
        thalach = (thalach-153)/(166-133.5)
        thal_2 = thal_3 = 0
        cp_1 = cp_2 = cp_3 = 0
        if ca == 0:
            ca_1 = 1
        elif ca == 1:
            ca_2 = 1
        elif ca == 2:
            ca_3 = 1
        elif ca == 3:
            ca_4 = 1
        if thal == 2:
            thal_2 = 1
        elif thal == 3:
            thal_3 = 1
        if slope == 1:
            slope_1 = 1
        elif slope == 2:
            slope_2 = 1
        if cst == 1:
            cp_1 = 1
        elif cst == 2:
            cp_2 = 1
        elif cst == 3:
            cp_3 = 1
    data = {
            'age': age,
            'thalach': thalach,
            'trtbps_winsorize':trtbps_winsorize,
            'oldpeak_winsorize_sqrt':oldpeak_winsorize_sqrt,
            'sex_1':sex_1,
            'cp_1':cp_1,
            'cp_2':cp_2,
            'cp_3':cp_3,
            'exang_1':exang_1,
            'slope_1':slope_1,
            'slope_2':slope_2,
            'ca_1': ca_1,
            'ca_2':ca_2,
            'ca_3':ca_3,
            'ca_4':ca_4,
            'thal_2':thal_2,
            'thal_3':thal_3}
    X_New = pd.DataFrame(data, index=[305])
    with open('Templates/Trained_Model.pkl', 'rb') as f:
        model = pickle.load(f)
    result = model.predict(X_New)
    print(result)
    pre = "LOW"
    if result == 1:
        pre = "HIGH"
    # return "The Paitent {} of heart attack.".format(pre)
    #return redirect("fetch.html", info=info, pre=pre)
    print(info)
    return redirect(url_for('read', info=info, pre=pre))


if __name__ == "__main__":
    app.run(host='127.0.0.2', port=5000)
