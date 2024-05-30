import json

def parse_quiz_string(quiz_string):
    # Initialize an empty list to store the parsed questions
    parsed_questions = []

    # Split the string by question numbers
    sections = quiz_string.split("\n\n")

    # Extract the title (first section)
    title = sections[0].strip("#").strip()

    # Process the remaining sections (questions and options)
    for section in sections[1:]:
        # Split the section into lines
        lines = section.split("\n")

        # Extract the question number and text
        try:
            question_number, question_text = lines[0].split(". ", 1)
        except ValueError:
            print("Error in line:", lines[0])
            continue

        # Extract the options (excluding the question number)
        options = [line.strip() for line in lines[1:]]

        # Extract the correct answer (last character of the first option)
        correct_answer = options[0][-1]

        # Create a dictionary for the question
        question_dict = {
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
        }

        # Append the question dictionary to the list
        parsed_questions.append(question_dict)

    return title, parsed_questions

# Example usage and saving the parsed data structure into a JSON file
quiz_string = """
## Medium Digital Image Processing Quiz\n\n1. What transformation is commonly used for perspective correction in digital images?\n   A) Orthogonal transformation\n   B) Affine transformation\n   C) Fourier transform\n\n2. What technique is used for depth estimation in multi-camera views?\n   A) Binocular stereopsis\n   B) Image segmentation\n   C) Region growing\n\n3. Which feature extraction method is used for detecting edges in images?\n   A) Harris corner detection\n   B) Canny edge detection\n   C) SIFT feature extraction\n\n4. What is the purpose of image segmentation?\n   A) To classify pixels into regions\n   B) To enhance image contrast\n   C) To remove noise from images\n\n5. How are patterns analyzed in digital image processing?\n    A) Through clustering and classification\n    B) By applying convolution and filtering\n    C) Using Fourier transform and histogram processing\n\n6. What is the primary objective of motion analysis in image processing?\n   A) To estimate depth in multi-camera views\n   B) To detect and track moving objects\n   C) To enhance image resolution\n\n7. Which segmentation technique is based on edge detection?\n    A) Graph-Cut\n    B) Mean-Shift\n    C) Region Growing\n\n8. How is dimensionality reduction achieved in pattern analysis?\n    A) By using clustering algorithms\n    B) By applying principal component analysis (PCA)\n    C) By using edge-based segmentation techniques\n\n**Answer Key**:\n1. B)\n2. A)\n3. B)\n4. A)\n5. A)\n6. B)\n7. A)\n8. B)
"""

title, questions = parse_quiz_string(quiz_string)

# Serialize data structure into JSON
quiz_data = {
    "title": title,
    "questions": questions
}

# Write JSON data to a file
with open("quiz_data.json", "w") as json_file:
    json.dump(quiz_data, json_file)

print("Quiz data has been saved to quiz_data.json.")
