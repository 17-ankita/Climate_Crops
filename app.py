from flask import Flask, render_template, request
from data_fetcher import fetch_csv
from analytics import top_m_crops_for_state, compare_avg_rainfall

app = Flask(__name__)

crop_df = fetch_csv("sample.csv")
rain_df = fetch_csv("sample.csv")

all_states = [s.strip() for s in crop_df['State'].unique()]
years = crop_df['Year'].unique().tolist()

@app.route("/", methods=["GET", "POST"])
def home():

    topx = None
    topy = None
    rainfall = None

    state_x = "Haryana"
    state_y = "Tamil Nadu"

    if request.method == "POST":

        query = request.form.get("query", "").lower()

        matched_states = []

        for state in all_states:
            if state.lower() in query:
                matched_states.append(state)

        matched_states = list(dict.fromkeys(matched_states))

        if len(matched_states) >= 2:
            state_x, state_y = matched_states[0], matched_states[1]

        elif len(matched_states) == 1:
            state_x = matched_states[0]
            state_y = matched_states[0]

        topx = top_m_crops_for_state(crop_df, state_x, years, m=3)
        topy = top_m_crops_for_state(crop_df, state_y, years, m=3)

        rainfall = compare_avg_rainfall(
            rain_df,
            [state_x, state_y],
            years
        )

    return render_template(
        "index.html",
        topx=topx,
        topy=topy,
        rainfall=rainfall,
        state_x=state_x,
        state_y=state_y
    )

if __name__ == "__main__":
    app.run(debug=True)