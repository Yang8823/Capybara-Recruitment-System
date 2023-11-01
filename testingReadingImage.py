import pyresparser

# Specify the path to the resume file
resume_path = "science-cs-egr-resumes.pdf"  # Replace with the actual path to your resume

# Extract information from the resume
data = pyresparser.from_path(resume_path)

# Access the extracted data
print("Name:", data['name'])
print("Email:", data['email'])
print("Phone Number:", data['mobile_number'])
print("Skills:", data['skills'])
print("Education:", data['education'])
print("Work Experience:", data['experience'])

pyresparser.cleanup()