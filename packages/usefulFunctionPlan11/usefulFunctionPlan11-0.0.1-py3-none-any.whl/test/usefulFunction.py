import re

def validate_email(email):
    """이메일 주소가 유효한 형식인지 확인합니다."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def remove_duplicates_and_sort(input_list):
    """리스트에서 중복을 제거하고 정렬된 결과를 반환합니다."""
    return sorted(set(input_list))

# 사용 예시
email = "example@example.com"
print("이메일 유효성 검사:", validate_email(email))

sample_list = [3, 1, 2, 3, 4, 2, 5]
print("중복 제거 및 정렬 결과:", remove_duplicates_and_sort(sample_list))
