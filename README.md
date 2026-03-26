[![OpenHAB Tests](https://github.com/katsemir/15.2/actions/workflows/ci.yml/badge.svg)](https://github.com/katsemir/15.2/actions/workflows/ci.yml)

Практична робота 15.2 Варіант 1

## Testing Architecture

Проєкт використовує 4 типи тестів:

* Unit tests (логіка правил, edge cases)
* Integration tests (взаємодія правил)
* Simulation tests (симуляція пристроїв і подій)
* Performance tests (навантаження, швидкодія)

Всі тести написані з використанням `pytest`.

## Test Cases Catalog

* Перевірка логіки правил (світло, температура)
* Системні сценарії (двері + температура + сигналізація)
* Симуляція пристроїв (сенсори, події, час)
* Failure scenarios (помилки сенсорів)
* Performance тести (load, memory)

## Coverage Reports

Coverage генерується через:

```bash
pytest tests/test_unit_rules.py --cov=. --cov-report=term-missing
```

## CI Integration Guide

CI реалізовано через GitHub Actions.

Pipeline включає:

1. Встановлення залежностей
2. Валідацію конфігурації
3. Запуск тестів (`pytest tests`)
4. Збірку Docker образу
5. Симуляцію деплою

Запускається при:

* push
* pull request
