# Vendor Management System

This project is a Vendor Management System developed using Django. It provides APIs for managing vendor profiles and tracking purchase orders.

## General Explanation

The Vendor Management System allows you to perform the following actions:

- Create, update, list and delete vendor profiles.
- Track purchase orders, including creation, updating, acknowledging, and deletion.
- Retrieve performance metrics for specific vendors.

## Requirements

- Python 3.9.9
- Django 3.2
- Django Rest Framework 3.13.1
- pytz 2022.7.1


## Steps to setup
1. Clone this repository
2. Install the requiremnets
3. Apply migrations
4. Run the development server

## API Documentation

### Vendor Profile Management

1. **Create Vendor:**
   - Endpoint: `POST http://127.0.0.1:8000/api/vendors/`
   - Request Sample:

     ```json
     {
       "vendor_code": "a1",
       "name": "Xyz",
       "contact_details": "1234567890",
       "address": "Vendor's address......"
     }
     ```

2. **List All Vendors:**
   - Endpoint: `GET http://localhost:8000/api/vendors/`

3. **List Specific Vendor:**
   - Endpoint: `GET http://localhost:8000/api/vendors/{vendor_id}/`

4. **Update Vendor Details:**
   - Endpoint: `PUT http://localhost:8000/api/vendors/{vendor_id}/`
   - Request Sample:

     ```json
     {
       "vendor_code": "a1",
       "name": "Abc",
       "contact_details": "4564564567",
       "address": "Updated address"
     }
     ```

5. **Delete Vendor:**
   - Endpoint: `DELETE http://localhost:8000/api/vendors/{vendor_id}/`

6. **Vendor Performance Metrics:**
   - Endpoint: `GET http://localhost:8000/api/vendors/{vendor_id}/performance/`

### Purchase Order Tracking

1. **Create an Order:**
   - Endpoint: `POST http://localhost:8000/api/vendors/{vendor_id}/performance/`
   - Request Sample:

     ```json
     {
       "vendor": 5,
       "po_number": "P001",
       "order_date": "2023-12-09",
       "expected_delivery_date": "2023-12-12",
       "delivered_date": null,
       "items": "Soap",
       "quantity": 100,
       "status": "pending",
       "quality_rating": null,
       "issue_date": "2023-12-08"
     }
     ```

2. **List All Orders:**
   - Endpoint: `GET http://localhost:8000/api/purchase_orders/`
   - List All Orders from a Specific Vendor:
     - Endpoint: `GET http://localhost:8000/api/purchase_orders/?vendor_id={vendor_id}`

3. **List Specific Order:**
   - Endpoint: `GET http://localhost:8000/api/purchase_orders/{po_id}/`

4. **Acknowledge Purchase Order:**
   - Endpoint: `PUT http://localhost:8000/api/purchase_orders/{po_id}/acknowledge/`

5. **Update Order:**
   - Endpoint: `PUT http://localhost:8000/api/purchase_orders/{po_id}/`
   - Request Sample:

     ```json
     {
       "po_id": 24,
       "vendor": 5,
       "po_number": "P002",
       "order_date": "2023-12-07",
       "expected_delivery_date": "2023-12-10",
       "delivered_date": "2023-12-13",
       "items": "Soap",
       "quantity": 100,
       "status": "COMPLETED",
       "quality_rating": 5,
       "issue_date": "2023-12-06T00:00:00Z",
       "acknowledgment_date": null
     }
     ```

6. **Delete an Order:**
   - Endpoint: `DELETE http://localhost:8000/api/purchase_orders/{po_id}/`
