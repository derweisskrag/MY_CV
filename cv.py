from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate, 
    BaseDocTemplate, 
    PageTemplate, 
    PageBreak, 
    Frame, 
    FrameBreak, 
    Spacer, 
    Paragraph
)

import pyphen
import string

def capitalize_decorator(func):
    def wrapper(text):
        capitalized_text = func(text)
        capitalize_words = {'i', 'english', 'estonian', "russian", "description:"}
        words = capitalized_text.split()
        capitalized_words = [word.capitalize() if word.replace("&shy;", "").lower() in capitalize_words else word for word in words]
        capitalized_words = helper(capitalized_words)
        return ' '.join(capitalized_words)
    return wrapper


def hyphenate_decorator(func):
    def wrapper(text):
        # Preprocess the text before hyphenation
        preprocessed_text = text.lower()
        hyphenated_text = func(preprocessed_text)
        # Postprocess the hyphenated text
        postprocessed_text = hyphenated_text.capitalize()
        return postprocessed_text
    return wrapper

@capitalize_decorator
@hyphenate_decorator
def format_text(text):
    hyphenator = pyphen.Pyphen(lang='en_US')  # Explicitly set language to English (US)

    lines = text.split("\n")
    words = [line.split() for line in lines]

    hyphenated_lines = []
    for line in words:
        hyphenated_words = []
        for word in line:
            hyphenated_word = hyphenator.inserted(word, '&shy;')
            hyphenated_words.append(hyphenated_word)
        hyphenated_line = ' '.join(hyphenated_words)
        hyphenated_lines.append(hyphenated_line)
    return "\n".join(hyphenated_lines)


def helper(lst):
    for i in range(len(lst) - 1):
        if lst[i].endswith("."):
            lst[i + 1] = lst[i + 1].capitalize()
    return lst

def process_descriptions(descriptions):
    result = []
    for description in descriptions:
        if not description.strip():  # Check if description is empty or contains only whitespace
            result.append(description)
        else:
            formated = format_text(description)
            words_list = formated.split()
            if words_list[-1] == '.':
                words_list = words_list[:-1]  # Remove the last element (the dummy period)
            formated = ' '.join(helper(words_list))  # Apply the helper function and join the words back to a string
            result.append(formated)
    return result



    
def draw_on_first_page(canvas, doc):
    '''
    This function is used to draw my custom design on the first page of the document

    Args: 
        canvas (Canvas): The canvas object used for drawing
        doc (SimpleDocTempalte): The document object containing the canvas
    '''
    # Set the font family and size
    canvas.setFont("Helvetica", 12)

    # Set the text color
    canvas.setFillColorRGB(1, 0, 0)

    #Text data and position:
    #Coordinates to draw at
    """
        Origing is at (0, 0) 
        x points to right
        y points to upwards
        Thus, origin of the canvas is left-bottom corner
    """
    x = 500
    y = 700

    #Texts to draw
    intro = "Sergei Ivanov - Resume"
    text_on_circle = "Python"


    # Draw the text at the given position
    canvas.drawString(x, y, intro)

    # Draw the line
    canvas.line(x, y - 20, x + 100, y - 20)

    # Draw a circle with inner color yellow and border color blue
    canvas.setStrokeColorRGB(0, 0, 1)  # Set border color to blue (RGB: 0, 0, 1)
    canvas.setFillColorRGB(1, 1, 0, .5)  # Set inner color to yellow (RGB: 1, 1, 0)
    canvas.setLineWidth(2)  # Set border thickness to 2 pixels
    radius = 50  # Set the radius of the circle
    # Python draws the circle:
    canvas.circle(x + 50, y - 100, radius, fill=True, stroke=True)

    # Change the colour to white
    canvas.setFillColorRGB(1, 1, 1)

    # Text inside circle
    # Text sizes and measurements for text on circle
    text_on_circle_width = canvas.stringWidth(text_on_circle, "Helvetica", 12)
    text_on_circle_heigth = canvas._fontsize
    text_on_circle_x = x + 50 - text_on_circle_width / 2
    text_on_circle_y = y - 100 - text_on_circle_heigth / 4
    text_color = (0, 0, 0)  # black
    # change the font and fill colour
    canvas.setFont("Times-Bold", 12)
    canvas.setFillColorRGB(*text_color)

    # Python draws the text on the circle
    canvas.drawString(text_on_circle_x, text_on_circle_y, text_on_circle)
    canvas.saveState()

    

def draw_background(canvas, doc):
    background_image_path = "Faruzan.jpg"
    canvas.drawImage(background_image_path, 0, 0, width=letter[0], height=letter[1])    

def create_cv_pdf():
    doc = SimpleDocTemplate("cv.pdf", pagesize=letter)
    styles = getSampleStyleSheet()

    #Styling
    custom_style = styles['Normal'].clone('custom_style')
    custom_style.fontSize = 10 #Default
    custom_style.leading = 14
    custom_style.alignment = 0

    #Create content for the CV
    content = []
    content.append(Paragraph('Curriculum Vitae', styles['Heading1']))
    content.append(Spacer(1, 12))

    # Personal Information on the left
    left_content = [
        Paragraph('Personal Information', styles['Heading2']),
        Paragraph('Name: Sergei Ivanov', styles['Normal']),
        Paragraph('Emails: kompasj@mail.ru, sergei.8klass@gmail.com', styles['Normal']),
        Paragraph('Address: Ida-Viru maakond, Narva-Jõesuu linn, Narva-Jõesuu linn, Pargi tn 10a-4', styles['Normal']),
        Paragraph('Phone number: +37253226378', styles['Normal']),
        Paragraph('Sotsiaalmeedia konto: https://www.facebook.com/sergei.ivanov.79230305/', styles['Normal']),
        Spacer(1, 12),
        Paragraph('Individual Traits', styles['Heading2']),
        Paragraph('As a highly motivated and dedicated individual, I am always eager to take on new challenges and explore innovative solutions. I am proactive in seeking opportunities for self-improvement and value continuous learning. My attention to detail and strong analytical skills enable me to approach complex problems with precision and creativity. I am a team player and believe in collaborative efforts to achieve project success.', styles['Normal']),
        Spacer(1, 12),
    ]

    #descriptions of my languages
    english_description = """
    Description: I have been studying English for several years and can confidently communicate in both
    written and spoken form. I have experience in academic and professional settings, and I am
    comfortable using English for everyday conversations and business communication. English is the best
    language for me to use in daily activities because I can communicate with a greater number of people
    from all over the world.
    """

    russian_description = """
    Description: Russian is my native language, and I am completely fluent in both spoken and written 
    forms. I have an extensive vocabulary and can effectively use Russian for any communication purpose, 
    including academic and professional contexts. 
    """

    estonian_description = """
    Description: I have acquired proficiency in Estonian through my studies and living experience 
    in Estonia. I can engage in conversations, read and write in Estonian with ease, though I may 
    still encounter some complex vocabulary in certain contexts. My military service helped me to 
    gain better knowledge of Estonian, whereby I am going to take C1 exam and get a new certification
    """
    english, estonian, russian = process_descriptions([
        english_description,
        estonian_description,
        russian_description])


    right_content = [
        #Education
        Paragraph('Education', styles['Heading2']),
        Paragraph('Upper-secondary education, Narva middle city upper-secondary school, 09.2016-06.2019', styles['Normal']),
        Spacer(1, 12),
        Paragraph('uncompleted tertiary education, Tallinn TalTech, 08.2019-05.2021', styles['Normal']),
        Spacer(1, 12),
        Paragraph('Secondary education, Narva-Jõesuu, 09.2007-06.2016', styles['Normal']),
        Spacer(1, 12),
        Paragraph('Tertiary education Computer Science College, Narva, 09.2023-06.2026', styles['Normal']),
        Spacer(1, 12),
        
        # Communicative skills
        Paragraph('Language skills', styles['Heading2']),
        
        Paragraph('English', styles['Heading3']),
        Paragraph('Speaking: B2', styles['Normal']),
        Paragraph('Writing: B2', styles['Normal']),
        Paragraph(english, custom_style),
        Spacer(1, 12),

        # Estonian
        Paragraph('Estonian', styles['Heading3']),
        Paragraph('Speaking: B2', styles['Normal']),
        Paragraph('Writing: B2', styles['Normal']),
        Paragraph(estonian, styles['Normal']),
        Spacer(1, 12),

        # Russian
        Paragraph('Russian', styles['Heading3']),
        Paragraph('Speaking: C2', styles['Normal']),
        Paragraph('Writing: C2', styles['Normal']),
        Paragraph("Mother's tongue: True", styles['Normal']),
        Paragraph(russian, styles['Normal']),
        Spacer(1, 12),
        #Computer Science Skills
        Paragraph('Computer Science Skills', styles['Heading2']),
        Paragraph('Proficiency: expert', styles['Normal']),

        #Languages
        Paragraph('Programming languages', styles['Heading3']),

        #JavaScript
        Paragraph('JavaScript', styles['Heading4']),
        Paragraph('Proficiency: Intermediate', styles['Normal']),
        Paragraph('Technologies: NEXT.js, React.js, Node.js at Intermediate', styles['Normal']),
        Spacer(1, 12),


        Paragraph('Python', styles['Heading4']),
        Paragraph('Proficiency: Intermediate', styles['Normal']),
        Paragraph('Technologies: Numpy, Pandas, SciPy, Asyncio at Beginner', styles['Normal']),
        Spacer(1, 12),

        #Others
        Paragraph('Other Programming languages', styles['Heading4']),
        Paragraph('Languages: C++, Java, PHP, TS', styles['Normal']),
        Paragraph('Proficiency: Intermediate', styles['Normal']),
        Paragraph("Description: Algorithms, Data Structures; completed course about Java algorithms on Edx Harvard courses' portal; able to follow DRY and OPP principles; knowledge of implements and extends principles when defining classes", styles['Normal']),
        Paragraph("Technologies: OpenGL (C++), Android Studio (Java), Laravel, Magento (PHP), React (TS)", styles['Normal']),
        Paragraph("Technologies' proficiency: Beginner", styles['Normal']),
        Spacer(1, 12),

        #Data Bases
        Paragraph('Data Bases', styles['Heading3']),
        Paragraph('Description: Pagination (cursor and offset); create and customize models; implement simple CRUD functions like create(), update(), delete(), mutate(); implement server side actions using NEXT or T3App framework built using NEXT and Prisma', styles['Normal']),
        
        #Prisma
        Paragraph('Prisma', styles['Heading4']),
        Paragraph('Proficiency: Beginner', styles['Normal']),
        
        #mySQL
        Paragraph('SQL', styles['Heading4']),
        Paragraph('Proficiency: Beginner', styles['Normal']),

        #mongoose
        Paragraph('Mongoose', styles['Heading4']),
        Paragraph('Proficiency: Beginner', styles['Normal']),

        #pandas
        Paragraph('Pandas', styles['Heading4']),
        Paragraph('Proficiency: Beginner', styles['Normal']),

        #end of data bases section
        Spacer(1, 12),

        #Interests
        Paragraph('Interest Fields', styles['Heading2']),
        Paragraph('In my free time, I enjoy participating in coding challenges on LeetCode to further improve my problem-solving skills. Solving algorithmic problems is not only a hobby but also a way for me to continuously learn and grow as a developer; also, I love growing my garden and engaged in growing activities; I love learning Science and Applying Python to my daily commisions.', styles['Normal']),
        Spacer(1, 12),

        # Individual Traits
        Paragraph('Individual Traits', styles['Heading2']),
        Paragraph('As a highly motivated and dedicated individual, I am always eager to take on new challenges and explore innovative solutions. I am proactive in seeking opportunities for self-improvement and value continuous learning. My attention to detail and strong analytical skills enable me to approach complex problems with precision and creativity. I am a team player and believe in collaborative efforts to achieve project success.', styles['Normal']),
        Spacer(1, 12),

        #Projects

        Paragraph('Projects', styles['Heading2']),
        Spacer(1, 12),

        # Additional Information
        Paragraph('Additional Information', styles['Heading2']),
        Paragraph('LeetCode Profile:', styles['Heading3']),
        Paragraph('You can find my LeetCode profile at https://leetcode.com/user0513YQ/. I am committed to regularly solving coding challenges to enhance my coding abilities and stay updated with new algorithms and data structures.', styles['Normal']),
        Spacer(1, 12),

        Paragraph('Commitment to Growth:', styles['Heading3']),
        Paragraph('I am passionate about continuous learning and professional growth. I actively seek opportunities to attend workshops, webinars, and coding meetups to expand my knowledge and skills in software development. I believe that growth is an essential part of becoming a successful developer, and I am dedicated to pursuing it throughout my career.', styles['Normal']),
        Spacer(1, 12),
        Paragraph('My understanding of OOP', styles['Heading3']),
        Paragraph('welllllllll'),
        Spacer(1, 12)
    ]

    #Add the left and right content to the respective frames
    content.extend(left_content)
    content.append(PageBreak())
    content.extend(right_content)

    # Build the document
    doc.build(content, onFirstPage=draw_on_first_page)


if __name__ == "__main__":
    create_cv_pdf()