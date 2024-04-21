import random

def random_nick():
    adjectives = ["Swift", "Lazy", "Crazy", "Mighty"]
    nouns = ["Fox", "Bear", "Wolf", "Eagle"]
    return random.choice(adjectives) + random.choice(nouns)

import uuid

def uuid_nick():
    # UUID4를 생성하고, 앞 8자리만 사용하여 닉네임을 생성합니다.
    return "User" + str(uuid.uuid4())[:8]
