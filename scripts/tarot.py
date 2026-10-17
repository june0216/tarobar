#!/usr/bin/env python3
"""타로바 카드 도구.

사용법:
  tarot.py draw N1 N2 N3   손님이 고른 숫자 3개로 3카드 스프레드를 뽑는다
  tarot.py list            78장 카드 목록과 정/역방향 의미를 출력한다
  tarot.py show QUERY      카드 번호나 이름(영문/한글 일부)으로 카드를 찾는다

draw는 덱 전체를 매번 새로 섞은 뒤 손님이 고른 자리의 카드를 뒤집는다.
그래서 같은 숫자를 골라도 매번 다른 카드가 나오고, 1번이 The Fool이라는 보장도 없다.
"""
import json
import random
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "cards.json"
IMAGE_BASE = "https://upload.wikimedia.org/wikipedia/commons/"
POSITIONS = ["과거", "현재", "미래"]
DECK_SIZE = 78

rng = random.SystemRandom()


def load_cards():
    with DATA.open(encoding="utf-8") as f:
        return json.load(f)


def image_url(card):
    return IMAGE_BASE + card["image"] + ".jpg"


def fail(message):
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


def parse_picks(args):
    if len(args) != 3:
        fail("숫자를 정확히 3개 골라야 합니다.")
    picks = []
    for raw in args:
        try:
            n = int(raw)
        except ValueError:
            fail(f"'{raw}'은(는) 숫자가 아닙니다.")
        if not 1 <= n <= DECK_SIZE:
            fail(f"{n}은(는) 1~{DECK_SIZE} 범위를 벗어났습니다.")
        picks.append(n)
    if len(set(picks)) != len(picks):
        fail("같은 숫자를 두 번 고를 수 없습니다.")
    return picks


def draw(args):
    picks = parse_picks(args)
    deck = load_cards()
    rng.shuffle(deck)

    spread = []
    for position, pick in zip(POSITIONS, picks):
        card = deck[pick - 1]
        reversed_ = rng.random() < 0.5
        spread.append({
            "position": position,
            "picked_number": pick,
            "name": card["name"],
            "ko": card["ko"],
            "orientation": "역방향" if reversed_ else "정방향",
            "meaning": card["reversed"] if reversed_ else card["upright"],
            "image_url": image_url(card),
        })

    header = "| " + " | ".join(f"{s['position']} · {s['orientation']}" for s in spread) + " |"
    divider = "|" + "---|" * len(spread)
    names = "| " + " | ".join(f"{s['name']} ({s['ko']})" for s in spread) + " |"
    images = "| " + " | ".join(f"![{s['name']}]({s['image_url']})" for s in spread) + " |"

    print(json.dumps({"ok": True, "spread": spread}, ensure_ascii=False, indent=2))
    print()
    print("\n".join([header, divider, names, images]))


def list_cards():
    for card in load_cards():
        print(f"{card['no']}. {card['name']} ({card['ko']}) / 정방향: {card['upright']} / 역방향: {card['reversed']}")


def show(args):
    if not args:
        fail("찾을 카드 번호나 이름을 입력하세요.")
    query = " ".join(args).strip().lower()
    cards = load_cards()
    if query.isdigit():
        matches = [c for c in cards if c["no"] == int(query)]
    else:
        matches = [c for c in cards if query in c["name"].lower() or query in c["ko"]]
    if not matches:
        fail(f"'{query}'에 해당하는 카드가 없습니다.")
    for card in matches:
        print(f"{card['no']}. {card['name']} ({card['ko']})")
        print(f"  정방향: {card['upright']}")
        print(f"  역방향: {card['reversed']}")
        print(f"  이미지: {image_url(card)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    command, args = sys.argv[1], sys.argv[2:]
    if command == "draw":
        draw(args)
    elif command == "list":
        list_cards()
    elif command == "show":
        show(args)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
