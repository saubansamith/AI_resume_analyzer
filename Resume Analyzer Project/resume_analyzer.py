import google.generativeai as genai
import fitz

def export_resume_details(path):
    genai.configure(api_key="AIzaSyADbZ9AxiGy73GIdOuULCSEvH-LAgWwkQo")
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    doc = fitz.open(path)
    pdf_text = "\n".join([page.get_text() for page in doc])
    # while True:
    response = model.generate_content(['''
                                       Analyze this resume and return python lists for name, email, phone, skills, education, 
                                       experience level (fresher, intermediate, experienced), objective, declaration, hobbies,
                                       achievements, certifications, projects. (Note that, if any of the following could not be found, assign the value False.)
                                       Just return the values in a list with the respective variable name given above.
   ''', pdf_text],generation_config={"temperature": 0})
    # if '=' in response:
    #     break
    code=response.text
    if code.split('\n')[0]=='```python':
        code='\n'.join(code.split('\n')[1:-2])
    with open('resume_analyzed.py','w', encoding="utf-8") as file:
        file.write(code)
    return len(doc)