import os
import sys
import subprocess
import logging

# Настройка логирования для вывода информации о процессе
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Путь к файлу с учетными данными Cloudflare API для Certbot.
# Этот файл должен содержать API-токен Cloudflare, необходимый для DNS-аутентификации.
CLOUDFLARE_CREDENTIALS_PATH = os.path.expanduser("~/.secrets/cloudflare.ini")

# Email для регистрации в Let's Encrypt и получения уведомлений.
# ВНИМАНИЕ: Замените на реальный адрес электронной почты.
CERTBOT_EMAIL = "your_email@example.com"

def is_certbot_installed() -> bool:
    """
    Проверяет, установлен ли Certbot в системе.

    Возвращает:
        bool: True, если Certbot установлен, иначе False.
    """
    try:
        # Попытка выполнить команду certbot --version для проверки его наличия.
        subprocess.run(["certbot", "--version"], check=True, capture_output=True)
        logging.info("Certbot установлен.")
        return True
    except FileNotFoundError:
        logging.error("Certbot не найден. Пожалуйста, установите его.")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при проверке Certbot: {e.stderr.decode().strip()}")
        return False

def issue_wildcard_certificate(domain: str) -> None:
    """
    Запускает Certbot для выпуска wildcard-сертификата Let's Encrypt
    для указанного домена с использованием DNS-аутентификации Cloudflare.

    Аргументы:
        domain (str): Основной домен, для которого будет выпущен сертификат (например, "example.com").
                      Будет запрошен сертификат как для 'domain', так и для '*.domain'.
    """
    if not os.path.exists(CLOUDFLARE_CREDENTIALS_PATH):
        logging.error(
            f"Файл с учетными данными Cloudflare '{CLOUDFLARE_CREDENTIALS_PATH}' не найден. "
            "Пожалуйста, создайте его и добавьте API-токен Cloudflare."
        )
        sys.exit(1)

    # Формирование команды Certbot
    # certonly: Только получить или обновить сертификат, без автоматической настройки веб-сервера.
    # --dns-cloudflare: Использовать плагин DNS-01 аутентификации для Cloudflare.
    # --dns-cloudflare-credentials: Указывает путь к файлу с учетными данными Cloudflare.
    # -d: Указывает домены для которых выпускается сертификат (основной домен и wildcard).
    # --agree-tos: Автоматически соглашается с условиями обслуживания Let's Encrypt.
    # --email: Указывает адрес электронной почты для уведомлений Let's Encrypt.
    # --non-interactive: Запускает Certbot в неинтерактивном режиме.
    cmd = [
        "sudo", "certbot", "certonly",
        "--dns-cloudflare",
        f"--dns-cloudflare-credentials={CLOUDFLARE_CREDENTIALS_PATH}",
        "-d", f"*.{domain}", "-d", domain,
        "--agree-tos",
        "--email", CERTBOT_EMAIL,
        "--non-interactive",
        "--keep-until-expiring" # Продлевать сертификат только когда он близок к истечению
    ]

    logging.info(f"Запуск Certbot для выпуска сертификата для домена: {domain}")
    try:
        # Выполнение команды Certbot.
        # capture_output=True позволяет захватить stdout и stderr для логирования.
        # text=True декодирует вывод как текст.
        process = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info("Сертификат успешно выпущен/обновлен.")
        logging.debug(f"Certbot stdout:\n{process.stdout}")
        logging.debug(f"Certbot stderr:\n{process.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выпуске/обновлении сертификата Certbot для {domain}:")
        logging.error(f"Код возврата: {e.returncode}")
        logging.error(f"stdout:\n{e.stdout}")
        logging.error(f"stderr:\n{e.stderr}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Непредвиденная ошибка при выполнении Certbot: {e}")
        sys.exit(1)

def main():
    """
    Основная функция скрипта.
    Проверяет предусловия и запускает процесс выпуска сертификата.
    """
    if not is_certbot_installed():
        logging.error(
            "Certbot не установлен. Пожалуйста, установите его, выполнив команду: "
            "sudo apt install certbot python3-certbot-dns-cloudflare"
        )
        sys.exit(1)

    if len(sys.argv) < 2:
        logging.error("Не указан домен. Использование: python ssl_issue.py example.com")
        sys.exit(1)

    domain_to_issue = sys.argv[1]
    issue_wildcard_certificate(domain_to_issue)
    logging.info(f"Процесс выпуска/обновления сертификата для {domain_to_issue} завершен.")

if __name__ == "__main__":
    main()