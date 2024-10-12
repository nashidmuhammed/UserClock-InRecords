# UserClock-InRecords
# FastAPI Item Management Application


## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- MongoDB installed and running locally or on a cloud provider
- pip (Python package installer)

## Installation

1. Clone the repository:
   git clone https://github.com/nashidmuhammed/UserClock-InRecords.git
   cd your-repository-name

2.	Create a virtual environment
    python -m venv venv
    source venv/bin/activate 

3. Install required packages
    pip install -r r.txt

4. Run the project
    uvicorn app.main:app --reload

## API Endpoints
<!-- Items CRUD APIs -->
1. POST /items/
    - insert a new item into the database
    - body: {
            "name": "string",
            "email": "string",
            "item_name": "string",
            "quantity": int,
            "expiry_date": "datetime.datetime.now"
            }

2. GET /items/{id}
    - return item from the database based item id
    - body: {"id": "ObjectId"}

3. GET /filter/items
    - return item from the database filtered by email, expiry date, quantity.
    - also return count of items grouped by email bsed on the filter data
    - body: {
            "email": "string",
            "quantity": int,
            "expiry_date": "datetime"
            }
    - filtered objects are optional

4. DELETE /items/{id}
    - delete item from the database based item id
    - body: {"id": "ObjectId"}

5. PUT /items/{id}
    - update specific item from the database based item id
    - body: {
            "id": "ObjectId",
            "name": "string",
            "email": "string",
            "item_name": "string",
            "quantity": int,
            "expiry_date": "datetime.datetime.now"
            }

<!-- User Clock-In Records APIs -->
6. POST /clock-in
    - Insert a new record in the database 
    - body: {
            "email": "string",
            "location": "string"
            }

7. GET /clock-in/{id}
    - return record from the database based item id
    - body: {"id": "ObjectId"}

8. GET /filter/clock-in
    - return record from the database filtered by email, location, insert_datetime.
    - body: {
            "email": "string",
            "location": "string",
            "insert_datetime": "datetime"
            }
    - filtered objects are optional

9. DELETE /clock-in/{id}
    - delete record from the database based record id
    - body: {"id": "ObjectId"}

10. PUT /clock-in/{id}
    - update specific record from the database based record id
    - body: {
            "id": "ObjectId",
            "email": "string",
            "location": "string"
            }
