from exams.models import Grade
def save_grade(student, course, midterm, final_exam, absences):
    final_grade = (float(midterm) * 0.4) + (float(final_exam) * 0.6)
    letter_grade = "DZ" if int(absences) > 3 else get_letter_grade(final_grade)
    eligibility = determine_eligibility(letter_grade)

    Grade.objects.update_or_create(
        student=student,
        course=course,
        defaults={
            'midterm_grade': midterm,
            'final_exam_grade': final_exam,
            'final_grade': final_grade,
            'letter_grade': letter_grade,
            'eligibility': eligibility,
            'absences': absences,
        }
    )

def get_letter_grade(score):
    if score >= 90:
        return 'AA'
    elif score >= 85:
        return 'BA'
    elif score >= 80:
        return 'BB'
    elif score >= 75:
        return 'CB'
    elif score >= 70:
        return 'CC'
    elif score >= 65:
        return 'DC'
    elif score >= 60:
        return 'DD'
    elif score >= 55:
        return 'FD'
    else:
        return 'FF'

def determine_eligibility(letter_grade):
    return "Eligible" if letter_grade in ["DD", "FD", "FF"] else "Not Eligible"
