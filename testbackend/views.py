from django.shortcuts import render

# Create your views here.

import psycopg2
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

DB_CONFIG = {
    'user': 'postgres',
    'password': 'Shivakumar@12',   # ✅ Make sure this matches your pgAdmin login
    'host': 'localhost',
    'port': 5432,
    'database': 'gsm_new'          # ✅ Your DB
}

def get_connection():
    return psycopg2.connect(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        database=DB_CONFIG['database']
    )



@csrf_exempt
def insert_department(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        department_name = data.get("department_name")
        status = data.get('status')

        if not department_name or not status:
            return JsonResponse({'message':"Department Name and Status."}, status=400)

        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = ''' INSERT INTO departments (department_name, status) VALUES (%s, %s) '''

            cursor.execute(sql, (department_name, status))
            conn.commit()

            return JsonResponse({"message":"Department Inserted"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            cursor.close()
            conn.close()
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def get_department(request):
    conn = psycopg2.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host='localhost',
            port=5432,
            database=DB_CONFIG.get('database')
        )

    cursor = conn.cursor()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ RAW SQL SELECT
        cursor.execute("SELECT department_id, department_name, status FROM departments")
        rows = cursor.fetchall()
        departments = [{'id': r[0], 'department_name': r[1], 'status': r[2]} for r in rows]  # ✅

        return JsonResponse(departments, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()

@csrf_exempt
def update_department(request, department_id):
    if request.method == "PUT":   
        data = json.loads(request.body)
        department_name = data.get("department_name")
        status = data.get('status')

        if not department_name or not status:
            return JsonResponse({'message':"Department Name and Status."}, status=400)
    
        if request.method == "PUT":
            try: 
          
                conn = get_connection()
                cursor = conn.cursor()

                sql = 'UPDATE departments SET department_name = %s, status = %s WHERE department_id = %s'
                cursor.execute(sql, (department_name, status, department_id))

                conn.commit()
                return JsonResponse({'message': "department updated successfully"})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            finally:
                cursor.close()
                conn.close()
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def delete_department(request, department_id):
    if request.method == "DELETE":
        try: 
           conn = get_connection()
           cursor = conn.cursor()

           sql = 'DELETE FROM departments WHERE department_id = %s'
           cursor.execute(sql, (department_id,))

           conn.commit()
           return JsonResponse({'message': "department deleted successfully"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            cursor.close()
            conn.close()
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)