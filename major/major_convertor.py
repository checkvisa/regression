list = []
set = set(list)
with open('./mdict', 'r') as major:
	for line in major:
		key, value = line.strip().split(' ==> ')
		set.add(value)
print set

# ['Statistics', 'Optic Engieering', 'Social Science', 'Archeology', 'Thermal Engineering', 'Atmosphere & Marine Science', 'Architecture', 'Bio-engineering', 'Music', 'Medicine / Pathology / Pharmacy', 'Mathematics', 'Psychology', 'Biology', 'Materials Science/Engineering', 'Mechanical Engineering', 'Geology', 'Biomedical Engineering', 'MBA', 'Vehicle Engieering', 'Eletrical Engineering', 'Neuroscience', 'Business / Management', 'Biophysics Engineering', 'Aerospace Engineering', 'Information Science/Technology', 'Biochemical Engineering', 'Environmental Science', 'Finance', 'N/A', 'Chemical Engineering', 'English', 'Chemistry', 'Physics', 'Bioinformatics / Biostatistics', 'Polymer', 'Law', 'Art', 'Computer Science/Engineering', 'Industrial Engineering', 'Nuclear Engineering', 'Civil Engineering', 'Medical Engineering', 'Education', 'Agriculture', 'Energy', 'Geography']