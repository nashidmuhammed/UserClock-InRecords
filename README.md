# UserClock-InRecords
# FastAPI Item Management Application


## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- MongoDB installed and running locally or on a cloud provider
- pip (Python package installer)

## Installation

1. Clone the repository:
   git clone https://github.com/your-username/your-repository-name.git
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
1.POST /items/
2.GET /items/{id}
3.GET /filter/items
4.DELETE /items/{id}
5.PUT /items/{id}

<!-- User Clock-In Records APIs -->
6.POST /clock-in
7.GET /clock-in/{id}
8.GET /filter/clock-in
9.DELETE /clock-in/{id}
10.PUT /clock-in/{id}
