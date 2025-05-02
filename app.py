from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def detect_and_recover(data):
    n = data['numProcesses']
    m = data['numResources']
    alloc = data['alloc']
    req = data['req']
    avail = data['avail']

    finish = [False] * n
    work = avail[:]
    changed = True

    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and all(req[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += alloc[i][j]
                finish[i] = True
                changed = True

    deadlocked = [i for i in range(n) if not finish[i]]
    terminated = []

    while deadlocked:
        proc = deadlocked[0]
        for j in range(m):
            work[j] += alloc[proc][j]
        finish[proc] = True
        terminated.append(proc)
        deadlocked = [i for i in range(n) if not finish[i]]

    return {
        "safe": all(finish),
        "terminated": terminated
    }

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    data = json.loads(request.form["matrixData"])
    result = detect_and_recover(data)
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
