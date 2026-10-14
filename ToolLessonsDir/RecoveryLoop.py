from Tools import execute_python_sandbox
from ErrorRecovery import analyze_error

def recovery_loop(code: str, max_retries: int = 3) -> dict:

    history = []
    retries_used = 0
    res = {
        "success": None,
        "status": None,
        "final_code": code,
        "retries_used": 0,
        "history": history
    }

    for attempt in range(max_retries + 1):

        if attempt == max_retries:
            res["status"] = "max_retries"
            res["success"] = False
            break

        print(f"\n--- Attempt {attempt} ---")

        result = execute_python_sandbox(res['final_code'], 20)

        history.append({'attempt': attempt,
                        'code': res['final_code'],
                        'result': result})

        if result['cleanup_success'] == False:
            res['status'] = 'cleanup_failed'
            res['success'] = False

            break

        if result['error_source'] == 'timeout':
            res['status'] = 'timeout'
            res['success'] = False
            break

        if result['error_source'] == 'infrastructure':
            res['status'] = 'infrastructure_error'
            res['success'] = False
            break

        if result['success'] == True:
            res['status'] = 'completed'
            res['success'] = True
            break

        fix = analyze_error(res['final_code'], result)

        print('Python code Error')
        print(f'Explanation:\n{fix.explanation}')
        print(f'Corrected code:\n{fix.corrected_code}\n')

        confirmation = input('Execute new code (yes/no):')

        if confirmation != "yes":
            print("Execution cancelled.")
            res['status'] = 'rejected'
            res['success'] = False
            break

        res['final_code'] = fix.corrected_code
        res['retries_used'] += 1

    return res
