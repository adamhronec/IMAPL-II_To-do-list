import requests

BASE_URL = "http://127.0.0.1:5000"

# Globálny prehľad
vysledky = []


def log_result(test_name, success, detail=""):
    status = "✅" if success else "❌"
    print(f"{status} {test_name} {'prešiel' if success else 'neprešiel'}")
    if detail and not success:
        print(f"   🔎 Detail: {detail}")
    vysledky.append((test_name, success))


def test_server_connection():
    try:
        response = requests.get(BASE_URL + "/")
        log_result("test_server_connection", response.status_code == 200, f"Status: {response.status_code}")
    except Exception as e:
        log_result("test_server_connection", False, str(e))


def test_create_task():
    data = {
        "text": "Test úloha",
        "description": "Toto je test",
        "due_date": "2025-12-31",
        "user_name": "tester"
    }
    try:
        response = requests.post(f"{BASE_URL}/ulohy", json=data)
        success = response.status_code == 201 and "id" in response.json()
        log_result("test_create_task", success, response.text)
        return response.json().get("id") if success else None
    except Exception as e:
        log_result("test_create_task", False, str(e))
        return None


def test_get_tasks():
    try:
        response = requests.get(f"{BASE_URL}/ulohy?user_name=tester")
        data = response.json()
        success = response.status_code == 200 and isinstance(data, list)
        log_result("test_get_tasks", success, response.text)
    except Exception as e:
        log_result("test_get_tasks", False, str(e))


def test_update_task(task_id):
    if not task_id:
        log_result("test_update_task", False, "Neplatné ID úlohy")
        return
    try:
        response = requests.put(f"{BASE_URL}/ulohy/{task_id}", json={
            "text": "Aktualizovaná úloha",
            "done": True
        })
        log_result("test_update_task", response.status_code == 200, response.text)
    except Exception as e:
        log_result("test_update_task", False, str(e))


def test_delete_task(task_id):
    if not task_id:
        log_result("test_delete_task", False, "Neplatné ID úlohy")
        return
    try:
        response = requests.delete(f"{BASE_URL}/ulohy/{task_id}")
        log_result("test_delete_task", response.status_code == 200, response.text)
    except Exception as e:
        log_result("test_delete_task", False, str(e))


def test_invalid_post():
    try:
        response = requests.post(f"{BASE_URL}/ulohy", json={"user_name": "tester"})
        log_result("test_invalid_post", response.status_code == 400, response.text)
    except Exception as e:
        log_result("test_invalid_post", False, str(e))


def test_put_nonexistent_task():
    try:
        response = requests.put(f"{BASE_URL}/ulohy/99999", json={"text": "Nič"})
        log_result("test_put_nonexistent_task", response.status_code == 404, response.text)
    except Exception as e:
        log_result("test_put_nonexistent_task", False, str(e))


def test_delete_nonexistent_task():
    try:
        response = requests.delete(f"{BASE_URL}/ulohy/99999")
        log_result("test_delete_nonexistent_task", response.status_code == 404, response.text)
    except Exception as e:
        log_result("test_delete_nonexistent_task", False, str(e))


def test_empty_tasks_for_unknown_user():
    try:
        response = requests.get(f"{BASE_URL}/ulohy?user_name=nikto-nikdy-nebol")
        data = response.json()
        success = response.status_code == 200 and data == []
        log_result("test_empty_tasks_for_unknown_user", success, response.text)
    except Exception as e:
        log_result("test_empty_tasks_for_unknown_user", False, str(e))


if __name__ == "__main__":
    print("🚀 Spúšťam testy...\n")

    test_server_connection()
    task_id = test_create_task()
    test_get_tasks()
    test_update_task(task_id)
    test_delete_task(task_id)

    test_invalid_post()
    test_put_nonexistent_task()
    test_delete_nonexistent_task()
    test_empty_tasks_for_unknown_user()

    # Zhrnutie
    print("\n📊 Výsledky testov:")
    for name, result in vysledky:
        status = "OK" if result else "ZLYHAL"
        print(f" - {name}: {status}")

    total = len(vysledky)
    passed = sum(1 for _, ok in vysledky if ok)
    print(f"\n✅ Prešlo {passed}/{total} testov")
    if passed == total:
        print("🎉 Všetko je v poriadku!")
    else:
        print("⚠️ Niektoré testy zlyhali.")
