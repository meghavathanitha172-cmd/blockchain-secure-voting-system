from flask import Flask, render_template, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

candidates = ["Candidate A", "Candidate B", "Candidate C"]
voted_users = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        voter_id = request.form["voter_id"]
        selected_candidate = request.form["candidate"]

        if voter_id in voted_users:
            return "You have already voted!"

        vote_data = {
            "voter_id": voter_id,
            "candidate": selected_candidate
        }

        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block["proof"]
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)

        blockchain.create_block(proof, previous_hash, vote_data)
        voted_users.append(voter_id)

        return redirect(url_for("results"))

    return render_template("vote.html", candidates=candidates)

@app.route("/results")
def results():
    votes = {"Candidate A": 0, "Candidate B": 0, "Candidate C": 0}

    for block in blockchain.chain:
        if isinstance(block["vote"], dict):
            candidate = block["vote"]["candidate"]
            votes[candidate] += 1

    return render_template("results.html", votes=votes, chain=blockchain.chain)

if __name__ == "__main__":
    app.run(debug=True)