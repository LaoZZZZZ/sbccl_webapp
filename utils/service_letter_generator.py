from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


class ServiceLetter(Document):
    def __init__(self, data_path):
        super().__init__(default_filepath=data_path,documentclass='letter')
        self.preamble.append(Command('makeatletter'))
        # self.preamble.append(Command('def', '\\vhrulefill#1{\leavevmode\leaders\hrule\@height#1\hfill \kern\z@}'))
        self.preamble.append(Command('makeatother'))
        # self.preamble.append(Command('textwidth', '6.75in'))
        # self.preamble.append(Command('textheight', '9.25in'))
        # self.preamble.append(Command('oddsidemargin', '-.25in'))
        # self.preamble.append(Command('evensidemargin', '-.25in'))
        # self.preamble.append(Command('topmargin', '-1in'))
        # self.preamble.append(Command('longindentation', '0.50\textwidth'))
        # self.preamble.append(Command('parindent', '0.4in'))
        self.preamble.append(Command('title', 'Service Letter'))
        self.preamble.append(Command('author', 'SBCCL'))
        self.preamble.append(Command('date', NoEscape(r'\today')))
        # self.append(NoEscape(r'\maketitle'))
        

    def fill_in_letter(self, volunteer_name, start_date, end_date, hours):
        # self.append(NoEscape(r'\hfill'))
        self.append(NoEscape(r'\begin{letter}'))

        self.preamble.append(Command('hfill'))
        self.append(Command('toopening', 'Whome It May Concern,'))
        self.append(Command('noindent'))

        letter_body = """As Co-Principals of the Center for Chinese Learning at Stony Brook (SBCCL), 
        We, Guobin Hu and Yufang Yang, are very proud to write this letter to confirm 
        that {name}\'s service to our school. Tiffany has volunteered a total of {hours} 
        hours for our school from {start_date} to {end_date} (with no financial or material 
        payment). She worked as a Teaching Assistant in the Chinese class and was responsible 
        for setting up class activities, grading students works etc.""".format(
            name=volunteer_name, start_date=start_date, end_date=end_date, hours=hours)
        
        """Add boday to the letter."""
        self.append(letter_body)
        
        # self.preamble.append(Command('hfill'))
        self.append(Command('noindent'))
        self.append('Should you have any further questions please feel free to contact us by either email or phone call.')
        # self.preamble.append(Command('hfill'))
        self.append(Command('closing' 'Sincerely Yours,'))
        self.append(NoEscape(r'\end{letter}'))
    
if __name__ == '__main__':
    doc = ServiceLetter('/User/luzhao/Desktop')
    doc.fill_in_letter('Tiffany Gao', '2022-09-15', '2023-06-13', 38)
    # doc.generate_pdf("simple_letter", clean_tex=True, compiler='/usr/local/texlive/2023/bin/universal-darwin/latexmk')
    print(doc.dumps())  # The document as string in LaTeX syntax

 