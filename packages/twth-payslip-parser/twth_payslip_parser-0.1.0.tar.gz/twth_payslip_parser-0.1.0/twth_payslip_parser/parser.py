import datetime

def LTTextBoxHorizontal(pdf, index):
    return pdf.pq("LTTextBoxHorizontal[index='%s']" % index)

def get_date(pdf):
    return datetime.datetime.strptime(
        LTTextBoxHorizontal(pdf, 10)[0].text.strip(),
        "%d/%m/%Y"
    )

def get_income_or_deductions(pdf, index, transform):
    elements = LTTextBoxHorizontal(pdf, index=index)[0].getchildren()
    values = [
        transform(l.text) for l in elements
    ]

    return values

def parse(pdf):
    income_labels_transform = lambda x: x.strip().strip(":").strip()
    income_labels = get_income_or_deductions(pdf, 3, income_labels_transform)

    income_numbers_transform = lambda x: float(x.strip().strip(":").replace(",",""))
    income_numbers = get_income_or_deductions(pdf, 12, income_numbers_transform)

    deduction_labels_transform = lambda x: x.strip().strip(":")
    deduction_labels = get_income_or_deductions(pdf, 13, deduction_labels_transform)

    deduction_numbers_transform = lambda x: float(x.strip().replace(",",""))
    deduction_numbers = get_income_or_deductions(pdf, 14, deduction_numbers_transform)

    data = {}

    data['date'] = get_date(pdf)

    data['income'] = {
        "items": list(zip(income_labels, income_numbers))
    }
    data['deductions'] = {
        "items": list(zip(deduction_labels, deduction_numbers))
    }

    data['income']['total'] = round(sum([i[1] for i in data['income']['items']]), 2)
    data['deductions']['total'] = round(sum([i[1] for i in data['deductions']['items']]), 2)

    data['deposit'] = round(data['income']['total'] - data['deductions']['total'], 2)

    return data
