from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

class DeadlockSimulator:
    def __init__(self):
        self.graph = []

    def load_graph(self, graph):
        self.graph = graph

    def detect_deadlock(self):
        n = len(self.graph)
        visited = [False] * n
        rec_stack = [False] * n

        def is_cyclic(v):
            visited[v] = True
            rec_stack[v] = True
            for i in range(n):
                if self.graph[v][i]:
                    if not visited[i] and is_cyclic(i):
                        return True
                    elif rec_stack[i]:
                        return True
            rec_stack[v] = False
            return False

        for node in range(n):
            if not visited[node]:
                if is_cyclic(node):
                    return True
        return False

simulator = DeadlockSimulator()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        graph = request.form.get("graph")
        try:
            graph_data = eval(graph)
            simulator.load_graph(graph_data)
            deadlock = simulator.detect_deadlock()
            return redirect(url_for("result", deadlock=deadlock))
        except:
            return render_template("index.html", error="Invalid input. Please enter a valid 2D array.")
    return render_template("index.html")

@app.route("/result")
def result():
    deadlock = request.args.get("deadlock", "false") == "True"
    return render_template("result.html", deadlock=deadlock)

if __name__ == "__main__":
    app.run(debug=True)