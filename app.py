from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

# Parameter sistem
Ceq1 = 0.01 * 1e-3
Ceq2 = 0.01 * 1e-3
C1 = 0.001 * 1e-6
C2 = 0.001 * 1e-6
R12 = 1
L12 = 0.01 * 1e-3

# Fungsi dinamika sistem
def sistemKendali(t, y, Idc_src1, Idc_src2):
    V1, V2, Idc12 = y
    dV1_dt = (Idc_src1 - Idc12) / Ceq1
    dV2_dt = (Idc12 - Idc_src2) / Ceq2
    dIdc12_dt = (V1 - V2 - Idc12 * R12) / L12
    return np.array([dV1_dt, dV2_dt, dIdc12_dt])

# Metode Runge-Kutta orde 4
def rk4_step(func, t, y, dt, *args):
    k1 = func(t, y, *args)
    k2 = func(t + 0.5*dt, y + 0.5*dt*k1, *args)
    k3 = func(t + 0.5*dt, y + 0.5*dt*k2, *args)
    k4 = func(t + dt, y + dt*k3, *args)
    return y + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['GET'])
def simulate():
    t_start = 0
    t_end = 0.1
    dt = 1e-4
    t_values = np.arange(t_start, t_end, dt)

    V1_0 = 0
    V2_0 = 0
    Idc12_0 = 0
    y0 = np.array([V1_0, V2_0, Idc12_0])

    # Arus sumber
    Idc_src1 = 0
    Idc_src2 = 0

    y_values = []
    y = y0

    for t in t_values:
        y_values.append(y.tolist())
        y = rk4_step(sistemKendali, t, y, dt, Idc_src1, Idc_src2)
    y_values = np.array(y_values)

    data = {
        't': t_values.tolist(),
        'V1': y_values[:, 0].tolist(),
        'V2': y_values[:, 1].tolist(),
        'Idc12': y_values[:, 2].tolist()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
