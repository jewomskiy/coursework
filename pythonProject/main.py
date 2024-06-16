import pulp
# Здесь получилось разбить по уму +\-, но пульп считает гендер баланс наибольшим приорететом.
# Список студентов
students = [
    {"name": "Ольга", "math": 100, "russian": 100, "third": 100, "third_subject": "informatics", "gender": 0, "wish": [3]},
    {"name": "Елена", "math": 95, "russian": 91, "third": 96, "third_subject": "informatics", "gender": 0, "wish": [2]},
    {"name": "Наталья", "math": 90, "russian": 92, "third": 94, "third_subject": "physics", "gender": 0, "wish": [1]},
    {"name": "Алексей", "math": 90, "russian": 85, "third": 95, "third_subject": "informatics", "gender": 1, "wish": [2]},
    {"name": "Марик", "math": 100, "russian": 100, "third": 100, "third_subject": "physics", "gender": 1, "wish": [1]},
    {"name": "Иван", "math": 100, "russian": 100, "third": 100, "third_subject": "informatics", "gender": 1, "wish": [2]},
    {"name": "Михали", "math": 100, "russian": 100, "third": 100, "third_subject": "informatics", "gender": 1, "wish": [2]},
    {"name": "Петр", "math": 78, "russian": 82, "third": 85, "third_subject": "physics", "gender": 1, "wish": [2]},
    {"name": "Сергей", "math": 100, "russian": 100, "third": 100, "third_subject": "physics", "gender": 1, "wish": [1]},
    {"name": "Дмитрий", "math": 80, "russian": 85, "third": 88, "third_subject": "informatics", "gender": 1, "wish": [1]}
]

N = len(students)
I = range(N)
K = range(1, N // 4 + 1)  # Максимум N // 4 групп, минимум 1 группа

# Расчет общего балла ЕГЭ с учетом весовых коэффициентов
for student in students:
    w = 1.1 if student["third_subject"] == "informatics" else 1.0
    student["total_score"] = (student["math"] + student["russian"] + w * student["third"]) / 100

# Создание модели задачи
model = pulp.LpProblem("Group_Assignment", pulp.LpMaximize)

x = pulp.LpVariable.dicts("x", [(i, k) for i in I for k in K], cat="Binary")

# Целевая функция: Максимизация суммы баллов в первой группе и учет пожеланий студентов
model += pulp.lpSum(students[i]["total_score"] * x[i, 1] for i in I) - 0.1 * pulp.lpSum((1 - x[i, k]) for i in I for k in K if k in students[i]["wish"])


# Ограничения
# Каждый студент должен быть в одной и только одной группе
for i in I:
    model += pulp.lpSum(x[i, k] for k in K) == 1

# Размер группы должен быть в пределах от 4 до N человек (строго минимум 4)
for k in K:
    model += pulp.lpSum(x[i, k] for i in I) >= 4
    model += pulp.lpSum(x[i, k] for i in I) <= N

# Гендерный баланс в каждой группе
for k in K:
    model += pulp.lpSum(x[i, k] * students[i]["gender"] for i in I) == pulp.lpSum(x[i, k] * (1 - students[i]["gender"]) for i in I)

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
for k in K:
    print(f"Group {k}: {groups[k]}")
    for i in groups[k]:
        print(f"\t{i}: {students[i]}")
