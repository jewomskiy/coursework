import pulp
import random
# Здесь получилось разбить по уму +\-, здесь гендер баланс уже меньшую роль играет. Просто раскидываем, чтобы женщин было +-
# одинаковой в каждой группе. Самый приятный вариант на данный момент.
# Список студентов
students = [
    {"name": "Ольга", "math": 100, "russian": 100, "third": 100, "third_subject": "informatics", "gender": 0,
     "preferences": ["Наталья", "Алина", "Ирина", "Александр"]},
    {"name": "Елена", "math": 99, "russian": 99, "third": 99, "third_subject": "informatics", "gender": 0,
     "preferences": ["Ольга", "Наталья", "Ирина", "Светлана"]},
    {"name": "Наталья", "math": 100, "russian": 100, "third": 100, "third_subject": "physics", "gender": 0,
     "preferences": ["Ольга", "Алина", "Ирина", "Светлана"]},
    {"name": "Алексей", "math": 100, "russian": 100, "third": 100, "third_subject": "informatics", "gender": 1,
     "preferences": ["Елена", "Марик", "Иван", "Дмитрий"]},
    {"name": "Марик", "math": 100, "russian": 100, "third": 100, "third_subject": "physics", "gender": 1,
     "preferences": ["Елена", "Алексей", "Иван", "Дмитрий"]},
    {"name": "Иван", "math": 30, "russian": 30, "third": 30, "third_subject": "informatics", "gender": 1,
     "preferences": ["Елена", "Алексей", "Марик", "Дмитрий"]},
    {"name": "Михали", "math": 65, "russian": 70, "third": 75, "third_subject": "informatics", "gender": 1,
     "preferences": ["Петр", "Сергей", "Александр", "Константин"]},
    {"name": "Петр", "math": 78, "russian": 82, "third": 80, "third_subject": "physics", "gender": 1,
     "preferences": ["Михали", "Сергей", "Александр", "Константин"]},
    {"name": "Сергей", "math": 85, "russian": 80, "third": 79, "third_subject": "physics", "gender": 1,
     "preferences": ["Михали", "Петр", "Александр", "Константин"]},
    {"name": "Дмитрий", "math": 75, "russian": 85, "third": 80, "third_subject": "informatics", "gender": 1,
     "preferences": ["Елена", "Алексей", "Марик", "Иван"]},
    {"name": "Алина", "math": 83, "russian": 76, "third": 81, "third_subject": "informatics", "gender": 0,
     "preferences": ["Алексей", "Марик", "Иван", "Дмитрий"]},
    {"name": "Ирина", "math": 75, "russian": 78, "third": 70, "third_subject": "informatics", "gender": 0,
     "preferences": ["Ольга", "Наталья", "Алина", "Светлана"]},
    {"name": "Светлана", "math": 90, "russian": 85, "third": 87, "third_subject": "physics", "gender": 0,
     "preferences": ["Наталья", "Алина", "Ирина", "Александр"]},
    {"name": "Александр", "math": 85, "russian": 89, "third": 92, "third_subject": "informatics", "gender": 1,
     "preferences": ["Михали", "Петр", "Сергей", "Константин"]},
    {"name": "Виктор", "math": 80, "russian": 77, "third": 85, "third_subject": "physics", "gender": 1,
     "preferences": ["Фёдор", "Григорий", "Максим", "Антон"]},
    {"name": "Константин", "math": 78, "russian": 80, "third": 79, "third_subject": "informatics", "gender": 1,
     "preferences": ["Михали", "Петр", "Сергей", "Александр"]},
    {"name": "Фёдор", "math": 88, "russian": 84, "third": 89, "third_subject": "informatics", "gender": 1,
     "preferences": ["Виктор", "Григорий", "Максим", "Антон"]},
    {"name": "Григорий", "math": 82, "russian": 80, "third": 85, "third_subject": "physics", "gender": 1,
     "preferences": ["Виктор", "Фёдор", "Максим", "Антон"]},
    {"name": "Максим", "math": 79, "russian": 77, "third": 80, "third_subject": "informatics", "gender": 1,
     "preferences": ["Виктор", "Фёдор", "Григорий", "Антон"]},
    {"name": "Антон", "math": 84, "russian": 83, "third": 86, "third_subject": "physics", "gender": 1,
     "preferences": ["Виктор", "Фёдор", "Григорий", "Максим"]}
]

# Создание случайных пожеланий для каждого студента
# for student in students:
#     preferences = random.sample([other_student["name"] for other_student in students if other_student["name"] != student["name"]], random.randint(3, 4))
#     student["preferences"] = preferences

N = len(students)
I = range(N)
MIN_STUDENTS = 6
K = range(1, min(5, N // MIN_STUDENTS + 1)) # Максимум N // 3 групп, минимум 1 группа
#Заменить все веса на переменные

def create_preferences_matrix(students):
    name_to_index = {student["name"]: i for i, student in enumerate(students)}
    preferences_matrix = [[0] * N for _ in range(N)]
    for i, student in enumerate(students):
        for preferred_name in student["preferences"]:
            j = name_to_index[preferred_name]
            preferences_matrix[i][j] = 1
    return preferences_matrix

preferences = create_preferences_matrix(students)

# Расчет общего балла ЕГЭ с учетом весовых коэффициентов
for student in students:
    w = 1.1 if student["third_subject"] == "informatics" else 1.0
    student["total_score"] = (student["math"] + student["russian"] + w * student["third"]) / 100

# Создание модели задачи
model = pulp.LpProblem("Group_Assignment", pulp.LpMaximize)

x = pulp.LpVariable.dicts("x", [(i, k) for i in I for k in K], cat="Binary")
y = pulp.LpVariable.dicts("y", [(i, j, k) for i in I for j in I for k in K], cat="Binary")

#Матрица предпочтений, кто с кем хочет. Пара предпочтений

# Целевая функция: Максимизация суммы баллов в первой группе и учет пожеланий студентов.
model += pulp.lpSum(students[i]["total_score"] * x[i, k] * k for i in I for k in K) + 0.2 * pulp.lpSum(preferences[i][j] * y[i, j, k] for i in I for j in I for k in K)

# Ограничения
# Каждый студент должен быть в одной и только одной группе
for i in I:
    model += pulp.lpSum(x[i, k] for k in K) == 1


# Размер группы должен быть в пределах
for k in K:
    model += pulp.lpSum(x[i, k] for i in I) >= MIN_STUDENTS
    model += pulp.lpSum(x[i, k] for i in I) <= N

#Убеждаемся, что пожелания не ломают нам ничего и нигде студент не появляется дважды.
for i in I:
    for j in I:
        if i != j:
            for k in K:
                model += y[i, j, k] <= x[i, k]
                model += y[i, j, k] <= x[j, k]
                model += y[i, j, k] >= x[i, k] + x[j, k] - 1
# Гендерный баланс в каждой группе. Теперь стремися к тому, чтобы у нас просто было равное количество женщин во всех группах. Минус в том, что сильная женщина
# может попасть к тупым мужчинам. Слишком большая разница в баллах.
total_women = sum(1 for student in students if student["gender"] == 0)
min_women_per_group = total_women // len(K)
max_women_per_group = min_women_per_group + 1

for k in K:
    model += pulp.lpSum(x[i, k] * (1 - students[i]["gender"]) for i in I) >= min_women_per_group
    model += pulp.lpSum(x[i, k] * (1 - students[i]["gender"]) for i in I) <= max_women_per_group


model.solve()

# Убираем пустые группы.
active_groups = [k for k in K if pulp.value(pulp.lpSum(x[i, k] for i in I)) > 0]


# Собираем студентов
groups = {k: [] for k in active_groups}
for k in active_groups:
    for i in I:
        if pulp.value(x[i, k]) == 1:
            groups[k].append(i)

# Вывод групп
for k in active_groups:
    print(f"Group {k}: {groups[k]}")
    for i in groups[k]:
        print(f"\t{i}: {students[i]}")

# GAMS(солвер) - посмотреть, сравнить. И с SciPy сравнить.
