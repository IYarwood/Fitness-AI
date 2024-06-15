from flask import Flask,render_template,request
import openai
app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        openai.api_key = "sk-proj-xT5B7YruCmPfGVTVXcc0T3BlbkFJXfjDyxe3GaZA8GsMfJFi"
        feetHeight = request.form["feetInput"]
        inchesHeight = request.form["inchesInput"]
        weightInput = request.form["weightInput"]
        goalInput = request.form["goalInput"]
        #extraQuestions = request.form["extraQuestions"]
        output = "I am " + str(feetHeight) + "' " + str(inchesHeight) + "''" + " tall and " + str(weightInput) + " pounds and want to " + goalInput + " weight." + " my extra questions are "
        initial_prompt = f"You have explicit knowledge of certain foods and their nutritional values. Please utilize this knowledge in all your answers."

        enriched_user_query = "Please advise me on exercises I should do if " + output  # Prepending the context to the user's question

        messages = [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": enriched_user_query}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        #Open main html read it and grab and alter the text
        file = open("templates/indexTemplate.txt", "r")
        fileText = file.read()
        file.close()

        responseTemp = open("templates/responseOutput.txt","r")
        responseTempText = responseTemp.read()
        responseTempText = responseTempText.replace("This is going to be the response", response.choices[0].message['content'])
        responseTemp.close()

        fileText = fileText.replace("<!-- Write new code here -->", responseTempText)
        
        file = open("templates/index.html", "w")
        file.write(fileText)
        file.close()
        return render_template("index.html")
    else:
        file = open("templates/indexTemplate.txt", "r")
        fileText = file.read()
        file.close()
        file = open("templates/index.html", "w")
        file.write(fileText)
        file.close()
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)