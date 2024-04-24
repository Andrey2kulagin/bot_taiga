from tgbot.handlers.utils.notification_service import send_notification_message


def parse_taiga_webhook(data):
    action = data['action']
    issue_data = data['data']
    issue_subject = issue_data['subject']
    issue_permalink = issue_data['permalink']
    project_name = issue_data['project']['name']
    project_permalink = issue_data['project']['permalink']
    notification = f'[{project_name}]({project_permalink})\n'
    if action == 'create':
        return f'Создан новый issue: "[{issue_subject}]({issue_permalink})"'
    elif action == 'change':
        change_data = data['change']
        notification += f'Изменен issue: "[{issue_subject}]({issue_permalink})". Изменения:'
        if change_data['comment'] != "":
            print('[e')
            notification = f'[{project_name}]({project_permalink})\n'
            comment_text = change_data['comment']
            comment_by = data['by']['full_name']
            comment_by_username = data['by']['username']
            comment_by_permalink = data['by']['permalink']
            # Новый комментарий
            if (change_data['comment_versions'] is None) and (change_data['delete_comment_date'] is None):
                notification += f'{comment_by} ([{comment_by_username}]({comment_by_permalink})) оставил комментарий в issue "[{issue_subject}]({issue_permalink})": \n_{comment_text}_'
            # Измененный комментарий
            elif (change_data['delete_comment_date'] is None):
                notification += f'{comment_by} ([{comment_by_username}]({comment_by_permalink})) изменил комментарий в issue "[{issue_subject}]({issue_permalink})": \n_{comment_text}_'
            # Удаленный комментарий
            else:
                notification += f'{comment_by} ([{comment_by_username}]({comment_by_permalink})) удалил комментарий в issue "[{issue_subject}]({issue_permalink})": \n_{comment_text}_'
        elif 'type' in change_data['diff']:
            type_change = change_data['diff']['type']
            notification += f'\n- Тип изменен с "{type_change["from"]}" на "{type_change["to"]}"'

        elif 'status' in change_data['diff']:
            status_change = change_data['diff']['status']
            notification += f'\n- Статус изменен с "{status_change["from"]}" на "{status_change["to"]}"'

        elif 'severity' in change_data['diff']:
            severity_change = change_data['diff']['severity']
            notification += f'\n- Важность изменена с "{severity_change["from"]}" на "{severity_change["to"]}"'

        elif 'priority' in change_data['diff']:
            priority_change = change_data['diff']['priority']
            notification += f'\n- Приоритет изменен с "{priority_change["from"]}" на "{priority_change["to"]}"'

        elif 'assigned_to' in change_data['diff']:
            assigned_to_change = change_data['diff']['assigned_to']
            from_assigned = assigned_to_change['from'] if assigned_to_change['from'] else 'никто'
            to_assigned = assigned_to_change['to'] if assigned_to_change['to'] else 'никто'
            notification += f'\n- Изменен ответственный с "{from_assigned}" на "{to_assigned}"'

        elif 'due_date' in change_data['diff']:
            due_date_change = change_data['diff']['due_date']
            notification += f'\n- Срок выполнения изменен с "{due_date_change["from"]}" на "{due_date_change["to"]}"'

        elif 'is_blocked' in change_data['diff']:
            is_blocked_change = change_data['diff']['is_blocked']
            notification += f'\n- Изменено значение "is_blocked" с "{is_blocked_change["from"]}" на "{is_blocked_change["to"]}"'

        return notification
    elif action == 'delete':
        return f'Удален issue: "{issue_subject}" ({issue_permalink})'
    else:
        return 'Действие не поддерживается'


def get_ping_tg_ids(data):
    issue_data = data['data']
    # id смотрящих событие, список
    watchers_taiga_id = issue_data['watchers']
    # объект показывающий кому назначено
    assigned_to = issue_data['assigned_to']
    # список всех id кому надо отправить уведомление
    ping_ids = []
    print('------------------')
    print('watchers', watchers_taiga_id)
    print('assigned_to', issue_data['assigned_to'])
    print('------------------')

    if watchers_taiga_id or (None not in watchers_taiga_id):
        ping_ids.extend(watchers_taiga_id)

    if (assigned_to is not None) and (assigned_to['id'] not in ping_ids):
        ping_ids.append(assigned_to['id'])
    print("ping ids", ping_ids)
    return ping_ids


def send_notifications(data):
    parsed_data = parse_taiga_webhook(data)
    if parsed_data != 'Действие не поддерживается':
        ping_ids = get_ping_tg_ids(data)
        for i in ping_ids:
            send_notification_message(i, parsed_data)
