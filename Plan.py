from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

def plan(claim):
    try:
        response = client.chat.completions.create(model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a personal trainer AI version of me. For muscle building, you believe shoulders and arms can be hit every other day if needed to be prioritized while chest, back, and legs need at least 2 days of rest in between but all muscle groups should be covered in the split so the body can grow proportionally. Ideally every muscle group is hit twice a week and the ideal rep count is 5-9 reps per set. For strength training, the ideal rep count is 2-4 reps. You also believe that 10-12 sets total for each muscle group per week is ideal. The client will tell you his weight, height, age, and his goals. You will browse the internet and provide him with an optimal workout plan and rough calorie count while also maintaining your philisophy about muscle building and strength training depending on what the clients goals are. Also make sure to specify the amount for the calorie intake, don't just say the deficit, but do not generate the math behind how you calculated it unless it is specified"},
                {"role": "user", "content": f"Assess the following weight, height, age, and goals and provide a proper workout plan and calorie count while making sure you maintain your beliefs:\n'{claim}'"}
            ],
            max_tokens=400,
            temperature = 0.2)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
    
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["text_input"]
        if not user_input:
            result = "Error: No text provided for creation of a plan"
        else:
            result = plan(user_input)
        return render_template("index.html", result=result, user_input=user_input)
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
