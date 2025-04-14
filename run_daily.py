# run_daily.py
import os
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def run_script(script_path: str) -> None:
    full_path = os.path.join(PROJECT_ROOT, script_path)
    print(f"\n▶️ Запуск: {full_path}")
    try:
        result = subprocess.run(
            ["python", full_path],
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(f"✅ Успешно: {os.path.basename(script_path)}")
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка в {os.path.basename(script_path)}:")
        print(e.stdout.strip())
        print(e.stderr.strip())

def run_daily_cycle() -> None:
    print("🚀 Запуск полного автопакета GameChanger...\n")
    scripts = [
        "data_collector/update_meta.py",
        "data_collector/fetch_matches.py",
        "data_collector/combine_data.py",
        "ml/train_model.py",
        "ml/auto_update.py",
        "analytics/auto_predictor.py",
        "analytics/results_updater.py",
        "analytics/stats.py"
    ]
    for script in scripts:
        run_script(script)

    print("\n✅ Готово! Всё обновлено и сохранено.")

if __name__ == "__main__":
    run_daily_cycle()
