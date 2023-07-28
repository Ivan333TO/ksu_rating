import json
import re
import os
from typing import Any, Dict, List

def verify_snils(snils: str) -> bool:
    pattern = r'\b\d\d\d-\d\d\d-\d\d\d \d\d\b'
    return re.match(pattern, snils) is not None or snils.isdigit()

def search_snils(SNILS: str) -> List[Dict[str, Any]]:
    res = []
    titles = os.listdir('data/')
    for title in titles:
        with open(f'data/{title}', 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            if SNILS in data['Конкурс']:
                res.append(data)
    return res

def format_snils_result(snils: str, json: Dict[str, Any]) -> str:
    ball = json['Конкурс'][snils]['Сумма баллов']

    res = f"{json['Направление']}\n" \
          f"Бюджетных мест: {json['Места']}\n\n" \
          f"Приоритет: {json['Конкурс'][snils]['Приоритет']}\n" \
          f"Сумма баллов: {ball}\n" \
          f"Место в списке: {json['Конкурс'][snils]['Номер']}/{json['Места']}\n" \
          f"Место в списке оригиналов: {json['Конкурс'][snils]['Место в списке оригиналов']}/{json['Места']}\n" \
          f"Место в списке: оригинал+высший приоритет: {json['Конкурс'][snils]['Место в списке: оригинал+высший приоритет']}/{json['Места']}\n" \

    return res