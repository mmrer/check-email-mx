import re
from dns import resolver, exception


def extract_domain(email):
    """Извлекает домен из email-адреса"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$'
    match = re.match(email_pattern, email.strip())
    if match:
        return match.group(1)
    return None


def check_mx_records(domain):
    """Проверяет наличие MX-записей для домена"""
    try:
        mx_records = resolver.resolve(domain, 'MX')
        if len(mx_records) == 0:
            return "MX-записи отсутствуют или некорректны"
        return "домен валиден"
    except resolver.NXDOMAIN:
        return "домен отсутствует"
    except (resolver.NoAnswer, exception.DNSException):
        return "MX-записи отсутствуют или некорректны"


def main():
    """Основная функция"""
    input_file = "email.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_file}' не найден.")
        print(f"Создайте файл '{input_file}' с email-адресами (по одному на строку).")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла '{input_file}': {e}")
        return
    
    if not emails:
        print(f"Файл '{input_file}' пуст.")
        return
    
    print(f"Проверка {len(emails)} email-адресов из файла '{input_file}':\n")
    
    # Обрабатываем каждый email
    for email in emails:
        domain = extract_domain(email)
        # Если не удалось извлечь домен из email, пробуем проверить сам email как домен
        if not domain:
            domain = email.strip()
        
        message = check_mx_records(domain)
        print(f"{email}: {message}")


if __name__ == "__main__":
    main()

