from data_collector.matches import get_latest_match
from analytics.draft_evaluator import evaluate_draft
from analytics.form_checker import get_player_form
from analytics.value_checker import evaluate_value
from analytics.logger import log_match_result

def main() -> None:
    match = get_latest_match()
    form = get_player_form(match)
    result = evaluate_draft(match, form)
    value = evaluate_value(match, result['winner'], result['confidence'])

    print(f"🔍 Матч: {match['team_a']} vs {match['team_b']}")
    print(f"📊 Форма: {match['team_a']} = {form['team_a_form']}, {match['team_b']} = {form['team_b_form']}")
    print(f"🤖 Прогноз: Победа {result['winner']} ({result['confidence']}%)")
    print(f"📌 Причина: {result['reason']}")
    print(f"💸 Ставка: {'✅ Value есть!' if value['value'] else '❌ Value нет'}")
    print(f"📈 Комментарий: {value['comment']}")

    log_match_result(match, result, value["value"])
    print("📝 Матч записан в журнал.")

if __name__ == "__main__":
    main()
