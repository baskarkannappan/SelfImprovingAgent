BENCHMARK_TASKS = [
    {
        "task_id": "B001",
        "task": "Design a simple Python dictionary-based memory cache class with set, get, and delete methods."
    },
    {
        "task_id": "B002",
        "task": "Update the memory cache class to include a Time-To-Live (TTL) expiration feature. Ensure the get method returns None if the item has expired."
    },
    {
        "task_id": "B003",
        "task": "Refactor our TTL memory cache class to be completely thread-safe using the threading module so that it can handle concurrent reads and writes."
    },
    {
        "task_id": "B004",
        "task": "Create a simple FastAPI endpoint (/session) that uses our thread-safe TTL memory cache class to store and retrieve user session tokens."
    },
    {
        "task_id": "B005",
        "task": "Write a suite of unit tests for the FastAPI endpoint using pytest. Mock the time module to specifically test that the TTL expiration logic works properly."
    },
    {
        "task_id": "B006",
        "task": "Design a scalable order management architecture for 10,000 concurrent users including database, API, and caching."
    },
    {
        "task_id": "B007",
        "task": "Design a production-ready commerce architecture supporting 20,000 concurrent users. Include customer, order, payment, shipping, inventory, and messaging."
    },
    {
        "task_id": "B008",
        "task": "Evaluate an architecture for 100,000 users where all services share one relational database and all requests are synchronous. Identify problems and propose solutions."
    },
    {
        "task_id": "B009",
        "task": "Compare a shared database architecture vs a database-per-service architecture for an order processing system."
    },
    {
        "task_id": "B010",
        "task": "Design a complete production-ready order management platform with Notifications, Order Tracking, Inventory, and Payment handling."
    }
]
