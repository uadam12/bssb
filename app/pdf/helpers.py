from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from io import BytesIO

def get_widths(lengths):
    total_length = sum(lengths)
    total_width = 15 * cm
    p = 4 * cm / len(lengths)
    
    return [
        (length * total_width / total_length) + p for length in lengths
    ]


class Icon(Image):
    def __init__(self, image_path):
        super().__init__(
            image_path,
            width=3*cm, 
            height=3.5*cm
        )

class H1(Paragraph):
    def __init__(self, title, id):
        text = [
            '<b>',
            'Borno State Scholarship Board',
            title, 'Application Form', id, 
            '</b>'
        ]
        style = ParagraphStyle(
            name='Title', 
            fontSize=14, 
            spaceAfter=12, 
            alignment=1, 
            fontName='Helvetica-Bold'
        )
        super().__init__(
            "<br /><br />".join(text), style
        )
    
class Text(Paragraph):
    body_style = getSampleStyleSheet()['BodyText']
    def __init__(self, text):
        super().__init__(
            text, self.body_style
        )

class P(Text):
    def __init__(self, key, value):
        super().__init__(
            f"<b>{key}</b><br/>{value}"
        )

class Row(Table):
    def __init__(self, *cells):
        data = [P(k, v) for k, v in cells]
        lengths = get_widths([
            max(len(k), len(v)) for k, v in cells
        ])
        
        super().__init__(
            [data], colWidths=lengths
        )

class Signature(Table):
    def __init__(self, date):
        data = [
            P('Applied On', date),
            P(40*'_', "Applicant's Signature")
        ]

        super().__init__(
            [data], colWidths=[None, 8.5*cm]
        )

class Grid(Table):
    style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black), 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    def __init__(self, rows):
        lengths = get_widths([
            len(max(col, key=len)) 
            for col in zip(*rows)
        ])

        data = [[
            Text(f"<b>{cell}</b>") for cell in rows[0]
        ]]

        for i in range(1, len(rows)):
            data.append([
                Text(cell) for cell in rows[i]
            ])

        super().__init__(
            data, colWidths=lengths
        )
        self.setStyle(self.style)

class Header(Table):
    def __init__(self, logo, title, id, avater):
        super().__init__(
            [
                [
                    Icon(logo), H1(title, id), Icon(avater)
                ]
            ], colWidths = [
                3*cm, 13*cm, 3*cm
            ]
        )
        self.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, 0), 'CENTER'), 
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))


class DrawLineBelow(Flowable):
    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width

    def draw(self):
        self.canv.setLineWidth(1)  # Line thickness
        self.canv.line(0, 0, self.width, 0)

class PDFDoc(SimpleDocTemplate):
    section_header_style = ParagraphStyle(
        name='SectionHeader', 
        fontSize=12, 
        spaceAfter=6, 
        alignment=0, 
        fontName='Helvetica-Bold'
    )

    def __init__(self):
        self.bssb_buffer = BytesIO()
        
        super().__init__(
            self.bssb_buffer, pagesize=A4, 
            rightMargin= cm, 
            leftMargin= cm, 
            topMargin= cm, 
            bottomMargin= cm
        )
        self.elements = []

    def add(self, element):
        self.elements.append(element)
    
    def add_line(self, width):
        line = DrawLineBelow(width)
        self.add(line)

    def add_space(self, space=12):
        self.add(Spacer(1, space))
 
    def add_header(self, header):
        self.add_space()
        self.add(Paragraph(
            header, self.section_header_style
        ))
        
        self.add_line(self.width-5)

        
    def generate_pdf(self):
        self.build(self.elements)
        pdf = self.bssb_buffer.getvalue()
        self.bssb_buffer.close()
        
        return pdf