import json
import os
import importlib.util

def load_classes_from_directory(directory):
    classes = []  # 로드된 클래스를 저장할 리스트

    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # 확장자 제거
            module_path = os.path.join(directory, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type):  # 클래스인지 확인
                    classes.append(attribute)

    return classes

# 사용 예시
directory_path = 'switcore/ui'  # 디렉토리 경로 설정
loaded_classes = load_classes_from_directory(directory_path)

# 로드된 클래스 출력
for cls in loaded_classes:
    if hasattr(cls, 'model_json_schema'):
        method = getattr(cls, 'model_json_schema')
        print("######################start########################")
        print(cls)
        result = method()
        print(json.dumps(result, indent=2))
        print("######################end########################")
    # print(cls)
