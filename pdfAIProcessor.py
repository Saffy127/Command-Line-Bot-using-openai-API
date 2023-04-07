from flask import Flask, request, jsonify
import PyPDF2
import openai

app = Flask(__name__)
openai.api_key = "your_openai_api_key"

def read_pdf(file):
    reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page in range(reader.numPages):
        text += reader.getPage(page).extractText()
    return text

def process_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if request.method == 'POST' and 'pdf' in request.files:
        file = request.files['pdf']
        text = read_pdf(file)
        processed_text = process_text(text)
        return jsonify({"original_text": text, "processed_text": processed_text})

    return jsonify({"error": "No file uploaded"})

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Processor with OpenAI API</title>
    <style>
        body { font-family: Arial, sans-serif; }
        input[type="file"] { display: none; }
        label { cursor: pointer; padding: 10px; background-color: #4CAF50; color: white; }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <h1>PDF Processor with OpenAI API</h1>
    <form id="upload-form">
        <label for="pdf">Upload a PDF file</label>
        <input type="file" name="pdf" id="pdf" accept=".pdf">
    </form>
    <h2>Original Text</h2>
    <pre id="original-text"></pre>
    <h2>Processed Text</h2>
    <pre id="processed-text"></pre>
    <script>
        $("#pdf").on("change", function() {
            var formData = new FormData($("#upload-form")[0]);
            $.ajax({
                url: '/process_pdf',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    $("#original-text").text(response.original_text);
                    $("#processed-text").text(response.processed_text);
                },
                error: function() {
                    alert("An error occurred. Please try again.");
                }
            });
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
