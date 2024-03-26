bot_user_not_authorized = "Вы еще не авторизовались в системе.\n Чтобы перейти к авторизации нажмите на кнопку"
# используется в клаве очев
AUTH_BUTTON = "Начать авторизацию"
generic_error_message = "Произошла ошибка. Сожалеем об этом"
select_project_action_message = "Выберите что необходимо сделать с проектом:"
CREATE_ISSUE_BUTTON = "Создать issue"
name_issue_message = "(1/5) Напишите название для будущего issue" # "Для отмены используйте команду /abort"
describe_issue_message = "(2/5) Отлично! Теперь придумайте описание для issue"
select_issue_severity_message = "(3/5) Теперь выберите уровень серьезности issue"
severity_variants = [
    "wishlist",
    "minor",
    "normal",
    "important",
    "critical"
]
select_issue_priority_message = "(4/5) Теперь выберите приоритет для issue"
priority_variants = [
    "low",
    "normal",
    "high"
]
select_issue_type_message = "(5/5) Наконец, выберите тип issue"
type_variants = [
    "bug",
    "question",
    "enhancement"
]
issue_type = 'bug'
if issue_type == type_variants[0]:
        issue_type = 3391300
elif issue_type == type_variants[1]:
    issue_type = 3391301
elif issue_type == type_variants[2]:
    issue_type = 3391302
print(type(issue_type))
