import pulp
# Здесь получилось разбить по уму +\-, здесь гендер баланс уже меньшую роль играет. Просто раскидываем, чтобы женщин было +-
# одинаковой в каждой группе. Самый приятный вариант на данный момент.
# Список студентов
students = [
    {"name": "Ольга", "math": 90, "russian": 95, "third": 100, "third_subject": "informatics", "gender": 0, "wish": [1]},
    {"name": "Елена", "math": 95, "russian": 91, "third": 96, "third_subject": "informatics", "gender": 0, "wish": [1]},
    {"name": "Наталья", "math": 90, "russian": 92, "third": 94, "third_subject": "physics", "gender": 0, "wish": [1]},
    {"name": "Алексей", "math": 90, "russian": 85, "third": 95, "third_subject": "informatics", "gender": 1, "wish": [2]},
    {"name": "Марик", "math": 89, "russian": 84, "third": 90, "third_subject": "physics", "gender": 1, "wish": [1]},
    {"name": "Иван", "math": 100, "russian": 100, "third": 100, "third_subject": "informatics", "gender": 1, "wish": [2]},
    {"name": "Михали", "math": 75, "russian": 79, "third": 83, "third_subject": "informatics", "gender": 1, "wish": [2]},
    {"name": "Петр", "math": 78, "russian": 82, "third": 85, "third_subject": "physics", "gender": 1, "wish": [2]},
    {"name": "Сергей", "math": 93, "russian": 80, "third": 85, "third_subject": "physics", "gender": 1, "wish": [1]},
    {"name": "Дмитрий", "math": 80, "russian": 85, "third": 88, "third_subject": "informatics", "gender": 1, "wish": [1]}
]

N = len(students)
I = range(N)
MIN_STUDENTS = 6
K = range(1, min(5, N // MIN_STUDENTS + 1)) # Максимум N // 3 групп, минимум 1 группа
#Заменить все веса на переменные

# Расчет общего балла ЕГЭ с учетом весовых коэффициентов
for student in students:
    w = 1.1 if student["third_subject"] == "informatics" else 1.0
    student["total_score"] = (student["math"] + student["russian"] + w * student["third"]) / 100

# Создание модели задачи
model = pulp.LpProblem("Group_Assignment", pulp.LpMaximize)

x = pulp.LpVariable.dicts("x", [(i, k) for i in I for k in K], cat="Binary")

#Матрица предпочтений, кто с кем хочет. Пара предпочтений

# Целевая функция: Максимизация суммы баллов в первой группе и учет пожеланий студентов. Чуть увеличил штраф, чтобы чаще кидал в ту группу, которую хотят.
model += pulp.lpSum(students[i]["total_score"] * x[i, 1] for i in I) - (0.25 * pulp.lpSum((1 - x[i, k]) for i in I for k in K if k in students[i]["wish"]))


# Ограничения
# Каждый студент должен быть в одной и только одной группе
for i in I:
    model += pulp.lpSum(x[i, k] for k in K) == 1


# Размер группы должен быть в пределах от 3 до N человек (строго минимум 3)
for k in K:
    model += pulp.lpSum(x[i, k] for i in I) >= MIN_STUDENTS
    model += pulp.lpSum(x[i, k] for i in I) <= N

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
