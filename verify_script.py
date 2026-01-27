import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header('Content-Type', 'application/json')
        
        if data:
            json_data = json.dumps(data).encode('utf-8')
            req.data = json_data
            
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            if response_body:
                return status_code, json.loads(response_body)
            return status_code, {}
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def print_result(name, result, expected_status=[200, 201, 204]):
    status_code, body = result
    if status_code in expected_status:
        print(f"[PASS] {name} - Status: {status_code}")
        return True, body
    else:
        print(f"[FAIL] {name} - Status: {status_code}")
        print(body)
        return False, body

def test_user_crud():
    print("\n--- Testing User CRUD ---")
    # 1. Create User
    user_data = {"username": "testuser_crud_urllib", "email": "crud_urllib@example.com"}
    success, body = print_result("Create User", make_request(f"{BASE_URL}/users/", "POST", user_data), [201])
    if not success:
        return
        
    user_id = body['id']
    print(f"Created User ID: {user_id}")
    
    # 2. Get User by ID
    print_result("Get User By ID", make_request(f"{BASE_URL}/users/{user_id}/"))
    
    # 3. Update User
    update_data = {"username": "testuser_updated_urllib", "email": "updated_urllib@example.com"}
    print_result("Update User", make_request(f"{BASE_URL}/users/{user_id}/", "PUT", update_data))
    
    # 4. Delete User
    print_result("Delete User", make_request(f"{BASE_URL}/users/{user_id}/", "DELETE"), [204])

def test_review_crud():
    print("\n--- Testing Review CRUD (MongoDB) ---")
    # 1. Create Review
    review_data = {
        "product_id": 1,
        "user_id": 1,
        "rating": 5,
        "comment": "Great product (urllib)!"
    }
    success, body = print_result("Create Review", make_request(f"{BASE_URL}/reviews/", "POST", review_data), [201])
    if not success:
        return
        
    review_id = body['_id']
    print(f"Created Review ID: {review_id}")
    
    # 2. Get Review by ID
    print_result("Get Review By ID", make_request(f"{BASE_URL}/reviews/{review_id}/"))
    
    # 3. Update Review
    update_data = {
        "rating": 4,
        "comment": "Good product."
    }
    print_result("Update Review", make_request(f"{BASE_URL}/reviews/{review_id}/", "PUT", update_data))
    
    # 4. Delete Review
    print_result("Delete Review", make_request(f"{BASE_URL}/reviews/{review_id}/", "DELETE"), [204])

def test_order_nested_creation():
    print("\n--- Testing Order Nested Creation ---")
    # NEED A PRODUCT FIRST
    product_data = {"name": "Test Product Urllib", "price": "10.00", "description": "Desc"}
    success, product_body = print_result("Create Product", make_request(f"{BASE_URL}/products/", "POST", product_data), [201])
    if not success:
        return
    product_id = product_body['id']

    # Create Order
    order_data = {
        "status": "PENDING",
        "items": [
            {"product": product_id, "quantity": 3}
        ]
    }
    success, body = print_result("Create Nested Order", make_request(f"{BASE_URL}/orders/", "POST", order_data), [201])
    if success:
        items = body.get('items', [])
        if len(items) == 1 and items[0]['quantity'] == 3 and items[0]['product'] == product_id:
            print("[PASS] Nested items verified")
        else:
            print("[FAIL] Nested items verification failed")
            print(json.dumps(items, indent=2))

if __name__ == "__main__":
    try:
        test_user_crud()
        test_review_crud()
        test_order_nested_creation()
    except Exception as e:
        print(f"Test failed with exception: {e}")
