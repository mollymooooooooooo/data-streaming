# Поток данных в реальном времени
## Структура проекта
- **Источник данных**: Использован API сайта randomuser.me (генерация случайных данных людей)
- **Apache Kafka (с Zookeeper)**: Для потоковой передачи данных из PostgreSQL
- **Apache Airflow**: Для организации оркестрации контейнера и хранения полученных данных в БД PostgreSQL
- **Apache Spark**: Для обработки данных
- **Cassandra**: Для хранения обработанных данных
- **Control Center и Schema Registry**: Для мониторинга и управления схемами потоков в Kafka

## Технологии
- Python
- Apache Airflow
- Apache Kafka
- Apache Spark
- Cassandra
- Apache Zookeeper
- PostgreSQL
- Docker
